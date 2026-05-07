"""
Configuration module for the debate simulation.
Initializes the chat model with specific parameters.
"""
from langchain.chat_models import init_chat_model

# Central configuration for the debate simulation
CONFIG = {
    "version": "v8",  # Increment this for different logic iterations
    "model_name": "google_genai:gemini-3.1-pro-preview",
    "temperature": 1,
    "max_tokens": 4096,
    "max_retries": 10,
    "thinking_budget": 2048
}

# Initialize the chat model using the CONFIG dictionary
model = init_chat_model(
    model=CONFIG["model_name"],
    max_retries=CONFIG["max_retries"],
    temperature=CONFIG["temperature"],
    max_tokens=CONFIG["max_tokens"],
    thinking_budget=CONFIG["thinking_budget"],
    include_thoughts=True
)
