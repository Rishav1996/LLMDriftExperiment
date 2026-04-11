import time
from google.adk.agents import LlmAgent
from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_read_json_tool, get_write_json_tool
from debate_agents.agents.base.utils import load_prompt

async def sleep_callback(callback_context):
    """Callback to sleep for 10 seconds after an agent call."""
    time.sleep(10)

def create_base_agent(name, instruction_path, description, output_key, schema, tools=None, sub_agents=None, planner=None, callback=None):
    """Helper to create a standardized LlmAgent."""
    agent = LlmAgent(
        name=name,
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt(instruction_path),
        description=description,
        output_key=output_key,
        include_contents='none',
        output_schema=schema,
        planner=planner,
        sub_agents=sub_agents or [],
        tools=tools or []
    )
    
    # Wrap the existing callback to include the sleep
    async def combined_callback(callback_context):
        if callback:
            await callback(callback_context)
        await sleep_callback(callback_context)
        
    agent.after_agent_callback = combined_callback
    return agent
