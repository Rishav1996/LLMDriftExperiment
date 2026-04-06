# Configuration for the LLM Drift Experiment
from google.adk.models.google_llm import Gemini # Correct import for the adapter
from google.genai import types

MAX_ROUNDS = 3

# Global retry options for the Gemini model adapter
GLOBAL_GEMINI_RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=30, attempts=5)

# Instantiate the Gemini model adapter with global retry options
GEMINI_MODEL_ADAPTER = Gemini(
    model="gemini-3.1-flash-lite-preview", # Model name as per previous context
    retry_options=GLOBAL_GEMINI_RETRY_OPTIONS
)

# Keep the string model name for reference if needed, though the adapter is preferred for config
GEMINI_MODEL_STR = "gemini-3.1-flash-lite-preview"

# Removed GLOBAL_GENERATE_CONTENT_CONFIG as retry options are now on the adapter instance.
# If other generate_content_config settings are needed, they should be passed differently.
