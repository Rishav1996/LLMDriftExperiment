from google.adk.tools.agent_tool import AgentTool
# Updated import path for the critique agent
from debate_agents.agents.cons.critique_agent import get_cons_critique_agent

def get_cons_critique_tool():
    """
    Returns an AgentTool that wraps the ConsCritiqueAgent.
    This allows other agents to invoke the cons critique agent to evaluate their tactics and personas.
    """
    # Instantiate the cons version of the critique agent
    critique_agent = get_cons_critique_agent()
    return AgentTool(
        agent=critique_agent,
        skip_summarization=False
    )
