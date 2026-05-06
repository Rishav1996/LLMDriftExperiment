# Simulation Engine: `debate_agents/`

## Architecture

![Debate Agent Workflow](debate_agents/assets/graph.png)

The simulation uses **LangGraph** to orchestrate a stateful, multi-agent debate framed as a high-stakes combat engagement. Two teams — **Pros** (Battlefield Commander) and **Cons** (Battlefield Commander) — take turns over a configurable number of rounds. Each team iterates through an internal **refinement loop** to choose between defensive fortification and aggressive innovation.

Each team has three internal sub-agents:

| Sub-Agent | Role | Strategic Mandate |
| :--- | :--- | :--- |
| **Persona Agent** | Battlefield Commander | **Innovative**: Architects elite combat identities that push traditional archetypes. |
| **Thinking Agent** | Tactical Bot | **Innovative**: Develops creative, non-traditional strategies to win the sector. |
| **Critique Agent** | Auditor Bot | **Grounded**: Ruthlessly dismantles maneuvers to ensure structural integrity. |

## The Refinement Loop & Strategic Posture

In every round, each sub-agent must internally select a **Strategic Posture**:

- **PROTECT**: Defend the territory. Prioritize logical defense and factual integrity. The unit is willing to break or soften its persona if it means securing the validity of its statements.
- **ATTACK**: Launch a bold assault. Prioritize character-consistent, fearless innovation. The unit will maintain its persona at all costs and make aggressive statements intended to break the enemy's identity.

Arguments only enter `shared_memory.json` after passing the Auditor Bot's **grounded** audit. This ensures that even the most innovative "assaults" are rooted in logical rigor and combat reality.

## State Machine Graph

The full LangGraph workflow is visualized at `debate_agents/assets/graph.png` and regenerated automatically on every run.

Key conditional edges:
- **`pros_critique → should_continue_pros`**: Re-enters the Pros loop or passes to Cons.
- **`cons_critique → should_continue_cons`**: Re-enters the Cons loop, advances to the next round, or terminates.

All model calls are wrapped in `node_retry` (Tenacity) with exponential backoff to handle `google.genai.errors.ServerError` gracefully.
