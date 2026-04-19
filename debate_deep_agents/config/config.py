from langchain.chat_models import init_chat_model

# --- Active Model Selection ---
model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite-preview",
    max_retries=10
)
