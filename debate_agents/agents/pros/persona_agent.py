import os
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.adk.tools.google_search_tool import google_search
from google.genai import types
from debate_agents.config import GEMINI_MODEL_ADAPTER # Updated import
from debate_agents.tools.memory_tools import get_write_markdown_tool

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_pros_persona_agent():
    return LlmAgent(
        name="ProsPersonaAgent",
        model=GEMINI_MODEL_ADAPTER, # Use the adapter instance
        instruction=load_prompt("pros/persona_agent.md"),
        description="Designs a deep, consistent adversarial persona for the pros side of the debate.",
        include_contents='none',
        output_key="pros_persona", # Updated with pros_ prefix
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[google_search, get_write_markdown_tool()]
    )
