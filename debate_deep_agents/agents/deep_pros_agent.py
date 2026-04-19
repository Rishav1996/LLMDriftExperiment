import os
from deepagents import create_deep_agent, CompiledSubAgent
from debate_deep_agents.config.config import model
from debate_deep_agents.schema.pros_schema import AgentSchema, PersonaSchema, ThinkingSchema, CritiqueSchema
from debate_deep_agents.tools.memory_tools import create_memory_tools

def create_pros_deep_agent():
    """
    Creates a Deep Agent for the Pros team with structured subagents.
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

    # Create common memory tools
    tools = create_memory_tools("ProsAgent")

    # Define subagents as CompiledSubAgents to support schemas
    subagents = [
        CompiledSubAgent(
            name="ProsPersonaAgent",
            description="Designs adversarial persona based on debate history.",
            runnable=create_deep_agent(
                model=model,
                system_prompt=persona_instruction,
                tools=tools,
                response_format=PersonaSchema,
                name="ProsPersonaAgent"
            )
        ),
        CompiledSubAgent(
            name="ProsThinkingAgent",
            description="Tactical strategy planning and argument drafting.",
            runnable=create_deep_agent(
                model=model,
                system_prompt=thinking_instruction,
                tools=tools,
                response_format=ThinkingSchema,
                name="ProsThinkingAgent"
            )
        ),
        CompiledSubAgent(
            name="ProsCritiqueAgent",
            description="Evaluates argument quality and logical consistency.",
            runnable=create_deep_agent(
                model=model,
                system_prompt=critique_instruction,
                tools=tools,
                response_format=CritiqueSchema,
                name="ProsCritiqueAgent"
            )
        )
    ]
    
    agent = create_deep_agent(
        model=model,
        system_prompt=system_instruction,
        subagents=subagents,
        tools=tools,
        response_format=AgentSchema,
        debug=True
    )
    return agent
