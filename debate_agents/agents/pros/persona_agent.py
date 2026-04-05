import os
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.adk.tools.google_search_tool import google_search
from google.genai import types
from debate_agents.config import GEMINI_MODEL, GLOBAL_GENERATE_CONTENT_CONFIG

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_pros_persona_agent(): # Renamed function
    return LlmAgent(
        name="ProsPersonaAgent", # Renamed agent name
        model=GEMINI_MODEL,
        instruction=load_prompt("pros/persona_agent.md"), # Updated prompt path
        description="Designs a deep, consistent adversarial persona for the pros side of the debate.", # Updated description
        include_contents='none',
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[google_search]
    )
