from google.adk.tools.agent_tool import AgentTool
from debate_agents.agents.critique_agent import get_critique_agent

def get_critique_tool():
    """
    Returns an AgentTool that wraps the CritiqueAgent.
    This allows other agents to invoke the critique agent to evaluate their tactics and personas.
    """
    critique_agent = get_critique_agent()
    return AgentTool(
        agent=critique_agent,
        skip_summarization=False
    )
