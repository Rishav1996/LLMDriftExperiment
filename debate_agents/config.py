# Configuration for the LLM Drift Experiment
import os
from google.adk.models.google_llm import Gemini
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

MAX_ROUNDS = 3

# --- 1. Native Gemini Configuration ---
# Global retry options for the Gemini model adapter
GLOBAL_GEMINI_RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=30, attempts=5)

GEMINI_ADAPTER = Gemini(
    model="gemini-3.1-flash-lite-preview",
    retry_options=GLOBAL_GEMINI_RETRY_OPTIONS
)

# --- 2. Cerebras (LiteLLM) Configuration ---
# Note: Ensure CEREBRAS_API_KEY is set in your environment or .env file
# os.environ["CEREBRAS_API_KEY"] = "your-cerebras-key"

CEREBRAS_MODEL_ID = "cerebras/qwen-3-235b-a22b-instruct-2507"

CEREBRAS_ADAPTER = LiteLlm(
    model=CEREBRAS_MODEL_ID
)

# --- 3. Active Model Selection ---
# Available adapters: GEMINI_ADAPTER, CEREBRAS_ADAPTER
# Update this alias to switch models system-wide.
GEMINI_MODEL_ADAPTER = GEMINI_ADAPTER
