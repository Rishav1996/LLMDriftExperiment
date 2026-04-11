from debate_agents.agents.base.factory import AgentWrapper
from debate_agents.schema.pros_schema import PersonaSchema, ThinkingSchema, CritiqueSchema
from debate_agents.tools.memory_tools import write_json_direct, read_json_direct
from typing import Any, Dict

async def pros_persona_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates the Pro agent's persona.

    Args:
        state (Dict[str, Any]): The current LangGraph debate state.

    Returns:
        Dict[str, Any]: The updated state including the last output and iteration count.
    """
    print(f"[ProsPersonaAgent] Running for Round {state['round']}...")
    agent = AgentWrapper(PersonaSchema, "pros/persona_agent.md", "ProsPersonaAgent")
    
    # Check if we already have a persona
    existing_personas = await read_json_direct("persona.json", "ProsPersonaAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ProsPersonaAgent")
    
    # If round > 1, pass the existing persona and shared memory for evaluation
    if state['round'] > 1 and existing_personas:
        context = f"Topic: {state['topic']}\nExisting Persona: {existing_personas[-1]['content']}\nOpponent's Last Argument (Shared Memory): {shared_memory[-1]['content'] if shared_memory else 'None'}"
    else:
        context = f"Topic: {state['topic']}"

    result = await agent.invoke(context, state['round'])
    
    if hasattr(result, 'skip_persona_generation') and result.skip_persona_generation:
        print("[ProsPersonaAgent] Agent chose to skip persona generation.")
        # Do not overwrite persona.json
    else:
        await write_json_direct("persona.json", result.model_dump(), "ProsPersonaAgent", state['round'])
        
    return {"last_output": result, "pros_iteration": state.get("pros_iteration", 0) + 1}

async def pros_thinking_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates the Pro agent's thinking process.

    Args:
        state (Dict[str, Any]): The current LangGraph debate state.

    Returns:
        Dict[str, Any]: The updated state including the last output.
    """
    print(f"[ProsThinkingAgent] Running for Round {state['round']}...")
    agent = AgentWrapper(ThinkingSchema, "pros/thinking_agent.md", "ProsThinkingAgent")
    persona = await read_json_direct("persona.json", "ProsThinkingAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ProsThinkingAgent")
    context = f"Topic: {state['topic']}\nPersona: {persona}\nShared Memory: {shared_memory}"
    result = await agent.invoke(context, state['round'])
    await write_json_direct("thinking.json", result.model_dump(), "ProsThinkingAgent", state['round'])
    return {"last_output": result}

async def pros_critique_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Critiques the Pro agent's thinking process.

    Args:
        state (Dict[str, Any]): The current LangGraph debate state.

    Returns:
        Dict[str, Any]: The updated state including approval status and last output.
    """
    print(f"[ProsCritiqueAgent] Running for Round {state['round']}...")
    agent = AgentWrapper(CritiqueSchema, "pros/critique_agent.md", "ProsCritiqueAgent")
    thinking = await read_json_direct("thinking.json", "ProsCritiqueAgent")
    persona = await read_json_direct("persona.json", "ProsCritiqueAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ProsCritiqueAgent")
    
    # Pass opponent's last argument for evaluation
    opponent_argument = shared_memory[-1]['content'] if shared_memory else "None"
    context = f"Round: {state['round']}\nThinking: {thinking}\nPersona: {persona}\nOpponent's Last Argument: {opponent_argument}"
    
    result = await agent.invoke(context, state['round'])
    await write_json_direct("critique.json", result.model_dump(), "ProsCritiqueAgent", state['round'])
    
    is_approved = result.approved
    if is_approved:
        latest_thinking = await read_json_direct("thinking.json", "ProsThinkingAgent")
        if latest_thinking:
            # data is a list of {"agent": agent_name, "content": content}
            content = latest_thinking[-1]["content"]
            answer = content.get("formulated_answer")
            if answer:
                await write_json_direct("shared_memory.json", answer, "ProsCritiqueAgent", state['round'])
                
    return {"is_approved": is_approved, "last_output": result}
