import os
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from debate_agents.config import GEMINI_MODEL_ADAPTER # Updated import
from debate_agents.tools.memory_tools import get_write_markdown_tool

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_cons_persona_agent():
    return LlmAgent(
        name="ConsPersonaAgent",
        model=GEMINI_MODEL_ADAPTER, # Use the adapter instance
        instruction=load_prompt("cons/persona_agent.md"),
        description="Designs a deep, consistent adversarial persona for the cons side of the debate.",
        include_contents='none',
        output_key="cons_persona", # Updated with cons_ prefix
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[get_write_markdown_tool()]
    )
