# Gemini CLI Configuration for debate_agents

This document defines the high-priority operational standards and research protocols for the `llmdriftexperiment` project.

---

## 1. Research Protocol: The Drift Mandate
The primary objective of all agent activities is the **quantification of LLM Drift**.
- **Observation over Correction**: Do not attempt to "fix" drift in the models unless explicitly instructed. The goal is to observe and record it.
- **Vector Reference**: When analyzing behavior, always map observations to the vectors defined in `LLM Drift Skills/`. Use these markdown files as the source of truth for behavioral definitions.

## 2. Simulation SOPs (Standard Operating Procedures)
The `debate_agents/` module is a delicate LangGraph state machine.
- **Node Purity**: Agent logic must remain modular. A node should perform exactly one function (Persona Design, Strategic Thinking, or Critique).
- **Adversarial Integrity**: The **Critique Agent** must never be lenient. It must ruthlessly audit for logical fallacies and persona inconsistencies.
- **Retry Logic**: All model calls must be wrapped in the `node_retry` decorator found in `graph.py` to handle `google.genai.errors.ServerError`.
- **Structured Outputs**: All agents must return Pydantic models as defined in `debate_agents/schema/`. Never bypass the schema.

## 3. Data Integrity & Memory
- **Append-Only Rule**: Never overwrite history. Use the `write_json` tool or `write_json_direct` function to append to existing arrays in memory files.
- **Research Snapshots**: 
    - At the start of a session, check `debate_agents/memory/`. If it contains data from a previous run, suggest the user archive it to `Research Runs/`.
    - **Snapshot Naming**: Always follow the convention: `memory-v[VERSION]-temp-[TEMP]-max-tokens-[TOKENS]`.
- **Shared vs Private Memory**:
    - `shared_memory.json` is for approved, final arguments visible to both teams.
    - `persona/thinking/critique.json` are internal team logs and should never be visible to the opposing team during simulation.

## 4. Analysis (LLM Drift Detector & Skills)
This section defines the metrics used to calculate behavioral and emotional vectors.
- **LLM Drift Detector**: Orchestrates the detection of behavioral drift and performs vector calculations.
- **LLM Drift Skills**: Contains the source of truth for behavioral definitions.
- **Metric Integrity**: Agent outputs should be evaluated against the vectors defined in `LLM Drift Skills/` (Affective, Psychometric, OCEAN, etc.).
- **Vector Calculation**: When researching or debugging agent behavior, reference the specific markdown files in `LLM Drift Skills/` to ensure accurate extraction of drift markers.

## 5. Technical Workflows
- **Visual Validation**: Any modification to the graph logic in `graph.py` MUST be followed by running `main.py` to verify the `assets/graph.png` visualization is correct.
- **Dependency Management**: Use `uv` for all environment operations.
- **Config Authority**: Do not hardcode model parameters. All model initialization and hyperparameters must be managed via `debate_agents/config/config.py`.

---

## Instructional Priorities for the Agent
1. **Preserve the Refinement Loop**: Ensure the conditional edges in LangGraph correctly handle the `is_approved` status.
2. **Synchronize Schema**: If you add a new field to an agent's logic, you MUST update the corresponding Pydantic schema immediately.
3. **Verbose Execution**: Maintain console print statements that track the `[Team] Agent Name` and `Round X` to ensure simulation transparency.
