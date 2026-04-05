from google.adk.agents.callback_context import CallbackContext

async def initialize_debate_state(callback_context: CallbackContext) -> None:
    """Ensures mandatory state variables are initialized, capturing topic from user input and shared memory."""
    # Check if topic is already in state
    if "topic" not in callback_context.state:
        # Try to extract topic from the initial user message
        user_input = ""
        inv_ctx = getattr(callback_context, "_invocation_context", None)
        if inv_ctx and inv_ctx.new_message and inv_ctx.new_message.parts:
            user_input = "".join([p.text for p in inv_ctx.new_message.parts if p.text]).strip()
        
        if user_input:
            callback_context.state["topic"] = user_input
        else:
            # Fallback default topic
            callback_context.state["topic"] = "The impact of Artificial Intelligence on the future of work"
            
    # Initialize shared_memory if it doesn't exist, otherwise retain it.
    if "shared_memory" not in callback_context.state:
        callback_context.state["shared_memory"] = f"Debate initiated on topic: {callback_context.state.get('topic', 'undefined topic')}

"
