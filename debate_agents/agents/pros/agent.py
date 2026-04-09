from google.adk.agents import LlmAgent

from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_read_markdown_tool, get_write_markdown_tool
from debate_agents.tools.pros.strategy_tool import get_pros_strategy_tool
from debate_agents.tools.pros.persona_tool import get_pros_persona_tool
from debate_agents.tools.pros.critique_tool import get_pros_critique_tool
from debate_agents.schema.pros.agent_schema import AgentSchema
from debate_agents.agents.utils import load_prompt

def get_pros_agent():
    """Factory function for the ProsRootAgent."""
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
        output_schema=AgentSchema
    )
