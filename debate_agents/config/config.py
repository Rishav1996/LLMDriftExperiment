from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite-preview",
    max_retries=10,
    temperature=1,
    max_tokens=8192,
    thinking_budget=2048,
    include_thoughts=True
)
