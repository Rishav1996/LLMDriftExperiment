from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_write_markdown_tool, get_read_markdown_tool
from debate_agents.schema.pros.critique_schema import CritiqueSchema
from debate_agents.agents.utils import load_prompt

def get_pros_critique_agent():
    """Factory function for the ProsCritiqueAgent."""
    return LlmAgent(
        name="ProsCritiqueAgent",
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt("pros/critique_agent.md"),
        description="Evaluates and refines pros persona profiles and strategic plans.",
        include_contents='none',
        output_key="pros_critique",
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[get_write_markdown_tool(), get_read_markdown_tool()],
        output_schema=CritiqueSchema
    )
