# Gemini CLI Configuration for Debate Agents

This file contains specialized instructions and operational context for using the Gemini CLI within this project.

## Project Scope
This project, `llmdriftexperiment`, utilizes an adversarial debate framework to track and analyze LLM drift.

## Operational Mandates
- **Memory Management:** Ensure that any modifications to agent logic respect the file-based memory system in `debate_agents/memory/`.
- **Schema Integrity:** Any changes to agent logic (in `debate_agents/agents/`) must be reflected in the corresponding schemas (in `debate_agents/schema/`).
- **Graph Updates:** If modifying the debate workflow in `debate_agents/agent.py`, update the `DebateState` and conditional edge logic to maintain graph stability.

## Standard Development Workflows
- **Running Simulations:** Always verify agent interactions using `python debate_agents/agent.py`.
- **Testing:** Add new test cases for individual nodes within `debate_agents/agents/` when introducing new logic.
- **Model Configuration:** Changes to model providers should be handled exclusively via `debate_agents/config.py`.
