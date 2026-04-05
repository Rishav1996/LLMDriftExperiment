from google.adk.tools.agent_tool import AgentTool
# Updated import path for the strategy agent
from debate_agents.agents.cons.thinking_agent import get_cons_thinking_agent

def get_strategy_tool():
    """
    Returns an AgentTool that wraps the ConsThinkingAgent.
    This allows other agents to invoke the cons thinking agent as a specialized tool.
    """
    # Instantiate the cons version of the thinking agent
    thinking_agent = get_cons_thinking_agent() 
    return AgentTool(
        agent=thinking_agent,
        skip_summarization=False # Let the parent agent summarize the strategy if needed
    )
