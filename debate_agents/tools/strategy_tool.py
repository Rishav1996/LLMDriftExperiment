from google.adk.tools.agent_tool import AgentTool
from debate_agents.agents.thinking_agent import get_thinking_agent

def get_strategy_tool():
    """
    Returns an AgentTool that wraps the StrategyThinkingAgent.
    This allows other agents to invoke the thinking agent as a specialized tool.
    """
    thinking_agent = get_thinking_agent()
    return AgentTool(
        agent=thinking_agent,
        skip_summarization=False # Let the parent agent summarize the strategy if needed
    )
