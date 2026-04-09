from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_write_markdown_tool
from debate_agents.schema.cons.persona_schema import PersonaSchema
from debate_agents.agents.utils import load_prompt

def get_cons_persona_agent():
    """Factory function for the ConsPersonaAgent."""
    return LlmAgent(
        name="ConsPersonaAgent",
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt("cons/persona_agent.md"),
        description="Designs a deep, consistent adversarial persona for the cons side of the debate.",
        include_contents='none',
        output_key="cons_persona",
        planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)),
        tools=[get_write_markdown_tool()],
        output_schema=PersonaSchema
    )
