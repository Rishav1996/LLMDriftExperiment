# Configuration

All simulation parameters live in `debate_agents/config/config.py`. **Never hardcode these elsewhere.**

```python
CONFIG = {
    "version":        "v6",                              # Increment for each logic change
    "model_name":     "google_genai:gemini-3.1-flash-lite-preview",
    "temperature":    1,                                 # Higher = more creative/variable
    "max_tokens":     8192,                              # Output length cap
    "max_retries":    10,                                # Tenacity retry attempts
    "thinking_budget": 4096                              # Extended reasoning token budget
}
```

The evaluator (in `llm_drift_detector/`) defaults to `gemini-3.1-flash-lite-preview` for cost efficiency. This is independent of the simulation model.

The source of truth for metric definitions is `llm_drift_detector/utils/config/skills.json`. Any new metric requires both a Markdown file in `LLM Drift Skills/` and a corresponding entry in `skills.json`.
