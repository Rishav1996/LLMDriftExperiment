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
