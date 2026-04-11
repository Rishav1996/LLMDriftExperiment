import mlflow
from typing import Any, Dict

def log_agent_interaction(agent_name: str, round_num: int, token_usage: Dict[str, Any], latency: float):
    """
    Logs token usage and latency metrics to MLflow for an agent interaction.
    """
    with mlflow.start_run(run_name=f"Round_{round_num}_{agent_name}", nested=True):
        mlflow.log_param("agent_name", agent_name)
        mlflow.log_param("round", round_num)
        
        # Log metrics
        mlflow.log_metric("latency_seconds", latency)
        if "prompt_tokens" in token_usage:
            mlflow.log_metric("prompt_tokens", token_usage["prompt_tokens"])
        if "completion_tokens" in token_usage:
            mlflow.log_metric("completion_tokens", token_usage["completion_tokens"])
        if "total_tokens" in token_usage:
            mlflow.log_metric("total_tokens", token_usage["total_tokens"])

def log_state_change(state_key: str, value: Any, round_num: int):
    """
    Logs significant state changes to MLflow.
    """
    # Only log numeric state changes as metrics
    if isinstance(value, (int, float)):
        mlflow.log_metric(f"{state_key}_round_{round_num}", float(value))
