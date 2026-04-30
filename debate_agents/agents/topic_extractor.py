"""
This module initializes the topic extractor agent.
It refines raw user input into a formal debate proposition.
"""
import os
from langchain_core.prompts import ChatPromptTemplate

# pylint: disable=import-error
from debate_agents.config.config import model
from debate_agents.schema.topic_extract_schema import TopicExtractSchema

def create_topic_extractor_agent():
    """
    Creates a LangChain-based topic extractor with a structured output schema.
    """
    prompt_path = os.path.join("debate_agents", "prompts", "topic_extract_agent.md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        instruction = f.read()

    prompt = ChatPromptTemplate.from_messages([
        ("system", instruction),
        ("user", "Extract and refine the topic from: {user_input}")
    ])

    # Simple chain with structured output
    chain = prompt | model.with_structured_output(TopicExtractSchema)

    return chain
