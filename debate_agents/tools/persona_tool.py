from google.adk.tools.agent_tool import AgentTool
from debate_agents.agents.persona_agent import get_persona_agent

def get_persona_tool():
    """
    Returns an AgentTool that wraps the PersonaDesignAgent.
    This allows other agents to invoke the persona agent as a specialized tool.
    """
    persona_agent = get_persona_agent()
    return AgentTool(
        agent=persona_agent,
        skip_summarization=True # Persona profiles are usually well-formatted
    )
