import json
import os
from google.adk.agents import LoopAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.planners import BuiltInPlanner
from google.genai import types

from debate_agents.agents.base.factory import create_base_agent
from debate_agents.agents.base.utils import load_prompt
from debate_agents.agents.pros.callbacks.persistence import (
    save_critique_callback,
    save_persona_callback,
    save_thinking_callback,
)
from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.schema.pros.pros_schema import (
    AgentSchema,
    CritiqueSchema,
    PersonaSchema,
    ThinkingSchema,
)
from debate_agents.tools.memory_tools import get_read_json_tool

def check_critique_approval(callback_context: CallbackContext) -> None:
    critique_file = os.path.join("debate_agents", "memory", "pros_memory", "critique.json")
    if os.path.exists(critique_file):
        with open(critique_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if data and isinstance(data, list):
                    last_critique = data[-1].get("content", {})
                    if isinstance(last_critique, str):
                        try: last_critique = json.loads(last_critique)
                        except: pass
                    if isinstance(last_critique, dict) and last_critique.get("approved") is True:
                        callback_context.actions.escalate = True
            except json.JSONDecodeError: pass

def get_pros_agent():
    persona_agent = create_base_agent("ProsPersonaAgent", "pros/persona_agent.md", "Designs a persona.", "pros_persona", PersonaSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=save_persona_callback)
    thinking_agent = create_base_agent("ProsThinkingAgent", "pros/thinking_agent.md", "Analyzes debate.", "pros_thinking", ThinkingSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=save_thinking_callback)
    critique_agent = create_base_agent("ProsCritiqueAgent", "pros/critique_agent.md", "Evaluates arguments.", "pros_critique", CritiqueSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=save_critique_callback)
    
    critique_agent.after_agent_callback = check_critique_approval
    return LoopAgent(
        name="ProsAgent",
        sub_agents=[persona_agent, thinking_agent, critique_agent],
        max_iterations=5,
        description="Coordinates iterative debate refinement loop."
    )
