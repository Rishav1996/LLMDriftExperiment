import os
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.adk.tools.google_search_tool import google_search
from google.genai import types
from debate_agents.config import GEMINI_MODEL

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_thinking_agent():
    return LlmAgent(
        name="StrategyThinkingAgent",
        model=GEMINI_MODEL,
        instruction=load_prompt("thinking_agent.md"),
        description="Analyzes debate history and persona to provide a tactical strategy.",
        include_contents='none',
        # Corrected: using thinking_budget instead of max_thinking_tokens
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        # Adding google_search tool
        tools=[google_search]
    )
