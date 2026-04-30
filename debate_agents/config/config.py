"""
Configuration module for the debate simulation.
Initializes the chat model with specific parameters.
"""
from langchain.chat_models import init_chat_model

# pylint: disable=import-error
model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite-preview",
    max_retries=10,
    temperature=1,
    max_tokens=4096,
    thinking_budget=2048,
    include_thoughts=True
)
