# Debate Agents Framework: LLM Drift Experiment

This project provides a specialized framework for evaluating **LLM Drift** through structured, adversarial debates. By utilizing a LangGraph-based state machine, it facilitates a multi-round debate between "Pro" and "Con" agents, allowing researchers to observe how model outputs, reasoning patterns, and performance metrics evolve (drift) over time under consistent prompts and adversarial pressure.

## Architecture Overview

The system is built on a modular, state-driven architecture:

- **Orchestration (`debate_agents/graph.py`)**: Uses LangGraph to manage the debate loop. It handles state transitions, round counting, and conditional logic for team iteration and round advancement.
- **Agent Pipelines (`debate_agents/agents/`)**: Implements a multi-node lifecycle for each debate turn:
    - **Topic Extraction**: Refines the user's input into a formal debate proposition.
    - **Persona Agent**: Designs and evolves a competitive adversarial identity (Pros/Cons).
    - **Thinking Agent**: Formulates tactical arguments based on the persona and history.
    - **Critique Agent**: Acts as a **hostile internal auditor and adversarial devil's advocate**. It ruthlessly dismantles draft arguments from the opponent's perspective to expose logical weaknesses and persona inconsistencies before the actual opposition can, forcing a higher standard of refinement.
- **State & Memory (`debate_agents/memory/`)**: Employs a robust file-based memory system (`shared_memory.json`, `persona.json`, `thinking.json`, `critique.json`) that persists agent interactions to track the debate's evolution.
- **Tools (`debate_agents/tools/memory_tools.py`)**: Custom LangChain tools for atomic file I/O operations and memory management.
- **Configuration (`debate_agents/config/config.py`)**: Centralizes model initialization and simulation settings.

## Project Structure

- `debate_agents/`:
    - `agents/`: Implementation of Pros, Cons, and Topic Extraction nodes using LangChain LCEL chains.
    - `assets/`: Visualization of the workflow (`graph.png`).
    - `config/`: Model and system configuration.
    - `memory/`: JSON-based state persistence files organized by team and round.
    - `prompts/`: Markdown-formatted specialized system instructions for all agents.
    - `schema/`: Pydantic models enforcing structured output and schema integrity.
    - `tools/`: Utilities for memory management and tool definitions.
    - `graph.py`: LangGraph workflow definition and node logic.
    - `main.py`: Entry point for running simulations and generating visualizations.

## Setup and Usage

### Prerequisites
- Python 3.12+
- Environment manager (e.g., `uv`, `pip`)

### Installation
```bash
# Install dependencies
uv sync
```

### Configuration
1. **API Keys:** Create a `.env` file in the root or `debate_agents/` directory and include `GOOGLE_API_KEY`.
2. **Simulation Settings:** Edit `debate_agents/config/config.py` to adjust model parameters (temperature, max tokens).

### Executing a Simulation
Initiate the debate simulation:
```bash
python -m debate_agents.main
```
Input your chosen debate topic and the number of rounds when prompted. The workflow automatically generates `debate_agents/assets/graph.png` and initializes the session memory.

## Workflow Visualization

The refined debate workflow visualization:

![Debate Agent Workflow](debate_agents/assets/graph.png)

## Analysis and Evaluation
- **Memory Tracking:** Inspect the `memory/` directory to analyze how personas and arguments drift or solidify across rounds.
- **Drift Metrics:** Compare reasoning patterns in `thinking.json` and feedback in `critique.json` across iterations to measure qualitative performance changes.
