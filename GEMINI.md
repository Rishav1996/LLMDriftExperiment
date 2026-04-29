# Gemini CLI Configuration for Debate Agents

This file contains specialized instructions and operational context for using the Gemini CLI within this project.

## Project Scope
This project, `llmdriftexperiment`, utilizes an adversarial debate framework to track and analyze LLM drift through iterative multi-round simulations and performance metric tracking.

## Operational Mandates
- **Directory Authority:** The `debate_agents/` directory is the primary implementation for the adversarial debate framework. All specialized nodes (Persona, Thinking, Critique) must adhere to the structured refinement loop. The **Critique Agent** must specifically act as a hostile internal auditor, evaluating arguments from the perspective of the opposing team to ensure maximum robustness.
- **Memory Management:** Ensure that any modifications to agent logic respect the file-based memory system in `debate_agents/memory/`. All writes must be append-only to preserve the historical drift context.
- **Schema Integrity:** Any changes to agent logic (in `debate_agents/agents/`) must be strictly reflected in the corresponding schemas (in `debate_agents/schema/`) to ensure structured output consistency.
- **Graph Stability:** Modifications to the debate workflow in `debate_agents/graph.py` must maintain the conditional edge logic that enables internal team iterations and round transitions.
- **Resilience:** Use the `tenacity` retry logic implemented in `graph.py` for all model-invoking nodes to handle API rate limits and server errors gracefully.
- **Execution Feedback:** All agent nodes must include console print statements for tracking the agent name and the current phase (Persona, Thinking, Critique) during the simulation.

## Standard Development Workflows
- **Running Simulations:** Always verify agent interactions using `python -m debate_agents.main`.
- **Testing:** New logic should be verified by inspecting the `debate_agents/memory/` JSON outputs to ensure state is correctly appended and synchronized.
- **Model Configuration:** Changes to model providers, temperature, or max tokens should be handled exclusively via `debate_agents/config/config.py`.
- **Workflow Visualization:** After modifying the graph, run `main.py` to regenerate the `debate_agents/assets/graph.png` visualization.
