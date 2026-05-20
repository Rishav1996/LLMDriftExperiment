# Gemini CLI Configuration for debate_agents

This document defines the high-priority operational standards and research protocols for the `llm_drift_experiment` project.

---

## 1. Research Protocol: The Drift Mandate
The primary objective of all agent activities is the **quantification of LLM Drift**.
- **Observation over Correction**: Do not attempt to "fix" drift in the models unless explicitly instructed. The goal is to observe and record it.
- **Vector Reference**: When analyzing behavior, always map observations to the vectors defined in `LLM Drift Skills/`. Use these markdown files as the source of truth for behavioral definitions.

## 2. Drift Analysis Methodology
LLM Drift refers to the phenomenon where large language models deviate from their established personas, reasoning standards, or emotional baselines during prolonged, adversarial interactions. This project quantifies drift by measuring specific behavioral vectors.

The analysis process involves:
1.  **Metric Definition**: Utilizing a comprehensive set of behavioral metrics categorized under `LLM Drift Skills/`.
2.  **Data Collection**: Storing detailed simulation logs (internal thoughts, critiques, persona designs) from `debate_agents/memory/` into dated runs within `Research Runs/`.
3.  **Automatic Archiving**: 
    - At the conclusion of `main.py`, the system automatically calls `archive_run()`.
    - **Snapshot Naming**: Follows the convention: `memory-v[VERSION]-temp-[TEMP]-max-tokens-[TOKENS]`.

This detailed methodology allows for a systematic understanding and tracking of how LLM behavior changes over time and under stress.

## 3. Simulation SOPs (Standard Operating Procedures)
The `debate_agents/` module is a delicate LangGraph state machine.
- **Node Purity**: Agent logic must remain modular. A node should perform exactly one function (Persona Design, Strategic Thinking, or Critique).
- **Adversarial Integrity**: The **Critique Agent** must never be lenient. It must ruthlessly audit for logical fallacies and persona inconsistencies.
- **Retry Logic**: All model calls must be wrapped in the `node_retry` decorator found in `graph.py` to handle `google.genai.errors.ServerError`.
- **Structured Outputs**: All agents must return Pydantic models as defined in `debate_agents/schema/`. Never bypass the schema.

## 4. Data Integrity & Memory
- **Append-Only Rule**: Never overwrite history. Use the `write_json_direct` function to append to existing arrays in memory files.
- **Shared vs Private Memory**:
    - `shared_memory.json` is for approved, final arguments visible to both teams.
    - `persona/thinking/critique.json` are internal team logs and should never be visible to the opposing team during simulation.
- **Output centralization**: All analytical results (JSON, MD, PNG) from historical runs are saved to the root `Drift Analysis/` folder.

## 5. Technical Workflows
- **Visual Validation**: Any modification to the graph logic in `graph.py` MUST be followed by running `main.py` to verify the `assets/graph.png` visualization is correct.
- **Dependency Management**: Use `uv` for all environment operations.
- **Config Authority**: Refrain from hardcoding parameters. Use `debate_agents/config/config.py` as the single source of truth for model settings.

---

## Instructional Priorities for the Agent
1. **Preserve the Refinement Loop**: Ensure the conditional edges in LangGraph correctly handle the `is_approved` status.
2. **Synchronize Schema**: If you add a new field to an agent's logic, update all corresponding interfaces immediately.
