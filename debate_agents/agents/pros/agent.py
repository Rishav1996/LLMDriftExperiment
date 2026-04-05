import os
from google.adk.agents import LlmAgent
from debate_agents.config import GEMINI_MODEL, GLOBAL_GENERATE_CONTENT_CONFIG
# Updated import paths for tools to use pros versions
from debate_agents.tools.pros.strategy_tool import get_strategy_tool
from debate_agents.tools.pros.persona_tool import get_persona_tool
from debate_agents.tools.pros.critique_tool import get_critique_tool
from debate_agents.tools.memory_tools import get_read_markdown_tool, get_write_markdown_tool

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_pros_agent():
    return LlmAgent(
        name="ProsAgent",
        model=GEMINI_MODEL,
        instruction=load_prompt("pros/agent.md"), # Updated prompt path
        description="Generates refined arguments in favor using persona, tactical, critique, and memory tools.",
        tools=[
            get_strategy_tool(), 
            get_persona_tool(), 
            get_critique_tool(),
            get_read_markdown_tool(),
            get_write_markdown_tool()
        ],
        output_key="shared_memory", # Changed to shared_memory as output is saved there
        include_contents='none',
        generate_content_config=GLOBAL_GENERATE_CONTENT_CONFIG 
    )
