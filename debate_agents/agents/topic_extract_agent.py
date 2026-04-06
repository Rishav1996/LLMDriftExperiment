import os
from google.adk.agents import LlmAgent
from debate_agents.config import GEMINI_MODEL_ADAPTER # Import added
from debate_agents.tools.memory_tools import get_write_markdown_tool, refresh_memory
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

async def refresh_memory_callback(callback_context: CallbackContext) -> None:
    """Clears all memory folders before a new topic is extracted and debated."""
    refresh_memory()

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_topic_extract_agent():
    return LlmAgent(
        name="TopicExtractAgent",
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt("topic_extract_agent.md"),
        description="Extracts the debate topic from user input.",
        output_key="topic",
        include_contents='none',
        tools=[get_write_markdown_tool()],
        before_agent_callback=refresh_memory_callback,
    )
