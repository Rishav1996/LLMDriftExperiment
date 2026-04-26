from langchain.chat_models import init_chat_model

# --- Active Model Selection ---
# Using Gemini 2.0 Flash Thinking for enhanced reasoning (Thinking Planner)
model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite-preview",
    max_retries=10,
    temperature=1,
    max_tokens=4096,
    thinking_budget=2048,
    include_thoughts=True
)
