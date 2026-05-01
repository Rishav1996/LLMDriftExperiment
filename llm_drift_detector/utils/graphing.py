import json
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import os

class GraphingService:
    def __init__(self, output_dir: str = "Drift Analysis"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_run_visualizations(self, run_name: str, analysis_results: Dict[str, Any]):
        """
        Generates and saves plots for a specific run's analysis results.
        """
        print(f"GraphingService: Generating visualizations for {run_name}...")
        
        # 1. Overall Drift Trend
        self._plot_overall_drift_trend(run_name, analysis_results)
        
        # 2. Category Breakdown (most recent round or all rounds)
        pros_drift = analysis_results.get("pros_agent_drift", {})
        cons_drift = analysis_results.get("cons_agent_drift", {})
        all_rounds = sorted(list(set(pros_drift.keys()) | set(cons_drift.keys())), key=lambda x: int(x.split('_')[1]))
        
        if all_rounds:
            last_round = all_rounds[-1]
            self._plot_category_scores(run_name, last_round, analysis_results, "Pros")
            self._plot_category_scores(run_name, last_round, analysis_results, "Cons")

    def _plot_overall_drift_trend(self, run_name: str, analysis_results: Dict[str, Any]):
        pros_drift = analysis_results.get("pros_agent_drift", {})
        cons_drift = analysis_results.get("cons_agent_drift", {})
        
        rounds = sorted([int(k.split('_')[1]) for k in pros_drift.keys()])
        pros_scores = [pros_drift[f"round_{r}"].get("overall_drift", 0) for r in rounds]
        cons_scores = [cons_drift[f"round_{r}"].get("overall_drift", 0) for r in rounds]

        plt.figure(figsize=(10, 6))
        plt.plot(rounds, pros_scores, marker='o', label='Pros Agent', color='blue')
        plt.plot(rounds, cons_scores, marker='o', label='Cons Agent', color='red')
        
        plt.title(f'Overall Drift Trend: {run_name}')
        plt.xlabel('Round')
        plt.ylabel('Drift Score')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        save_path = os.path.join(self.output_dir, f"{run_name}_trend.png")
        plt.savefig(save_path)
        plt.close()
        print(f"Saved trend plot to {save_path}")

    def _plot_category_scores(self, run_name: str, round_id: str, analysis_results: Dict[str, Any], agent_type: str):
        agent_key = f"{agent_type.lower()}_agent_drift"
        round_data = analysis_results.get(agent_key, {}).get(round_id, {})
        category_scores = round_data.get("category_scores", {})
        
        if not category_scores:
            return

        categories = []
        scores = []
        for cat, skills in category_scores.items():
            if skills:
                avg = sum(skills.values()) / len(skills)
                categories.append(cat)
                scores.append(avg)

        plt.figure(figsize=(10, 6))
        plt.bar(categories, scores, color='skyblue' if agent_type == "Pros" else 'salmon')
        plt.title(f'Category Scores: {agent_type} Agent ({round_id})')
        plt.ylabel('Average Score')
        plt.ylim(0, 1) # Assuming standard normalization
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        save_path = os.path.join(self.output_dir, f"{run_name}_{agent_type.lower()}_{round_id}_categories.png")
        plt.savefig(save_path)
        plt.close()
        print(f"Saved category plot to {save_path}")
