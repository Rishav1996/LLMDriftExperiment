from debate_agents.tools.memory_tools import write_json_direct

async def save_persona_callback(callback_context):
    await write_json_direct("persona.json", callback_context.state.get("pros_persona"), "ProsPersonaAgent")

async def save_thinking_callback(callback_context):
    await write_json_direct("thinking.json", callback_context.state.get("pros_thinking"), "ProsThinkingAgent")

async def save_critique_callback(callback_context):
    await write_json_direct("critique.json", callback_context.state.get("pros_critique"), "ProsCritiqueAgent")
