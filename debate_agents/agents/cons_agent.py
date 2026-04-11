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
    agent = AgentWrapper(PersonaSchema, "cons/persona_agent.md", "ConsPersonaAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ConsPersonaAgent")
    context = f"Topic: {state['topic']}\nShared Memory: {shared_memory}"
    result = await agent.invoke(context, state['round'])
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
    agent = AgentWrapper(CritiqueSchema, "cons/critique_agent.md", "ConsCritiqueAgent")
    thinking = await read_json_direct("thinking.json", "ConsCritiqueAgent")
    persona = await read_json_direct("persona.json", "ConsCritiqueAgent")
    context = f"Thinking: {thinking}\nPersona: {persona}"
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
