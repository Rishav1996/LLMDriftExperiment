import os
import json
import time
from typing import Dict, List, Any, Optional
from .skills import LLMDriftSkillsManager
from .metrics_ragas import LLMDriftRagasMetricsManager
from .data_processing import ResearchRunLoader

class DriftEvaluator:
    def __init__(self, skills_config_path: str = "llm_drift_detector/utils/config/skills.json"):
        self.skills_manager = LLMDriftSkillsManager(skills_config_path)
        self.metrics_manager = LLMDriftRagasMetricsManager()
        self.run_loader = ResearchRunLoader()
        
        # Register all skills as RAGAS metrics
        for skill in self.skills_manager.get_all_skills():
            self.metrics_manager.register_metric_from_skill(
                skill_name=skill.name,
                category=skill.category,
                technical_definition=skill.technical_definition,
                prompt_guidelines_summary=skill.prompt_guidelines_summary,
                evaluation_rubric_summary=skill.rubric.score_description_mapping, # Pass mapping directly
                scoring_range=skill.scoring_range
            )

    def evaluate_round(self, run_data: Dict[str, Any], round_num: int, agent_type: str, num_iterations: int = 1, target_metrics: Optional[List[str]] = None, wait_time: int = 5) -> Dict[str, Any]:
        """
        Evaluates a specific round for an agent.
        target_metrics: Optional list of skill names to evaluate. If None, evaluates all.
        wait_time: Seconds to sleep after each metric evaluation.
        """
        texts = self.run_loader.extract_agent_round_text(run_data, round_num, agent_type)
        conversation_turn = texts.get("conversation_turn", "")
        
        if not conversation_turn:
            print(f"Warning: No text found for {agent_type} in round {round_num}")
            return {}

        all_categories = self.skills_manager.get_all_categories()
        all_skills_to_evaluate = []
        skill_to_category_map = {}

        for category in all_categories:
            skills_in_category = self.skills_manager.get_skills_by_category(category)
            
            # Filter skills if target_metrics is provided
            if target_metrics:
                skills_in_category = [s for s in skills_in_category if s.name in target_metrics]
            
            for skill in skills_in_category:
                all_skills_to_evaluate.append(skill)
                skill_to_category_map[skill.name.lower()] = category

        if not all_skills_to_evaluate:
            return {}

        # Prepare all metrics for the batch call
        metrics_to_run = [self.metrics_manager.get_metric(skill.name) for skill in all_skills_to_evaluate]
        
        print(f"--- [Batch] Evaluating {len(metrics_to_run)} metrics for {agent_type} round {round_num} ---")
        
        # Call global batch evaluation method
        batch_results = self.metrics_manager.batch_score(
            texts=conversation_turn,
            persona=texts.get("persona", ""),
            metrics=metrics_to_run,
            num_iterations=num_iterations
        )
        
        # Re-organize results into category_scores
        category_scores = {cat: {} for cat in all_categories}
        for skill_name_lower, score in batch_results.items():
            category = skill_to_category_map.get(skill_name_lower)
            if category:
                # Find the original skill name for the key if needed, or just use the lower one
                # The skills_manager uses original names, so let's try to match it
                original_skill = next((s for s in all_skills_to_evaluate if s.name.lower() == skill_name_lower), None)
                if original_skill:
                    category_scores[category][original_skill.name] = score
                else:
                    category_scores[category][skill_name_lower] = score

        # Clean up empty categories
        category_scores = {k: v for k, v in category_scores.items() if v}

        if wait_time > 0:
            print(f"--- [Wait] Sleeping {wait_time}s after global batch evaluation ---")
            time.sleep(wait_time)

        overall_scores = self.calculate_overall_scores(category_scores)

        return {
            "round": round_num,
            "agent_type": agent_type,
            "category_scores": category_scores,
            "overall_scores": overall_scores,
            "evaluated_metrics": target_metrics if target_metrics else "all"
        }

    def calculate_overall_scores(self, category_scores: Dict[str, Dict[str, float]]) -> float:
        """
        Implements the hierarchical weighting system from persona_dna.md.
        """

        if not category_scores:
            return 0.0

        group_averages = []
        for category, skills in category_scores.items():
            if skills:
                avg = sum(skills.values()) / len(skills)
                group_averages.append(avg)
        
        if not group_averages:
            return 0.0
            
        return sum(group_averages) / len(group_averages)

    def evaluate_all_runs(self, base_path: str, num_iterations: int = 1, wait_time: int = 5) -> Dict[str, Any]:
        """
        Evaluates all runs in the specified directory.
        """
        all_runs = self.run_loader.load_all_runs(base_path)
        results = {}

        for run_name, run_data in all_runs.items():
            print(f"Evaluating run: {run_name}")
            num_rounds = self.run_loader.get_number_of_rounds(run_data)
            
            run_results = {
                "pros_agent_scores": {},
                "cons_agent_scores": {}
            }

            for round_num in range(1, num_rounds + 1):
                run_results["pros_agent_scores"][f"round_{round_num}"] = self.evaluate_round(run_data, round_num, "Pros", num_iterations, wait_time=wait_time)
                run_results["cons_agent_scores"][f"round_{round_num}"] = self.evaluate_round(run_data, round_num, "Cons", num_iterations, wait_time=wait_time)
            
            results[run_name] = run_results
            
        return results
