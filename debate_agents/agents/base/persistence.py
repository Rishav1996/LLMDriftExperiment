from debate_agents.tools.memory_tools import write_json_direct

async def save_persona_callback(callback_context):
    team = "pros_memory" if "Pros" in callback_context.agent_name else "cons_memory"
    await write_json_direct("persona.json", callback_context.state.get(f"{team.split('_')[0]}_persona"), callback_context.agent_name)

async def save_thinking_callback(callback_context):
    team = "pros_memory" if "Pros" in callback_context.agent_name else "cons_memory"
    await write_json_direct("thinking.json", callback_context.state.get(f"{team.split('_')[0]}_thinking"), callback_context.agent_name)

async def save_critique_callback(callback_context):
    team = "pros_memory" if "Pros" in callback_context.agent_name else "cons_memory"
    await write_json_direct("critique.json", callback_context.state.get(f"{team.split('_')[0]}_critique"), callback_context.agent_name)

async def save_shared_memory_callback(callback_context):
    """Saves the approved formulated_answer to shared_memory.json."""
    prefix = "pros" if "Pros" in callback_context.agent_name else "cons"
    thinking_data = callback_context.state.get(f"{prefix}_thinking")
    
    # Extract the formulated_answer
    answer = None
    if isinstance(thinking_data, dict):
        answer = thinking_data.get("formulated_answer")
    elif hasattr(thinking_data, "formulated_answer"):
        answer = thinking_data.formulated_answer
        
    if answer:
        await write_json_direct("shared_memory.json", answer, callback_context.agent_name)
