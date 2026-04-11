import time
from langchain_google_genai import ChatGoogleGenerativeAI
from debate_agents.agents.base.utils import load_prompt
from debate_agents.config import GEMINI_MODEL_ADAPTER
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Any
from debate_agents.tools.mlflow_logger import log_agent_interaction
import logging

# Set up logging for retries
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    model initialization, and invocation with structured output, including retries and MLflow logging.
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

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        before_sleep=lambda retry_state: logger.info(f"Retrying {self.name} due to error: {retry_state.outcome.exception()}"),
        reraise=True
    )
    async def invoke(self, state_str: str, round_num: int) -> Any:
        """
        Invokes the agent with retries for API and parsing failures, and logs metrics to MLflow.

        Args:
            state_str (str): The current context string.
            round_num (int): The current debate round number.

        Returns:
            Any: The structured output from the agent.
        """
        messages = [
            SystemMessage(content=self.instruction),
            HumanMessage(content=f"Round: {round_num}\nCurrent Context and Memory:\n{state_str}")
        ]
        
        start_time = time.perf_counter()
        
        # Use ainvoke directly and track token usage from metadata
        response = await self.model.ainvoke(messages)
        result = await self.structured_model.ainvoke(messages)
        
        end_time = time.perf_counter()
        latency = end_time - start_time
        
        # Extract token usage from the response metadata
        token_usage = response.response_metadata.get("usage_metadata", {})
        
        # Log to MLflow
        log_agent_interaction(self.name, round_num, token_usage, latency)
        
        return result
