import os
from deepagents import create_deep_agent
from deepagents.middleware.subagents import SubAgent
from debate_agents.config import GEMINI_MODEL_ADAPTER

def create_topic_extractor_deep_agent():
    """
    Creates a Deep Agent for topic extraction.
    """
    prompt_path = os.path.join("debate_deep_agents", "prompts", "topic_extract_agent.md")
    with open(prompt_path, "r") as f:
        system_instruction = f.read()

    # Define the subagent (though for this simple task we might just use the main agent)
    # The topic extractor is specialized, so we define it as a subagent to be called.
    subagent = SubAgent(
        name="topic-extractor",
        description="Extracts and refines the debate topic from user input.",
        system_prompt=system_instruction
    )
    
    agent = create_deep_agent(
        model=GEMINI_MODEL_ADAPTER,
        subagents=[subagent]
    )
    return agent
