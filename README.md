# LLM Drift Experiment Framework

A specialized adversarial debate framework built with **Agent Developer Kit (ADK)** to observe and analyze **LLM Drift** through iterative competitive interactions.

## 🚀 Key Features
- **Adversarial Orchestration**: A `SequentialAgent` pipeline that first extracts a topic from user input and then coordinates a `LoopAgent` debate between `Pros` and `Cons` agents.
- **Strategic Persona Core**: Agents utilize specialized `AgentTool` sub-agents (`StrategyThinkingAgent`, `PersonaDesignAgent`, `CritiqueAgent`) to refine their characters and tactics.
- **Isolated Session Memory**: Custom markdown-based memory system with session-isolated private folders (`pros_memory/`, `cons_memory/`) and a `shared_memory.md` for round summaries.
- **Model Grounding**: Powered by **Gemma 3 27B** with `BuiltInPlanner` for advanced reasoning and `google_search` for factual grounding.
- **Experiment Tracking**: Integrated with **MLflow** for post-debate analysis of agent evolution.
- **Gemma 3 27B**: The primary LLM for all agents.
- **Distributed Tracing**: Full instrumentation via **OpenTelemetry** exporting to **MLflow** for detailed performance and trajectory analysis.

## 🛠️ Project Structure
- `debate_agents/agent.py`: The root orchestrator (SequentialAgent).
- `debate_agents/tracing.py`: Global tracing configuration (OTLP -> MLflow).
- `debate_agents/agents/`: Individual agent logic definitions.
- `debate_agents/prompts/`: Centralized markdown files for all agent instructions.
- `debate_agents/tools/`: Custom tools for memory isolation and Agent-as-a-Tool wrappers.
- `debate_agents/memory/`: Persistent storage for agent reasoning history.

## ⚡ Quick Start
### Prerequisites
- Python 3.12+
- `uv` package manager
- Google AI Studio API Key (configured as `GOOGLE_API_KEY`)
- Local MLflow server running: `mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000`

### Installation
```bash
uv sync
```

### Running the Debate
```bash
adk run debate_agents/agent.py
```
*Note: Ensure your MLflow server is active to capture traces.*

## 🧬 Framework Details
The agents follow a 3-step preparation cycle in each round:
1. **Persona Design**: Refining their voice and adversarial stance.
2. **Strategy Thinking**: Researching the topic and formulating tactical points.
3. **Critique**: Self-evaluating the persona and strategy before final generation.
