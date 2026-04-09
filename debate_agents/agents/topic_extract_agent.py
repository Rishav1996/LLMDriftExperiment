from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext

from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_write_json_tool, refresh_memory
from debate_agents.schema.topic_extract_schema import TopicExtractSchema
from debate_agents.agents.utils import load_prompt

async def refresh_memory_callback(callback_context: CallbackContext) -> None:
    """Clears all memory folders before a new topic is extracted and debated."""
    refresh_memory()

def get_topic_extract_agent():
    """Factory function for the TopicExtractAgent."""
    return LlmAgent(
        name="TopicExtractAgent",
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt("topic_extract_agent.md"),
        description="Extracts the debate topic from user input.",
        output_key="topic",
        include_contents='none',
        tools=[get_write_json_tool()],
        before_agent_callback=refresh_memory_callback,
        output_schema=TopicExtractSchema
    )
