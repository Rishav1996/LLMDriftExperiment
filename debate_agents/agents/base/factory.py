from google.adk.agents import LlmAgent
from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.agents.base.utils import load_prompt

def create_base_agent(name, instruction_path, description, output_key, schema, tools=None, sub_agents=None, planner=None, callback=None):
    """Helper to create a standardized LlmAgent."""
    agent = LlmAgent(
        name=name,
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt(instruction_path),
        description=description,
        output_key=output_key,
        output_schema=schema,
        planner=planner,
        sub_agents=sub_agents or [],
        tools=tools or []
    )
    if callback:
        agent.after_agent_callback = callback
    return agent
