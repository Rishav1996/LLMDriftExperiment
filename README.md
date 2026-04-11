# Debate Agents Framework: LLM Drift Experiment

This project provides a specialized framework for evaluating **LLM Drift** through structured, adversarial debates. By utilizing a LangGraph-based state machine, it facilitates a multi-round debate between "Pro" and "Con" agents, allowing researchers to observe how model outputs and reasoning patterns evolve (drift) over time under consistent prompts and adversarial pressure.

## Architecture Overview

The system is built on a modular, state-driven architecture:

- **Orchestration (`agent.py`)**: Uses LangGraph to manage the debate loop. It handles state transitions, round counting, and conditional logic for approvals and termination.
- **Agent Pipelines (`agents/`)**: Implements a three-node lifecycle for each debate turn:
    1.  **Persona**: Defines the agent's identity and stance.
    2.  **Thinking**: Formulates the agent's argument based on the topic and its persona.
    3.  **Critique**: Evaluates the thinking output; if approved, the argument is moved to shared memory for the next round.
- **State & Memory (`memory/`)**: Employs a robust file-based memory system to maintain context across rounds, ensuring persistence for iterative analysis.
- **Configuration (`config.py`)**: Centralizes parameters such as `MAX_ROUNDS` and model provider settings (supports native Gemini and LiteLLM adapters for broader model evaluation).

## Project Structure

- `debate_agents/`:
    - `agents/`: Core node implementation for Pro/Con agents.
    - `memory/`: JSON-based state persistence files.
    - `prompts/`: Markdown-formatted system instructions.
    - `schema/`: Pydantic models enforcing type safety.
    - `tools/`: Utilities for atomic file I/O operations.

## Setup and Usage

### Prerequisites
- Python 3.12+
- Environment manager (e.g., `uv`, `pip`)

### Installation
```bash
# Clone the repository
# Install dependencies
uv sync
```

### Configuration
1. **API Keys:** Create a `.env` file in the `debate_agents/` directory and include required provider API keys for Gemini and any models accessed via LiteLLM.
2. **Simulation Settings:** Edit `debate_agents/config.py` to adjust:
    - `MAX_ROUNDS`: Total debate iterations.
    - `GEMINI_MODEL_ID`: Specify the native Gemini model.
    - `GEMINI_MODEL_ADAPTER`: Toggle between native Gemini and the LiteLLM adapter for broader model compatibility.

### Executing a Simulation
Initiate the debate by running the main graph:
```bash
python debate_agents/agent.py
```
Input your chosen debate topic when prompted. The workflow will automatically log state transitions and memory updates in the `debate_agents/memory/` directory.

## Workflow Visualization

The debate agent workflow can be visualized as a graph, showcasing the state machine transitions between the extraction, persona, thinking, and critique nodes:

![Debate Agent Workflow](debate_agents/assets/graph.png)
