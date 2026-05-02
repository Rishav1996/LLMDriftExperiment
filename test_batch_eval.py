import sys
import os
from llm_drift_detector.utils.evaluator import DriftEvaluator

def test_batch():
    evaluator = DriftEvaluator()
    base_path = "Research Runs"
    
    # Just try to evaluate one round of one run
    run_name = "memory-v1-temp-0-max-tokens-2048"
    run_path = os.path.join(base_path, run_name)
    
    if not os.path.exists(run_path):
        print(f"Run path {run_path} not found.")
        return

    from llm_drift_detector.utils.data_processing import ResearchRunLoader
    loader = ResearchRunLoader()
    all_runs = loader.load_all_runs(base_path)
    run_data = all_runs.get(run_name)
    
    if not run_data:
        print(f"Run data for {run_name} not found.")
        return

    print(f"Testing batch evaluation for {run_name}, Round 1, Pros Agent...")
    # Evaluate with just a couple of metrics to save time/cost
    target_metrics = ["Theory of Mind", "Politeness", "Emotional Tone"]
    
    result = evaluator.evaluate_round(
        run_data=run_data,
        round_num=1,
        agent_type="Pros",
        target_metrics=target_metrics,
        wait_time=0
    )
    
    print("\nResult:")
    import json
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    test_batch()
