from google.adk.tools.agent_tool import AgentTool
# Updated import path for the persona agent
from debate_agents.agents.cons.persona_agent import get_cons_persona_agent

def get_cons_persona_tool():
    """
    Returns an AgentTool that wraps the ConsPersonaAgent.
    This allows other agents to invoke the cons persona agent for persona design.
    """
    # Instantiate the cons version of the persona agent
    persona_agent = get_cons_persona_agent()
    return AgentTool(
        agent=persona_agent,
        skip_summarization=True # Persona profiles are usually well-formatted
    )
