from debate_agents.agents.base.factory import AgentWrapper
from debate_agents.schema.cons_schema import PersonaSchema, ThinkingSchema, CritiqueSchema
from debate_agents.tools.memory_tools import write_json_direct, read_json_direct

async def cons_persona_node(state):
    agent = AgentWrapper(PersonaSchema, "cons/persona_agent.md", "ConsPersonaAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ConsPersonaAgent")
    context = f"Topic: {state['topic']}\nShared Memory: {shared_memory}"
    result = await agent.invoke(context)
    await write_json_direct("persona.json", result.model_dump(), "ConsPersonaAgent")
    return {"last_output": result, "cons_iteration": state.get("cons_iteration", 0) + 1}

async def cons_thinking_node(state):
    agent = AgentWrapper(ThinkingSchema, "cons/thinking_agent.md", "ConsThinkingAgent")
    persona = await read_json_direct("persona.json", "ConsThinkingAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ConsThinkingAgent")
    context = f"Topic: {state['topic']}\nRound: {state['round']}\nPersona: {persona}\nShared Memory: {shared_memory}"
    result = await agent.invoke(context)
    await write_json_direct("thinking.json", result.model_dump(), "ConsThinkingAgent")
    return {"last_output": result}

async def cons_critique_node(state):
    agent = AgentWrapper(CritiqueSchema, "cons/critique_agent.md", "ConsCritiqueAgent")
    thinking = await read_json_direct("thinking.json", "ConsCritiqueAgent")
    persona = await read_json_direct("persona.json", "ConsCritiqueAgent")
    context = f"Thinking: {thinking}\nPersona: {persona}"
    result = await agent.invoke(context)
    await write_json_direct("critique.json", result.model_dump(), "ConsCritiqueAgent")
    
    is_approved = result.approved
    if is_approved:
        latest_thinking = await read_json_direct("thinking.json", "ConsThinkingAgent")
        if latest_thinking:
            content = latest_thinking[-1]["content"]
            answer = content.get("formulated_answer")
            if answer:
                await write_json_direct("shared_memory.json", answer, "ConsCritiqueAgent")
                
    return {"is_approved": is_approved, "last_output": result}
