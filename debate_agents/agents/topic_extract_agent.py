from debate_agents.agents.base.factory import AgentWrapper
from debate_agents.schema.topic_extract_schema import TopicExtractSchema
from debate_agents.tools.memory_tools import refresh_memory, write_json_direct

async def topic_extractor_node(state):
    refresh_memory()
    agent = AgentWrapper(TopicExtractSchema, "topic_extract_agent.md", "TopicExtractAgent")
    # Include round in context for the agent
    context = f"User Input: {state['user_input']}\nCurrent Round: 1"
    result = await agent.invoke(context)
    topic = result.topic if hasattr(result, "topic") else str(result)
    # The prompt expects the topic to be saved to shared_memory.json
    await write_json_direct("shared_memory.json", topic, "TopicExtractAgent")
    return {"topic": topic, "round": 1, "current_team": "pros"}
