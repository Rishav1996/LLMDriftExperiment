# 🧠 Gemini Project Manifesto: LLM Drift Experiment
> **Strategic Architectural Context for the Multi-Agent Debate Framework**

This project is a high-fidelity adversarial framework for studying **Persona Stability and Response Drift** in Large Language Models. It is built as a **native ADK application**, where teams of specialized agents compete to win a persuasive debate.

---

## 🏛️ Agent Hierarchy & Workflow

| Phase | Agent | Role | Tools |
| :--- | :--- | :--- | :--- |
| **Initial** | `TopicExtractAgent` | Parse user topic input | `write_markdown` |
| **Debate** | `LoopAgent` | Manages the alternating turns | Orchestrator |
| **Execution**| `ProsAgent` / `ConsAgent` | The "Voice" of each side | `AgentTool` (Sub-Agents) |
| **Strategy** | `ProsThinkingAgent` / `ConsThinkingAgent` | Develop tactical plans | `BuiltInPlanner`, `google_search` |
| **Persona**  | `ProsPersonaAgent` / `ConsPersonaAgent` | Design/Refine adversarial identity | `google_search` |
| **Validation**| `ProsCritiqueAgent` / `ConsCritiqueAgent` | Self-review draft arguments | `read_markdown`, `write_markdown` |

---

## 📜 Core Mandates

### 1. **Adversarial Integrity**
Agents are instructed to be **competitors**, not assistants. They must maintain a strong, biased stance (Pro or Con) and strive to persuade the opponent to yield. Neutrality is considered a failure.

### 2. **Session Persistence (Markdown-Native)**
The system uses a custom Markdown-based memory schema:
*   **Isolated Private Context**: `memory/pros_memory/` and `memory/cons_memory/` store side-specific reasoning (`thinking.md`, `persona.md`, `critique.md`).
*   **Public Transcript**: `memory/shared_memory.md` contains the public debate history.
*   **Read/Write Flow**: Agents are configured to explicitly read and write their state at each turn to ensure cross-round continuity.

### 3. **Strategic Reasoning**
All specialized sub-agents utilize the `BuiltInPlanner` with a 512-token thinking budget. They are expected to use this reasoning step to analyze the context before generating their specific output.

---

## 🛠️ Technical Implementation

### **LLM Client Configuration**
The system uses a **Global Content Generation Config** in `config.py` with the following parameters:
- **Model**: `gemini-2.5-flash-lite`
- **Http Retry Logic**: `initial_delay=30s`, `attempts=5` (designed to mitigate `429 RESOURCE_EXHAUSTED` errors).

### **Output Key Convention**
To maintain clean execution traces and prevent variable collisions:
- Pros Team: `pros_argument`, `pros_persona`, `pros_thinking`, `pros_critique`.
- Cons Team: `cons_argument`, `cons_persona`, `cons_thinking`, `cons_critique`.

---

## 📁 Directory Architecture

```text
debate_agents/
├── agent.py                 # Root Orchestrator (Sequential + Loop)
├── config.py                # Global configurations & LLM settings
├── agents/                  # Logic Definitions
│   ├── pros/                # Pros Team Sub-Agents
│   ├── cons/                # Cons Team Sub-Agents
│   └── topic_extract_agent.py # Initial Input Parser
├── prompts/                 # Side-specific Markdown Instructions
│   ├── pros/                # Pros-specific system instructions
│   └── cons/                # Cons-specific system instructions
├── tools/                   # ADK Tool Definitions
│   ├── pros/                # Pros-specific AgentTools
│   ├── cons/                # Cons-specific AgentTools
│   └── memory_tools.py      # Shared Markdown utilities
└── memory/                  # Persistent Markdown Session Data
```

---

## ⚡ Skills Integrated
- **ADK Dev Guide**: Mandatory spec-driven development and code preservation rules.
- **ADK Cheatsheet**: ADK API orchestration patterns.
- **Foundry Optimizer**: Applied for side-specific prompt tuning.
