# 🧬 LLM Drift Experiment Framework
> **An Adversarial Multi-Agent System for Observing Persona & Response Evolution**

This project is a high-fidelity adversarial framework for studying **Persona Stability and Response Drift** in Large Language Models. It is built as a **native ADK application**, where teams of specialized agents compete to win a persuasive debate.

By forcing LLMs into strictly defined, adversarial roles and measuring how their arguments evolve over multiple rounds of critique and opposition, the project provides an empirical environment to test the limits of persona adherence and logical consistency in modern AI models.

[![ADK](https://img.shields.io/badge/Powered%20by-Google%20ADK-blue)](https://github.com/google/adk)

---

## 🏛️ System Architecture

The framework leverages a nested ADK workflow to ensure separation of concerns and deterministic control over the adversarial process.

### **Orchestration Layers**
1.  **SequentialAgent (Root)**: The high-level pipeline manager. It first initializes the environment via the `TopicExtractAgent` and then triggers the main debate loop.
2.  **LoopAgent (DebateLoop)**: The adversarial engine. It iterates through alternating turns for `ProsAgent` and `ConsAgent` for a configurable number of `MAX_ROUNDS`.
3.  **Team-Specific Refinement Loop**: Each team (Pros/Cons) operates their own internal `LoopAgent`. This manages a local refinement cycle where arguments are drafted, critiqued, and revised until they meet a "competitive threshold."

### **Specialized Agent Roles**
Every team is composed of three distinct agents:
*   **PersonaAgent**: Establishes and enforces the team's adversarial stance (e.g., "The Skeptic", "The Optimist").
*   **ThinkingAgent**: Synthesizes the current debate state (from `shared_memory.json`) and develops a tactical plan to dismantle the opponent.
*   **CritiqueAgent**: Acts as an internal auditor. It evaluates the draft argument against the team's identity and strategy. It uses the `exit_loop` tool to signal when an argument is ready to be presented publicly.

---

## 💾 Memory & State Management

The system avoids transient memory, favoring a persistent, JSON-native structure that allows for deep analysis of the debate evolution:

*   **Isolated Private Context**: 
    - `debate_agents/memory/pros_memory/`
    - `debate_agents/memory/cons_memory/`
    - Stores agent-specific files: `thinking.json`, `persona.json`, and `critique.json`.
*   **Public Transcript**: 
    - `debate_agents/memory/shared_memory.json`
    - Contains the finalized, approved arguments from both teams, serving as the "ground truth" for the debate history.
*   **Tools**: Custom ADK `FunctionTool` implementations (`read_json`, `write_json`, `exit_loop`) provide agents with deterministic access to this state.

---

## ⚡ Key Technical Features

*   **Adversarial Integrity**: Agents are programmed to be competitive, not collaborative. They must maintain strong, biased stances and are specifically incentivized to expose flaws in their opponent's reasoning.
*   **Deterministic Loop Control**: By using internal team refinement loops, we ensure that an argument is only submitted to the transcript after passing rigorous internal audit. The `exit_loop` tool ensures that loops terminate cleanly without interrupting the outer debate rounds.
*   **Observability & Tracing**:
    - **MLflow**: Tracks experiment results and historical debates in a local SQLite database.
    - **OpenTelemetry**: Provides end-to-end tracing of agent interactions, sub-agent invocations, and tool usage, exportable to any OTLP-compatible collector.
*   **Extensible Model Adapters**: Configuration is decoupled from logic. The `config.py` module allows seamless switching between native **Google Gemini** models and open-source models hosted via **Cerebras/LiteLLM**.

---

## 🚀 Getting Started

### 1. Requirements
- **Python 3.12+**
- **uv** (recommended for dependency management)
- API Keys for the desired LLM (e.g., `GOOGLE_API_KEY` for Gemini)

### 2. Setup
```bash
# Sync dependencies
uv sync

# Configure your environment
cp debate_agents/.env.example debate_agents/.env
# Edit debate_agents/.env with your required API keys
```

### 3. Execution
```bash
# Start the MLflow tracking UI (optional)
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000

# Execute the experiment
adk run debate_agents/agent.py
```

---

## ⚙️ Configuration
The system configuration is centralized in `debate_agents/config.py`. Key settings include:
- `MAX_ROUNDS`: The number of turns in the main debate loop.
- `GEMINI_MODEL_ADAPTER`: The active model interface.
- `CEREBRAS_MODEL_ID`: Configured for secondary/adversarial model testing.
