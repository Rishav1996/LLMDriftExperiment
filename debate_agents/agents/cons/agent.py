import os
import json
from google.adk.agents import LoopAgent
from google.adk.agents.callback_context import CallbackContext
from debate_agents.tools.memory_tools import get_read_json_tool, get_write_json_tool
from debate_agents.agents.cons.persona_agent import get_cons_persona_agent
from debate_agents.agents.cons.thinking_agent import get_cons_thinking_agent
from debate_agents.agents.cons.critique_agent import get_cons_critique_agent

def check_critique_approval(callback_context: CallbackContext) -> None:
    """
    Checks if the CritiqueAgent has approved the argument.
    Reads the last entry from critique.json and checks for approved: true.
    """
    critique_file = os.path.join("debate_agents", "memory", "cons_memory", "critique.json")
    if os.path.exists(critique_file):
        with open(critique_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if data and isinstance(data, list):
                    # Check the last critique entry
                    last_critique = data[-1].get("content", {})
                    # Ensure content is dict or parsed string
                    if isinstance(last_critique, str):
                        try:
                            last_critique = json.loads(last_critique)
                        except:
                            pass
                    
                    if isinstance(last_critique, dict) and last_critique.get("approved") is True:
                        callback_context.actions.escalate = True
            except json.JSONDecodeError:
                pass

def get_cons_agent():
    """Factory function for the ConsRootAgent (LoopAgent)."""
    persona_agent = get_cons_persona_agent()
    thinking_agent = get_cons_thinking_agent()
    critique_agent = get_cons_critique_agent()
    
    critique_agent.after_agent_callback = check_critique_approval
    
    return LoopAgent(
        name="ConsAgent",
        sub_agents=[
            persona_agent,
            thinking_agent,
            critique_agent
        ],
        max_iterations=5,
        description="Coordinates iterative debate refinement loop."
    )
