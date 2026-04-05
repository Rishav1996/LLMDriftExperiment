from google.adk.tools.agent_tool import AgentTool
# Updated import path for the critique agent
from debate_agents.agents.pros.critique_agent import get_pros_critique_agent

def get_critique_tool():
    """
    Returns an AgentTool that wraps the ProsCritiqueAgent.
    This allows other agents to invoke the pros critique agent to evaluate their tactics and personas.
    """
    # Instantiate the pros version of the critique agent
    critique_agent = get_pros_critique_agent()
    return AgentTool(
        agent=critique_agent,
        skip_summarization=False
    )
