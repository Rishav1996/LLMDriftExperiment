from google.adk.agents.callback_context import CallbackContext
from debate_agents.tools.memory_tools import refresh_memory
from debate_agents.schema.topic_extract_schema import TopicExtractSchema
from debate_agents.agents.factory import create_base_agent

async def refresh_memory_callback(callback_context: CallbackContext) -> None:
    refresh_memory()

def get_topic_extract_agent():
    return create_base_agent(
        name="TopicExtractAgent",
        instruction_path="topic_extract_agent.md",
        description="Extracts the debate topic from user input.",
        output_key="topic",
        schema=TopicExtractSchema,
        callback=refresh_memory_callback
    )
