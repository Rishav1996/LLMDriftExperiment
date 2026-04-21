import os
from debate_deep_agents.config.config import model
from debate_deep_agents.tools.memory_tools import create_memory_tools
from debate_deep_agents.schema.topic_extract_schema import TopicExtractSchema
from langchain_core.prompts import ChatPromptTemplate

def create_topic_extractor_agent():
    """
    Creates a simple LangChain-based topic extractor.
    """
    prompt_path = os.path.join("debate_deep_agents", "prompts", "topic_extract_agent.md")
    with open(prompt_path, "r") as f:
        instruction = f.read()

    prompt = ChatPromptTemplate.from_messages([("system", instruction), ("user", "Extract and refine the topic from: {user_input}")])
    
    # Simple chain with structured output
    chain = prompt | model.with_structured_output(TopicExtractSchema)
    
    return chain
