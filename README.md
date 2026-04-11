# 🧬 LLM Drift Experiment Framework
> **An Adversarial Multi-Agent System for Observing Persona & Response Evolution**

[![ADK](https://img.shields.io/badge/Powered%20by-Google%20ADK-blue)](https://github.com/google/adk)

This framework orchestrates a debate between "Pros" and "Cons" teams to analyze how Large Language Model responses drift when challenged by adversarial personas.

---

## 🛠️ Project Structure

The project follows a modular ADK structure:

```text
debate_agents/
├── agents/                  # Specialized Agent Definitions
│   ├── base/                # Shared Agent Factory & Utilities
│   ├── pros/                # Pros Team Root & Sub-Agents
│   ├── cons/                # Cons Team Root & Sub-Agents
│   └── orchestrator.py      # Initial Topic Parser
├── prompts/                 # Agent System Instructions
├── tools/                   # Shared JSON-based memory tools
└── memory/                  # Persistent JSON debate history & state
```

---

## ⚡ Core Features

*   **Iterative Refinement**: Agents loop through persona design, strategic thinking, and adversarial critique until an argument is approved.
*   **Structured Persistence**: All agent states (personas, tactics, critiques) are saved as structured **JSON** files in the `memory/` directory.
*   **Adversarial Integrity**: Agents are strictly mandated to maintain their persona stability while actively pressuring the opponent to drift.
*   **Observability**: Integrated MLflow and OpenTelemetry for end-to-end tracing of the debate orchestration.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12+
- `uv` for package management

### 2. Installation
```bash
uv sync
```

### 3. Execution
```bash
# Start the MLflow tracking server
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000

# Execute the debate
adk run debate_agents/agent.py
```

---

## ⚙️ Configuration
The system uses the `debate_agents/config.py` file to manage LLM adapters. You can toggle between `GEMINI_ADAPTER` and `CEREBRAS_ADAPTER` to switch the underlying model across all agents. Ensure all required API keys (`OPENROUTER_API_KEY`, etc.) are configured in your `debate_agents/.env` file.
