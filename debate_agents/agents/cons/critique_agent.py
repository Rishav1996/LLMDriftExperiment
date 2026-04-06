import os
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.adk.tools.google_search_tool import google_search
from google.genai import types
from debate_agents.config import GEMINI_MODEL, GLOBAL_GENERATE_CONTENT_CONFIG
from debate_agents.tools.memory_tools import get_write_markdown_tool, get_read_markdown_tool

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_cons_critique_agent():
    return LlmAgent(
        name="ConsCritiqueAgent",
        model=GEMINI_MODEL,
        instruction=load_prompt("cons/critique_agent.md"),
        description="Evaluates and refines cons persona profiles and strategic plans.",
        include_contents='none',
        output_key="cons_critique", # Updated with cons_ prefix
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[google_search, get_write_markdown_tool(), get_read_markdown_tool()],
        generate_content_config=GLOBAL_GENERATE_CONTENT_CONFIG 
    )
