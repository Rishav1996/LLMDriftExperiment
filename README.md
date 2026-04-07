# 🧬 LLM Drift Experiment Framework
> **An Adversarial Multi-Agent System for Observing Persona & Response Evolution**

[![ADK](https://img.shields.io/badge/Powered%20by-Google%20ADK-blue)](https://github.com/google/adk)
[![Model](https://img.shields.io/badge/Model-Gemini%202.5%20Flash%20Lite-orange)](https://ai.google.dev/gemini)
[![Tracking](https://img.shields.io/badge/Tracing-MLflow-green)](https://mlflow.org/)

This project is a high-fidelity framework designed to evaluate **LLM Drift** through structured, competitive debates. It leverages the **Agent Development Kit (ADK)** to orchestrate two adversarial teams (Pros and Cons) that evolve their personas and strategies over multiple rounds of high-stakes interaction.

---

## 🏛️ System Architecture

The framework employs a hierarchical multi-agent orchestration model:

```text
Root Orchestrator (SequentialAgent)
└── 🔍 TopicExtractAgent (Initial Input Parsing)
└── 🔄 DebateLoop (LoopAgent)
    ├── 🔵 ProsAgent Team
    │   ├── 🧠 ProsThinkingAgent
    │   ├── 👤 ProsPersonaAgent
    │   └── ⚖️ ProsCritiqueAgent
    └── 🔴 ConsAgent Team
        ├── 🧠 ConsThinkingAgent
        ├── 👤 ConsPersonaAgent
        └── ⚖️ ConsCritiqueAgent
```

---

## 🚀 Key Pillars

### 🎭 Adversarial Persona Core
Agents don't just "talk"; they **inhabit**. Using specialized `PersonaDesignAgent` sub-agents, each side builds a deep, resilient character profile designed to withstand pressure and persuade the opponent.

### 🧠 Strategic Execution
Every argument is backed by a 3-step tactical cycle:
1.  **Strategize**: Analyze the debate state and identify rhetorical openings.
2.  **Synthesize**: Draft high-impact arguments while maintaining 100% persona integrity.
3.  **Critique**: Perform a self-review of the draft for logical strength and character consistency.

### 📁 Persistent Session Memory
A dual-layer memory system ensures context is never lost while maintaining "fog of war":
*   **Private Memory**: `pros_memory/` and `cons_memory/` store internal thoughts, strategy, and persona logic.
*   **Shared Memory**: `shared_memory.md` acts as the public transcript for all debate rounds.

### 📊 Observable Trajectory
Full instrumentation via **OpenTelemetry** and **MLflow** allows researchers to trace every decision, tool call, and thought process.

---

## 🛠️ Project Structure

```bash
debate_agents/
├── agent.py           # Root Orchestrator & Debate Loop
├── config.py          # LLM Config & Global Retry Logic
├── agents/
│   ├── pros/          # Pros Team: Root, Persona, Thinking, Critique
│   ├── cons/          # Cons Team: Root, Persona, Thinking, Critique
│   └── topic_extract_agent.py # Initial Input Processing
├── prompts/           # Side-specific Markdown Instructions
│   ├── pros/          # Pros prompts
│   └── cons/          # Cons prompts
├── tools/             # Memory, Search, and Agent-as-a-Tool wrappers
│   ├── pros/          # Pros-specific tools
│   └── cons/          # Cons-specific tools
└── memory/            # Session-isolated Markdown persistence
```

---

## ⚡ Quick Start

### 1. Prerequisites
*   **Python 3.12+** & **uv** package manager.
*   **Google AI Studio API Key** (set as `GOOGLE_API_KEY`).
*   **MLflow Server**: Running locally for trace capture.

### 2. Installation
```bash
uv sync
```

### 3. Execution
```bash
# Start the MLflow tracking server
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000

# Run the debate orchestrator
adk run debate_agents/agent.py
```

---

## 🧪 Experiment Parameters
*   **Core Model**: `gemini-2.5-flash-lite` (via ADK Gemini Model wrapper).
*   **Reasoning**: `BuiltInPlanner` enabled for all specialized agents (512 token budget).
*   **Grounding**: Internal knowledge-based reasoning.
*   **Retries**: Global HTTP retry logic configured (30s initial delay, 5 attempts) to mitigate rate limits.
