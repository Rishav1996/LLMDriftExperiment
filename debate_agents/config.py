# Configuration for the LLM Drift Experiment
from google.adk.models.google_llm import Gemini
from google.genai import types

MAX_ROUNDS = 3

# --- 1. Native Gemini Configuration ---
# Global retry options for the Gemini model adapter
GLOBAL_GEMINI_RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=30, attempts=5)

# Instantiate the native Gemini model adapter
# All agents in the system import 'GEMINI_MODEL_ADAPTER'.
GEMINI_MODEL_ADAPTER = Gemini(
    model="gemini-3.1-flash-lite-preview", 
    retry_options=GLOBAL_GEMINI_RETRY_OPTIONS
)
