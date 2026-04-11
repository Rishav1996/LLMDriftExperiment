from langchain_google_genai import ChatGoogleGenerativeAI
from debate_agents_langgraph.agents.base.utils import load_prompt
from debate_agents_langgraph.config import GEMINI_MODEL_ADAPTER
from langchain_core.messages import SystemMessage, HumanMessage
import os

def get_model(temperature=0.7):
    model_name = GEMINI_MODEL_ID = "gemini-1.5-flash"
    if isinstance(GEMINI_MODEL_ADAPTER, str):
        model_name = GEMINI_MODEL_ADAPTER
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

class AgentWrapper:
    def __init__(self, schema, instruction_path, name, temperature=0.7):
        self.name = name
        self.model = get_model(temperature=temperature)
        self.instruction = load_prompt(instruction_path)
        self.structured_model = self.model.with_structured_output(schema)

    async def invoke(self, state_str: str):
        # LangChain approach
        messages = [
            SystemMessage(content=self.instruction),
            HumanMessage(content=f"Current Context and Memory:\n{state_str}")
        ]
        return await self.structured_model.ainvoke(messages)
