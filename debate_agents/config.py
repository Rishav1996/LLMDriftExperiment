# Configuration for the LLM Drift Experiment
from google.adk.models import Gemini
from google.genai import types # Import added

GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
MAX_ROUNDS = 3

# Global configuration for LLM content generation, including retry options
GLOBAL_GENERATE_CONTENT_CONFIG = types.GenerateContentConfig(
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(initial_delay=30, attempts=5) # Updated initial_delay and attempts
    )
)
