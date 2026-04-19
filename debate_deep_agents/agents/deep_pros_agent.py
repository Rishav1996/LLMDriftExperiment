import os
from deepagents import create_deep_agent
from deepagents.middleware.subagents import SubAgent
from debate_deep_agents.config.config import model

def create_pros_deep_agent():
    """
    Creates a Deep Agent for the Pros team.
    """
    prompt_path = os.path.join("debate_deep_agents", "prompts", "pros", "agent.md")
    persona_prompt_path = os.path.join("debate_deep_agents", "prompts", "pros", "persona_agent.md")
    thinking_prompt_path = os.path.join("debate_deep_agents", "prompts", "pros", "thinking_agent.md")
    critique_prompt_path = os.path.join("debate_deep_agents", "prompts", "pros", "critique_agent.md")
    
    with open(prompt_path, "r") as f:
        system_instruction = f.read()
    with open(persona_prompt_path, "r") as f:
        persona_instruction = f.read()
    with open(thinking_prompt_path, "r") as f:
        thinking_instruction = f.read()
    with open(critique_prompt_path, "r") as f:
        critique_instruction = f.read()

    # Define subagents
    subagents = [
        SubAgent(name="ProsPersonaAgent", description="Designs adversarial persona.", system_prompt=persona_instruction),
        SubAgent(name="ProsThinkingAgent", description="Tactical strategy planning.", system_prompt=thinking_instruction),
        SubAgent(name="ProsCritiqueAgent", description="Evaluates argument quality.", system_prompt=critique_instruction)
    ]
    
    agent = create_deep_agent(
        model=model,
        system_prompt=system_instruction,
        subagents=subagents
    )
    return agent
