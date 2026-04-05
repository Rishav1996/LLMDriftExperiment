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

def get_cons_critique_agent(): # Renamed function
    return LlmAgent(
        name="ConsCritiqueAgent", # Renamed agent name
        model=GEMINI_MODEL,
        instruction=load_prompt("cons/critique_agent.md"), # Updated prompt path
        description="Evaluates and refines cons persona profiles and strategic plans.", # Updated description
        include_contents='none',
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[google_search],
        generate_content_config=GLOBAL_GENERATE_CONTENT_CONFIG 
    )
