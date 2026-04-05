import os
from google.adk.agents import LlmAgent
from debate_agents.config import GEMINI_MODEL
from debate_agents.tools.strategy_tool import get_strategy_tool
from debate_agents.tools.persona_tool import get_persona_tool
from debate_agents.tools.critique_tool import get_critique_tool
from debate_agents.tools.memory_tools import get_read_markdown_tool, get_write_markdown_tool

def load_prompt(filename: str) -> str:
    path = os.path.join("debate_agents", "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_pros_agent():
    return LlmAgent(
        name="ProsAgent",
        model=GEMINI_MODEL,
        instruction=load_prompt("pros_agent.md"),
        description="Generates refined arguments in favor using persona, tactical, critique, and memory tools.",
        tools=[
            get_strategy_tool(), 
            get_persona_tool(), 
            get_critique_tool(),
            get_read_markdown_tool(),
            get_write_markdown_tool()
        ],
        # Changed output_key to final_argument as output is saved to shared_memory.md
        output_key="final_argument", 
        include_contents='none'
    )
