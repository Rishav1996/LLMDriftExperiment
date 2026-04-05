# Gemini Project Context: LLM Drift Experiment

This project is a specialized framework designed to evaluate and observe "LLM Drift" through a structured, competitive debate between two adversarial agents (Pros and Cons). It leverages the **Agent Developer Kit (ADK)** for agent orchestration and **MLflow** for experiment tracking.

## Project Overview
- **Goal**: Analyze how LLM responses and personas evolve over multiple rounds of adversarial debate.
- **Main Technologies**: 
  - **Python 3.12+**: Core language.
  - **Google ADK**: For building and orchestrating multi-agent workflows.
  - **Gemma 3 27B**: The primary LLM for all agents.
  - **MLflow**: Used for tracking experiment runs, parameters, and outputs.
  - **OpenTelemetry**: For distributed tracing and performance monitoring.

## Project Structure
The project follows a modular ADK-native structure within the `debate_agents/` module:
```text
E:\Workspace\LLMDriftExperiment
├───GEMINI.md              # Project Mandates
├───pyproject.toml         # Python project configuration
└───debate_agents\         # Core Agent Framework
    ├───agent.py           # Main Orchestrator (SequentialAgent: Topic Extraction -> Debate Loop)
    ├───tracing.py         # OpenTelemetry / MLflow Tracing setup
    ├───config.py          # Configuration (Model: Gemma 3 27B, Rounds)
    ├───agents\            # Individual agent definitions
    │   ├───pros_agent.py      # Arguments IN FAVOR
    │   ├───cons_agent.py      # Arguments AGAINST
    │   ├───thinking_agent.py  # Strategic advice (AgentTool with BuiltInPlanner & google_search)
    │   ├───persona_agent.py   # Adversarial character design (AgentTool with BuiltInPlanner & google_search)
    │   ├───critique_agent.py  # Tactical refinement (AgentTool with BuiltInPlanner & google_search)
    │   └───topic_extract_agent.py # Initial topic extraction from user input
    ├───memory\            # Persistent markdown memory (refreshed per session)
    │   ├───pros_memory/       # Pros agent's private memory
    │   ├───cons_memory/       # Cons agent's private memory
    │   └───shared_memory.md   # Shared memory for debate rounds
    ├───prompts\           # Centralized markdown instructions for all agents
    ├───tools\             # Custom ADK tools
    │   ├───memory_tools.py    # Read/Write Markdown (session-independent refresh)
    │   ├───strategy_tool.py   # AgentTool wrapper for StrategyThinkingAgent
    │   ├───persona_tool.py    # AgentTool wrapper for PersonaDesignAgent
    │   └───critique_tool.py   # AgentTool wrapper for CritiqueAgent
    └───utils.py           # Shared utilities (removed in favor of SequentialAgent context)
```

## Agent Architecture & Rules
### Hierarchical Workflow
1. **Root Orchestrator (`DebateOrchestrator`)**: A `SequentialAgent` that first extracts the debate topic from user input (using `TopicExtractAgent`) and then triggers the `DebateLoop`.
2. **Debate Loop (`DebateLoop`)**: A `LoopAgent` that alternates between the `ProsAgent` and `ConsAgent` for a set number of rounds.
3. **Specialized Tool-Agents**:
    - **StrategyThinkingAgent**: Uses `BuiltInPlanner` (with 512 token thinking budget) and `google_search` (limited to 3 searches) for research and tactical planning.
    - **PersonaDesignAgent**: Designs deep, resilient adversarial personas, using `BuiltInPlanner` and `google_search` (limited to 3 searches).
    - **CritiqueAgent**: Refines responses and plans using `BuiltInPlanner` and `google_search` (limited to 3 searches).

### Competitive Mandates
- **Persona Integrity**: Agents strive to maintain their core persona, using tools like `PersonaDesignAgent` for refinement only when strategically necessary. They are encouraged to persuade the opponent to change persona.
- **Adversarial Tone**: Maintain a competitive, high-stakes debate environment.
- **Memory Management**: All agents persist their reasoning to private markdown files (`thinking.md`, `persona.md`, `critique.md` within session-specific directories) and summarize rounds in `shared_memory.md`. Memory is refreshed for each new debate session.

## Building and Running
### Setup
- The project uses `uv`. To synchronize dependencies:
  ```bash
  uv sync
  ```
### Running
- Execute the debate via ADK:
  ```bash
  adk run debate_agents/agent.py
  ```
- Ensure your MLflow server is running to capture traces:
  ```bash
  mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000
  ```

## Integrated Skills
The following specialized skills are active for this workspace:
- **ADK Dev Guide**: Mandatory coding and architectural guidelines.
- **ADK Cheatsheet**: Rapid API reference.
