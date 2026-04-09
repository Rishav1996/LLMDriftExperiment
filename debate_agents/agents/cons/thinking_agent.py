from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_write_markdown_tool
from debate_agents.schema.cons.thinking_schema import ThinkingSchema
from debate_agents.agents.utils import load_prompt

def get_cons_thinking_agent():
    """Factory function for the ConsThinkingAgent."""
    return LlmAgent(
        name="ConsThinkingAgent",
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt("cons/thinking_agent.md"),
        description="Analyzes debate history and persona to provide a tactical strategy for the cons.",
        include_contents='none',
        output_key="cons_thinking",
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[get_write_markdown_tool()],
        output_schema=ThinkingSchema
    )
