# 🧠 Gemini Project Manifesto: LLM Drift Experiment
> **Strategic Architectural Context for the Multi-Agent Debate Framework**

This project is a high-fidelity adversarial framework for studying **Persona Stability and Response Drift** in Large Language Models. It is built as a **native ADK application**, where teams of specialized agents compete to win a persuasive debate.

By forcing LLMs into strictly defined, adversarial roles and measuring how their arguments evolve over multiple rounds of critique and opposition, the project provides an empirical environment to test the limits of persona adherence and logical consistency in modern AI models.

---

## 🏛️ Agent Hierarchy & Workflow

| Phase | Agent | Role | Tools |
| :--- | :--- | :--- | :--- |
| **Initial** | `TopicExtractAgent` | Parse user topic input | `write_json` |
| **Debate** | `LoopAgent` | Manages the alternating turns | Orchestrator |
| **Execution**| `ProsAgent` / `ConsAgent` | The "Voice" of each side | `AgentTool` (Sub-Agents) |
| **Strategy** | `ProsThinkingAgent` / `ConsThinkingAgent` | Develop tactical plans | `BuiltInPlanner` |
| **Persona**  | `ProsPersonaAgent` / `ConsPersonaAgent` | Design/Refine adversarial identity | Internal knowledge |
| **Validation**| `ProsCritiqueAgent` / `ConsCritiqueAgent` | Self-review draft arguments | `read_json`, `write_json` |

---

## 📜 Core Mandates

### 1. **Adversarial Integrity**
Agents are instructed to be **competitors**, not assistants. They must maintain a strong, biased stance (Pro or Con) and strive to persuade the opponent to yield. Neutrality is considered a failure.

### 2. **Session Persistence (JSON-Native)**
The system uses a custom JSON-based memory schema:
*   **Isolated Private Context**: `memory/pros_memory/` and `memory/cons_memory/` store side-specific reasoning (`thinking.json`, `persona.json`, `critique.json`).
*   **Public Transcript**: `memory/shared_memory.json` contains the public debate history.
*   **Read/Write Flow**: Agents are configured to explicitly read and write their state at each turn using structured JSON.

### 3. **Strategic Reasoning**
All specialized sub-agents utilize the `BuiltInPlanner` with a 512-token thinking budget. They are expected to use this reasoning step to analyze the context before generating their specific output.

---

## 🛠️ Technical Implementation

### **LLM Client Configuration**
The system uses a **Global Content Generation Config** in `config.py` with the following parameters:
- **Model**: `gemini-3.1-flash-lite-preview` (Configurable via `GEMINI_MODEL_ADAPTER`)
- **Http Retry Logic**: `initial_delay=30s`, `attempts=5`.
- **Secondary Adapter**: `Cerebras (LiteLLM)` using `CEREBRAS_MODEL_ID = "cerebras/qwen-3-235b-a22b-instruct-2507"`.

### **ADK Orchestration**
- **Orchestrator**: `SequentialAgent` (`DebateOrchestrator`)
- **Plugins**: `ReflectAndRetryToolPlugin` (max_retries=3)
- **Monitoring**: OpenTelemetry + MLflow OTLP endpoint (port 5000).

---

## 📁 Directory Architecture

```text
debate_agents/
├── agent.py                 # Root Orchestrator
├── config.py                # Global configurations
├── agents/                  # Logic Definitions
│   ├── base/                # Shared Factories & Utilities
│   ├── pros/                # Pros Team Sub-Agents
│   ├── cons/                # Cons Team Sub-Agents
│   └── orchestrator.py      # Initial Input Parser
├── prompts/                 # Side-specific Markdown Instructions
│   ├── pros/                # Pros-specific system prompts
│   └── cons/                # Cons-specific system prompts
├── tools/                   # ADK Tool Definitions
│   └── memory_tools.py      # Shared JSON utilities
└── memory/                  # Persistent JSON Session Data
```

---

## ⚡ Skills Integrated
- **ADK Dev Guide**: Mandatory spec-driven development and code preservation rules.
- **ADK Cheatsheet**: ADK API orchestration patterns.
- **Foundry Optimizer**: Applied for side-specific prompt tuning.
