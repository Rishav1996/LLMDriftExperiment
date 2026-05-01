import json
import os
from typing import Dict, List, Any, Optional

class Rubric:
    def __init__(self, score_description_mapping: Dict[float, str], scoring_range: List[float]):
        self.score_description_mapping = score_description_mapping
        self.scoring_range = scoring_range

    def get_description(self, score: float) -> str:
        # Find the closest score in the rubric and return its description
        # This is a simplified approach; a more robust method might interpolate or use nearest neighbor
        closest_score = min(self.score_description_mapping.keys(), key=lambda x: abs(x - score))
        return self.score_description_mapping.get(closest_score, "Score out of rubric range.")

    def get_range(self) -> List[float]:
        return self.scoring_range

class LLMDriftSkill:
    def __init__(self, name: str, category: str, technical_definition: str, prompt_guidelines_summary: str, evaluation_rubric_summary: str, scoring_range: List[float]):
        self.name = name
        self.category = category
        self.technical_definition = technical_definition
        self.prompt_guidelines_summary = prompt_guidelines_summary
        self.scoring_range = scoring_range

        # Parse the evaluation rubric summary to create a Rubric object
        self.rubric = self._parse_rubric(evaluation_rubric_summary, scoring_range)

    def _parse_rubric(self, rubric_summary: str, scoring_range: List[float]) -> Rubric:
        score_description_mapping = {}
        lines = rubric_summary.split(' - ') # Split by the dash separator used in summaries

        # Handle cases where rubric might be just a score range or a simple description
        if len(lines) < 2 and len(rubric_summary.strip()) > 0:
            # If it's not clearly delineated by score-description pairs, try to infer
            # This part might need refinement based on actual rubric variations.
            # For now, we'll try to extract scores and descriptions more loosely.
            import re
            # Regex to find score (float) and description
            matches = re.findall(r"(-?\d+\.?\d*)\s*\((.*?)\)", rubric_summary)
            if matches:
                for score_str, description in matches:
                    try:
                        score = float(score_str)
                        score_description_mapping[score] = description.strip()
                    except ValueError:
                        continue # Skip if score is not a valid float
            else:
                 # Fallback for simple ranges without explicit score numbers in summary if possible
                if len(scoring_range) == 2:
                    score_description_mapping[scoring_range[0]] = "Minimum score"
                    score_description_mapping[scoring_range[1]] = "Maximum score"
                    score_description_mapping[(scoring_range[0] + scoring_range[1])/2] = "Mid-range score"
        else:
            # Assume format like "-1.0 (Egocentric/Blind): Ignores context, literal."
            for line in lines:
                parts = line.strip().split('): ')
                if len(parts) == 2:
                    score_part = parts[0]
                    description = parts[1]
                    
                    try:
                        # Extract score from string like "-1.0 (Egocentric/Blind)"
                        score_match = re.match(r"(-?\d+\.?\d*)\s*\(", score_part)
                        if score_match:
                            score = float(score_match.group(1))
                            score_description_mapping[score] = description.strip()
                        else:
                            # Fallback if score is not explicitly captured, try to infer from range
                            if len(scoring_range) == 2:
                                # A more complex mapping might be needed if scores aren't explicit
                                pass # For now, this structure is assumed to have explicit scores
                    except ValueError:
                        continue # Skip if score is not a valid float
                elif len(parts) == 1 and len(rubric_summary.strip()) > 0:
                    # Handle cases where rubric might not have explicit scores but just labels
                    # This is a basic fallback and might need more advanced parsing logic
                    pass
        
        # If after parsing, the mapping is empty, create a default based on scoring range
        if not score_description_mapping and len(scoring_range) == 2:
            score_description_mapping[scoring_range[0]] = "Minimum score"
            score_description_mapping[scoring_range[1]] = "Maximum score"
            score_description_mapping[(scoring_range[0] + scoring_range[1])/2] = "Mid-range score"

        return Rubric(score_description_mapping, scoring_range)

    def get_rubric_description(self, score: float) -> str:
        return self.rubric.get_description(score)

class LLMDriftSkillsManager:
    def __init__(self, config_path: str = "llm_drift_library/config/skills.json"):
        self.skills_config_path = config_path
        self.skills: Dict[str, LLMDriftSkill] = {}
        self._load_skills()

    def _load_skills(self):
        if not os.path.exists(self.skills_config_path):
            print(f"Warning: Skills configuration file not found at {self.skills_config_path}")
            return

        try:
            with open(self.skills_config_path, 'r') as f:
                config_data = json.load(f)
            
            for skill_data in config_data.get("skills", []):
                skill = LLMDriftSkill(
                    name=skill_data.get("name"),
                    category=skill_data.get("category"),
                    technical_definition=skill_data.get("technical_definition"),
                    prompt_guidelines_summary=skill_data.get("prompt_guidelines_summary"),
                    evaluation_rubric_summary=skill_data.get("evaluation_rubric_summary"),
                    scoring_range=skill_data.get("scoring_range")
                )
                self.skills[skill.name.lower()] = skill
        except Exception as e:
            print(f"Error loading skills from {self.skills_config_path}: {e}")

    def get_skill(self, skill_name: str) -> Optional[LLMDriftSkill]:
        return self.skills.get(skill_name.lower())

    def get_all_skills(self) -> List[LLMDriftSkill]:
        return list(self.skills.values())

    def get_skills_by_category(self, category: str) -> List[LLMDriftSkill]:
        return [skill for skill in self.skills.values() if skill.category.lower() == category.lower()]

    def get_all_categories(self) -> List[str]:
        return sorted(list(set(skill.category for skill in self.skills.values())))
