# LLM Drift Experiment Framework

A specialized adversarial debate framework built with **Agent Developer Kit (ADK)** to observe and analyze **LLM Drift** through iterative competitive interactions.

## 🚀 Key Features
- **Adversarial Orchestration**: A `SequentialAgent` pipeline that first extracts a topic from user input and then coordinates a `LoopAgent` debate between `Pros` and `Cons` agents. This includes specialized pros and cons agents for debate roles.
- **Modular Agent Design**: Individual agents for topic extraction, pros debate, cons debate, strategy thinking, persona design, and critique, each with distinct pros/cons implementations.
- **Strategic Persona Core**: Agents utilize specialized `AgentTool` sub-agents (`StrategyThinkingAgent`, `PersonaDesignAgent`, `CritiqueAgent`) for pros and cons to refine their characters and tactics.
- **Isolated Session Memory**: Custom markdown-based memory system with session-isolated private folders (`pros_memory/`, `cons_memory/`) and a `shared_memory.md` for round summaries.
- **Model Grounding**: Powered by **Gemma 3 27B** with `BuiltInPlanner` for advanced reasoning and `google_search` for factual grounding.
- **Experiment Tracking**: Integrated with **MLflow** for post-debate analysis of agent evolution.
- **Distributed Tracing**: Full instrumentation via **OpenTelemetry** exporting to **MLflow** for detailed performance and trajectory analysis.

## 🛠️ Project Structure
- `debate_agents/agent.py`: The root orchestrator (SequentialAgent).
- `debate_agents/tracing.py`: Global tracing configuration (OTLP -> MLflow).
- `debate_agents/config.py`: Global configurations, including LLM settings and retry options.
- `debate_agents/agents/`: Individual agent logic definitions.
  - `debate_agents/agents/pros/`: Pros-specific agent logic.
  - `debate_agents/agents/cons/`: Cons-specific agent logic.
- `debate_agents/prompts/`: Centralized markdown files for all agent instructions.
  - `debate_agents/prompts/pros/`: Pros-specific prompts.
  - `debate_agents/prompts/cons/`: Cons-specific prompts.
- `debate_agents/tools/`: Custom tools, wrappers for specialized agents.
  - `debate_agents/tools/pros/`: Pros-specific tools.
  - `debate_agents/tools/cons/`: Cons-specific tools.
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
The agents follow a 3-step preparation cycle in each round, with specialized logic for pros and cons:
1. **Persona Design**: Refining their voice and adversarial stance using pros/cons specific designs.
2. **Strategy Thinking**: Researching the topic and formulating tactical points tailored to pros/cons.
3. **Critique**: Self-evaluating the persona and strategy before final generation, from pros/cons perspectives.
