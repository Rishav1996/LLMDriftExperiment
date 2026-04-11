import os

def load_prompt(filename: str) -> str:
    """Utility to load prompt content from the prompts directory."""
    path = os.path.join("debate_agents_langgraph", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
