from google.adk.agents.callback_context import CallbackContext
from debate_agents.tools.memory_tools import refresh_memory, get_write_json_tool
from debate_agents.schema.topic_extract_schema import TopicExtractSchema
from debate_agents.agents.base.factory import create_base_agent

async def refresh_memory_before_callback(callback_context: CallbackContext) -> None:
    """Clears the memory directory before the agent starts."""
    refresh_memory()

def get_topic_extract_agent():
    agent = create_base_agent(
        name="TopicExtractAgent",
        instruction_path="topic_extract_agent.md",
        description="Extracts the debate topic from user input.",
        output_key="topic",
        schema=TopicExtractSchema,
        tools=[get_write_json_tool()],
        callback=None
    )
    # Set before_agent_callback directly
    agent.before_agent_callback = refresh_memory_before_callback
    return agent
