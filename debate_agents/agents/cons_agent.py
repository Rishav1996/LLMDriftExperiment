from debate_agents.agents.base.factory import AgentWrapper
from debate_agents.schema.cons_schema import PersonaSchema, ThinkingSchema, CritiqueSchema
from debate_agents.tools.memory_tools import write_json_direct, read_json_direct
from typing import Any, Dict

async def cons_persona_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates the Con agent's persona.

    Args:
        state (Dict[str, Any]): The current LangGraph debate state.

    Returns:
        Dict[str, Any]: The updated state including the last output and iteration count.
    """
    print(f"[ConsPersonaAgent] Running for Round {state['round']}...")
    agent = AgentWrapper(PersonaSchema, "cons/persona_agent.md", "ConsPersonaAgent")
    
    # Check if we already have a persona
    existing_personas = await read_json_direct("persona.json", "ConsPersonaAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ConsPersonaAgent")
    
    # If round > 1, pass the existing persona and shared memory for evaluation
    if state['round'] > 1 and existing_personas:
        context = f"Topic: {state['topic']}\nExisting Persona: {existing_personas[-1]['content']}\nOpponent's Last Argument (Shared Memory): {shared_memory[-1]['content'] if shared_memory else 'None'}"
    else:
        context = f"Topic: {state['topic']}"

    result = await agent.invoke(context, state['round'])
    
    if hasattr(result, 'skip_persona_generation') and result.skip_persona_generation:
        print("[ConsPersonaAgent] Agent chose to skip persona generation.")
    else:
        await write_json_direct("persona.json", result.model_dump(), "ConsPersonaAgent", state['round'])
        
    return {"last_output": result, "cons_iteration": state.get("cons_iteration", 0) + 1}

async def cons_thinking_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates the Con agent's thinking process.

    Args:
        state (Dict[str, Any]): The current LangGraph debate state.

    Returns:
        Dict[str, Any]: The updated state including the last output.
    """
    print(f"[ConsThinkingAgent] Running for Round {state['round']}...")
    agent = AgentWrapper(ThinkingSchema, "cons/thinking_agent.md", "ConsThinkingAgent")
    persona = await read_json_direct("persona.json", "ConsThinkingAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ConsThinkingAgent")
    context = f"Topic: {state['topic']}\nRound: {state['round']}\nPersona: {persona}\nShared Memory: {shared_memory}"
    result = await agent.invoke(context, state['round'])
    await write_json_direct("thinking.json", result.model_dump(), "ConsThinkingAgent", state['round'])
    return {"last_output": result}

async def cons_critique_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Critiques the Con agent's thinking process.

    Args:
        state (Dict[str, Any]): The current LangGraph debate state.

    Returns:
        Dict[str, Any]: The updated state including approval status and last output.
    """
    print(f"[ConsCritiqueAgent] Running for Round {state['round']}...")
    agent = AgentWrapper(CritiqueSchema, "cons/critique_agent.md", "ConsCritiqueAgent")
    thinking = await read_json_direct("thinking.json", "ConsCritiqueAgent")
    persona = await read_json_direct("persona.json", "ConsCritiqueAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ConsCritiqueAgent")
    
    # Pass opponent's last argument for evaluation
    opponent_argument = shared_memory[-1]['content'] if shared_memory else "None"
    context = f"Round: {state['round']}\nThinking: {thinking}\nPersona: {persona}\nOpponent's Last Argument: {opponent_argument}"
    
    result = await agent.invoke(context, state['round'])
    await write_json_direct("critique.json", result.model_dump(), "ConsCritiqueAgent", state['round'])
    
    is_approved = result.approved
    if is_approved:
        latest_thinking = await read_json_direct("thinking.json", "ConsThinkingAgent")
        if latest_thinking:
            content = latest_thinking[-1]["content"]
            answer = content.get("formulated_answer")
            if answer:
                await write_json_direct("shared_memory.json", answer, "ConsCritiqueAgent", state['round'])
                
    return {"is_approved": is_approved, "last_output": result}
