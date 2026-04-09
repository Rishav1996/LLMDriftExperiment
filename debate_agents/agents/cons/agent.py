import os
import json
from google.adk.agents import LoopAgent, LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.planners import BuiltInPlanner
from google.genai import types
from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_read_json_tool, write_json_direct
from debate_agents.schema.cons.cons_schema import PersonaSchema, ThinkingSchema, CritiqueSchema, AgentSchema
from debate_agents.agents.base.utils import load_prompt
from debate_agents.agents.base.factory import create_base_agent

# --- Callbacks ---
async def save_persona_callback(callback_context):
    await write_json_direct("persona.json", callback_context.state.get("cons_persona"), "ConsPersonaAgent")

async def save_thinking_callback(callback_context):
    await write_json_direct("thinking.json", callback_context.state.get("cons_thinking"), "ConsThinkingAgent")

async def save_critique_callback(callback_context):
    await write_json_direct("critique.json", callback_context.state.get("cons_critique"), "ConsCritiqueAgent")

# --- Agent Factories ---
def get_cons_persona_agent():
    return create_base_agent("ConsPersonaAgent", "cons/persona_agent.md", "Designs a persona.", "cons_persona", PersonaSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=save_persona_callback)

def get_cons_thinking_agent():
    return create_base_agent("ConsThinkingAgent", "cons/thinking_agent.md", "Analyzes debate.", "cons_thinking", ThinkingSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=save_thinking_callback)

def get_cons_critique_agent():
    return create_base_agent("ConsCritiqueAgent", "cons/critique_agent.md", "Evaluates arguments.", "cons_critique", CritiqueSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=save_critique_callback)

def get_cons_agent():
    return LoopAgent(
        name="ConsAgent",
        sub_agents=[get_cons_persona_agent(), get_cons_thinking_agent(), get_cons_critique_agent()],
        max_iterations=5,
        description="Coordinates iterative debate refinement loop."
    )
