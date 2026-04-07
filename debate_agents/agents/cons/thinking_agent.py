import os
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from debate_agents.config import GEMINI_MODEL_ADAPTER # Updated import
from debate_agents.tools.memory_tools import get_write_markdown_tool, get_read_markdown_tool

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_cons_thinking_agent():
    return LlmAgent(
        name="ConsThinkingAgent",
        model=GEMINI_MODEL_ADAPTER, # Use the adapter instance
        instruction=load_prompt("cons/thinking_agent.md"),
        description="Analyzes debate history and persona to provide a tactical strategy for the cons.",
        include_contents='none',
        output_key="cons_thinking", # Updated with cons_ prefix
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[get_write_markdown_tool()]
    )
