from google.adk.agents import LlmAgent

from debate_agents.config import GEMINI_MODEL_ADAPTER
from debate_agents.tools.memory_tools import get_read_markdown_tool, get_write_markdown_tool
from debate_agents.tools.cons.strategy_tool import get_cons_strategy_tool
from debate_agents.tools.cons.persona_tool import get_cons_persona_tool
from debate_agents.tools.cons.critique_tool import get_cons_critique_tool
from debate_agents.schema.cons.agent_schema import AgentSchema
from debate_agents.agents.utils import load_prompt

def get_cons_agent():
    """Factory function for the ConsRootAgent."""
    return LlmAgent(
        name="ConsAgent",
        model=GEMINI_MODEL_ADAPTER,
        instruction=load_prompt("cons/agent.md"), 
        description="Generates refined arguments against using persona, tactical, critique, and memory tools.",
        tools=[
            get_cons_strategy_tool(), 
            get_cons_persona_tool(), 
            get_cons_critique_tool(),
            get_read_markdown_tool(),
            get_write_markdown_tool()
        ],
        output_key="cons_argument", 
        include_contents='none',
        output_schema=AgentSchema
    )
