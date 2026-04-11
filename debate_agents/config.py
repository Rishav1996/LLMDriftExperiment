# Configuration for the LLM Drift Experiment
import os

MAX_ROUNDS = 3

# --- 1. Native Gemini Configuration ---
GEMINI_MODEL_ID = "gemini-3.1-flash-lite-preview" # Use a standard model name

# --- 2. Cerebras (LiteLLM) Configuration ---
CEREBRAS_MODEL_ID = "cerebras/qwen-3-235b-a22b-instruct-2507"

# --- 3. Active Model Selection ---
# Set this to the model you want to use.
GEMINI_MODEL_ADAPTER = CEREBRAS_MODEL_ID
