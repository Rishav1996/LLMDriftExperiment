from langchain_google_genai import ChatGoogleGenerativeAI
from debate_agents.agents.base.utils import load_prompt
from debate_agents.config import GEMINI_MODEL_ADAPTER
from langchain_core.messages import SystemMessage, HumanMessage

def get_model(temperature=0.7):
    # Reverting to ChatGoogleGenerativeAI as requested.
    model_name = GEMINI_MODEL_ADAPTER
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

class AgentWrapper:
    def __init__(self, schema, instruction_path, name, temperature=0.7):
        self.name = name
        self.model = get_model(temperature=temperature)
        self.instruction = load_prompt(instruction_path)
        self.structured_model = self.model.with_structured_output(schema)

    async def invoke(self, state_str: str, round_num: int):
        # LangChain approach
        messages = [
            SystemMessage(content=self.instruction),
            HumanMessage(content=f"Round: {round_num}\nCurrent Context and Memory:\n{state_str}")
        ]
        return await self.structured_model.ainvoke(messages)
