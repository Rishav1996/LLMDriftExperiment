from google.adk.tools.agent_tool import AgentTool
# Updated import path for the persona agent
from debate_agents.agents.pros.persona_agent import get_pros_persona_agent

def get_pros_persona_tool():
    """
    Returns an AgentTool that wraps the ProsPersonaAgent.
    This allows other agents to invoke the pros persona agent for persona design.
    """
    # Instantiate the pros version of the persona agent
    persona_agent = get_pros_persona_agent()
    return AgentTool(
        agent=persona_agent,
        skip_summarization=True # Persona profiles are usually well-formatted
    )
