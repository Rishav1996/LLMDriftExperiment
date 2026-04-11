from debate_agents.agents.base.factory import AgentWrapper
from debate_agents.schema.topic_extract_schema import TopicExtractSchema
from debate_agents.tools.memory_tools import refresh_memory, write_json_direct
from typing import Any, Dict

async def topic_extractor_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts the debate topic from the user input.

    Args:
        state (Dict[str, Any]): The current LangGraph debate state.

    Returns:
        Dict[str, Any]: The updated state including the topic, current round, and team.
    """
    print("[TopicExtractAgent] Running for Round 1...")
    refresh_memory()
    agent = AgentWrapper(TopicExtractSchema, "topic_extract_agent.md", "TopicExtractAgent")
    # Include round in context for the agent
    context = f"User Input: {state['user_input']}"
    result = await agent.invoke(context, 1)
    topic = result.topic if hasattr(result, "topic") else str(result)
    # The prompt expects the topic to be saved to shared_memory.json
    await write_json_direct("shared_memory.json", topic, "TopicExtractAgent", 1)
    return {"topic": topic, "round": 1, "current_team": "pros"}
