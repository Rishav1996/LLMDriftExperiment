import os
from deepagents import create_deep_agent
from deepagents.middleware.subagents import SubAgent
from debate_deep_agents.config.config import model
from debate_deep_agents.tools.memory_tools import create_memory_tools
from debate_deep_agents.schema.topic_extract_schema import TopicExtractSchema

def create_topic_extractor_deep_agent():
    """
    Creates a Deep Agent for topic extraction.
    """
    prompt_path = os.path.join("debate_deep_agents", "prompts", "topic_extract_agent.md")
    with open(prompt_path, "r") as f:
        system_instruction = f.read()

    # Define the subagent
    subagent = SubAgent(
        name="topic-extractor",
        description="Extracts and refines the debate topic from user input.",
        system_prompt=system_instruction
    )
    
    # Create memory tools
    tools = create_memory_tools("TopicExtractAgent")
    
    agent = create_deep_agent(
        model=model,
        subagents=[subagent],
        tools=tools,
        response_format=TopicExtractSchema,
        debug=True
    )
    return agent
