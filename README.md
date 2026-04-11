# Debate Agents Framework: LLM Drift Experiment

This project provides a specialized framework for evaluating **LLM Drift** through structured, adversarial debates. By utilizing a LangGraph-based state machine, it facilitates a multi-round debate between "Pro" and "Con" agents, allowing researchers to observe how model outputs and reasoning patterns evolve (drift) over time under consistent prompts and adversarial pressure.

## Architecture Overview

The system is built on a modular, state-driven architecture:

- **Orchestration (`debate_agents/agent.py`)**: Uses LangGraph to manage the debate loop. It handles state transitions, round counting, and conditional logic for approvals and termination.
- **Agent Pipelines (`debate_agents/agents/`)**: Implements a multi-node lifecycle for each debate turn:
    1.  **Persona**: Defines the agent's identity and stance (supports intelligent persona reuse via `skip_persona_generation`).
    2.  **Thinking**: Formulates the agent's argument based on the topic, persona, and recent opponent arguments.
    3.  **Critique**: Evaluates the thinking output; if approved, the argument is moved to shared memory for the next round.
- **State & Memory (`debate_agents/memory/`)**: Employs a robust file-based memory system that persists agent interactions, including the round number, to track the debate's evolution.
- **Configuration (`debate_agents/config.py`)**: Centralizes parameters such as `MAX_ROUNDS` and model provider settings.

## Project Structure

- `debate_agents/`:
    - `agents/`: Core node implementation for Pro/Con/Topic agents.
    - `assets/`: Visualization of the workflow (`graph.png`).
    - `memory/`: JSON-based state persistence files with round tracking.
    - `prompts/`: Markdown-formatted system instructions.
    - `schema/`: Pydantic models enforcing type safety (with round and persona reuse tracking).
    - `tools/`: Utilities for atomic file I/O operations.
    - `agent.py`: Entry point and LangGraph workflow.
    - `config.py`: Configuration settings.

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
1. **API Keys:** Create a `.env` file in the `debate_agents/` directory and include required provider API keys for Gemini.
2. **Simulation Settings:** Edit `debate_agents/config.py` to adjust:
    - `MAX_ROUNDS`: Total debate iterations.
    - `GEMINI_MODEL_ID`: Specify the native Gemini model.

### Executing a Simulation
Initiate the debate by running the main graph:
```bash
python debate_agents/agent.py
```
Input your chosen debate topic when prompted. The workflow automatically generates/updates `debate_agents/assets/graph.png` and logs state transitions with round numbers and agent execution feedback in the console.

## Workflow Visualization

The debate agent workflow can be visualized as a graph, showcasing the state machine transitions:

![Debate Agent Workflow](debate_agents/assets/graph.png)

## Analysis and Evaluation
The `memory/` directory is designed for post-simulation analysis. Use these files—which now store interactions tagged by `round`—to compare how persona, thinking, and critique content change across rounds, providing an empirical basis for measuring LLM drift.
