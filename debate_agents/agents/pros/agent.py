import os
from google.adk.agents import LlmAgent
from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_read_markdown_tool, get_write_markdown_tool
# Updated import paths and function names for pros versions
from debate_agents.tools.pros.strategy_tool import get_pros_strategy_tool
from debate_agents.tools.pros.persona_tool import get_pros_persona_tool
from debate_agents.tools.pros.critique_tool import get_pros_critique_tool

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_pros_agent():
    return LlmAgent(
        name="ProsAgent",
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt("pros/agent.md"), 
        description="Generates refined arguments in favor using persona, tactical, critique, and memory tools.",
        tools=[
            get_pros_strategy_tool(), 
            get_pros_persona_tool(), 
            get_pros_critique_tool(),
            get_read_markdown_tool(),
            get_write_markdown_tool()
        ],
        output_key="pros_argument", 
        include_contents='none',
    )
