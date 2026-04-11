import json
import os
from google.adk.agents import LoopAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.planners import BuiltInPlanner
from google.genai import types
from debate_agents.tools.memory_tools import get_read_json_tool
from debate_agents.schema.cons_schema import PersonaSchema, ThinkingSchema, CritiqueSchema
from debate_agents.agents.base.factory import create_base_agent
from debate_agents.agents.base.persistence import (
    save_critique_callback,
    save_persona_callback,
    save_thinking_callback,
)

async def check_critique_approval(callback_context: CallbackContext) -> None:
    """
    Checks if the CritiqueAgent has approved the argument.
    If approved, save the critique result and stop the loop.
    """
    # 1. Save the critique output first (callback ensures it's persisted)
    await save_critique_callback(callback_context)
    
    # 2. Check for approval
    critique_file = os.path.join("debate_agents", "memory", "cons_memory", "critique.json")
    if os.path.exists(critique_file):
        with open(critique_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if data and isinstance(data, list):
                    # Check the last critique entry
                    last_critique = data[-1].get("content", {})
                    # Ensure content is dict
                    if isinstance(last_critique, str):
                        try: last_critique = json.loads(last_critique)
                        except: pass
                    
                    if isinstance(last_critique, dict) and last_critique.get("approved") is True:
                        # Escalation triggers the LoopAgent to stop
                        callback_context.actions.escalate = True
            except json.JSONDecodeError: pass

def get_cons_agent():
    persona_agent = create_base_agent("ConsPersonaAgent", "cons/persona_agent.md", "Designs a persona.", "cons_persona", PersonaSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=save_persona_callback)
    thinking_agent = create_base_agent("ConsThinkingAgent", "cons/thinking_agent.md", "Analyzes debate.", "cons_thinking", ThinkingSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=save_thinking_callback)
    critique_agent = create_base_agent("ConsCritiqueAgent", "cons/critique_agent.md", "Evaluates arguments.", "cons_critique", CritiqueSchema, planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=512)), tools=[get_read_json_tool()], callback=None)
    
    # Register the approval check (which now includes saving) as the critique agent's callback
    critique_agent.after_agent_callback = check_critique_approval
    
    return LoopAgent(
        name="ConsAgent",
        sub_agents=[persona_agent, thinking_agent, critique_agent],
        max_iterations=5,
        description="Coordinates iterative debate refinement loop."
    )
