from debate_agents_langgraph.agents.base.factory import AgentWrapper
from debate_agents_langgraph.schema.pros_schema import PersonaSchema, ThinkingSchema, CritiqueSchema
from debate_agents_langgraph.tools.memory_tools import write_json_direct, read_json_direct

async def pros_persona_node(state):
    agent = AgentWrapper(PersonaSchema, "pros/persona_agent.md", "ProsPersonaAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ProsPersonaAgent")
    context = f"Topic: {state['topic']}\nShared Memory: {shared_memory}"
    result = await agent.invoke(context)
    await write_json_direct("persona.json", result.model_dump(), "ProsPersonaAgent")
    return {"last_output": result, "pros_iteration": state.get("pros_iteration", 0) + 1}

async def pros_thinking_node(state):
    agent = AgentWrapper(ThinkingSchema, "pros/thinking_agent.md", "ProsThinkingAgent")
    persona = await read_json_direct("persona.json", "ProsThinkingAgent")
    shared_memory = await read_json_direct("shared_memory.json", "ProsThinkingAgent")
    context = f"Topic: {state['topic']}\nPersona: {persona}\nShared Memory: {shared_memory}"
    result = await agent.invoke(context)
    await write_json_direct("thinking.json", result.model_dump(), "ProsThinkingAgent")
    return {"last_output": result}

async def pros_critique_node(state):
    agent = AgentWrapper(CritiqueSchema, "pros/critique_agent.md", "ProsCritiqueAgent")
    thinking = await read_json_direct("thinking.json", "ProsCritiqueAgent")
    persona = await read_json_direct("persona.json", "ProsCritiqueAgent")
    context = f"Round: {state['round']}\nThinking: {thinking}\nPersona: {persona}"
    result = await agent.invoke(context)
    await write_json_direct("critique.json", result.model_dump(), "ProsCritiqueAgent")
    
    is_approved = result.approved
    if is_approved:
        latest_thinking = await read_json_direct("thinking.json", "ProsThinkingAgent")
        if latest_thinking:
            # data is a list of {"agent": agent_name, "content": content}
            content = latest_thinking[-1]["content"]
            answer = content.get("formulated_answer")
            if answer:
                await write_json_direct("shared_memory.json", answer, "ProsCritiqueAgent")
                
    return {"is_approved": is_approved, "last_output": result}
