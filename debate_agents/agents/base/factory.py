from langchain_google_genai import ChatGoogleGenerativeAI
from debate_agents.agents.base.utils import load_prompt
from debate_agents.config import GEMINI_MODEL_ADAPTER
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Any

def get_model(temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    """
    Configures and returns a Gemini model instance.

    Args:
        temperature (float): The sampling temperature. Defaults to 0.7.

    Returns:
        ChatGoogleGenerativeAI: An instance of the Gemini model.
    """
    model_name = GEMINI_MODEL_ADAPTER
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

class AgentWrapper:
    """
    A wrapper class for LLM agents that manages instruction loading, 
    model initialization, and invocation with structured output.
    """
    def __init__(self, schema: Any, instruction_path: str, name: str, temperature: float = 0.7):
        """
        Initializes the AgentWrapper.

        Args:
            schema (Any): The Pydantic schema for structured output.
            instruction_path (str): Path to the system instruction markdown file.
            name (str): The name of the agent.
            temperature (float): The sampling temperature. Defaults to 0.7.
        """
        self.name = name
        self.model = get_model(temperature=temperature)
        self.instruction = load_prompt(instruction_path)
        self.structured_model = self.model.with_structured_output(schema)

    async def invoke(self, state_str: str, round_num: int) -> Any:
        """
        Invokes the agent with the provided state and current round context.

        Args:
            state_str (str): The current context string.
            round_num (int): The current debate round number.

        Returns:
            Any: The structured output from the agent.
        """
        # LangChain approach
        messages = [
            SystemMessage(content=self.instruction),
            HumanMessage(content=f"Round: {round_num}\nCurrent Context and Memory:\n{state_str}")
        ]
        return await self.structured_model.ainvoke(messages)
