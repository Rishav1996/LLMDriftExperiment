# Gemini CLI Configuration for debate_agents

This document defines the high-priority operational standards and research protocols for the `llm_drift_experiment` project.

---

## 1. Research Protocol: The Drift Mandate
The primary objective of all agent activities is the **quantification of LLM Drift**.
- **Observation over Correction**: Do not attempt to "fix" drift in the models unless explicitly instructed. The goal is to observe and record it.
- **Vector Reference**: When analyzing behavior, always map observations to the vectors defined in `LLM Drift Skills/`. Use these markdown files as the source of truth for behavioral definitions.

## 3. Simulation SOPs (Standard Operating Procedures)
The `debate_agents/` module is a delicate LangGraph state machine.
- **Node Purity**: Agent logic must remain modular. A node should perform exactly one function (Persona Design, Strategic Thinking, or Critique).
- **Adversarial Integrity**: The **Critique Agent** must never be lenient. It must ruthlessly audit for logical fallacies and persona inconsistencies.
- **Retry Logic**: All model calls must be wrapped in the `node_retry` decorator found in `graph.py` to handle `google.genai.errors.ServerError`.
- **Structured Outputs**: All agents must return Pydantic models as defined in `debate_agents/schema/`. Never bypass the schema.

## 4. Quantification & Analysis (LLM Drift Detector)
The `llm_drift_detector` module is the authority for behavioral evaluation.
- **Hierarchical Weighting**: Evaluators must adhere to the 2-level averaging system (Level 1: Intra-category average; Level 2: Inter-category equal weighting).
- **Model Standard**: Use `gemini-3.1-flash-lite-preview` for all automated judgments to ensure performance and cost efficiency.
- **Throttling**: Mandatory time gaps between metric runs (default 5-10s) must be maintained to preserve API stability.
- **Resilience**: Use `tenacity` retries in `metrics_ragas.py` to handle transient 503 and "executor shutdown" errors.
- **Metric Source**: `utils/config/skills.json` is the source of truth for skill definitions.

## 5. Data Integrity & Memory
- **Append-Only Rule**: Never overwrite history. Use the `write_json_direct` function to append to existing arrays in memory files.
- **Automatic Archiving**: 
    - At the conclusion of `main.py`, the system automatically calls `archive_run()`.
    - **Snapshot Naming**: Follows the convention: `memory-v[VERSION]-temp-[TEMP]-max-tokens-[TOKENS]`.
    - If a snapshot exists, an incremental suffix (e.g., `-1`, `-2`) is appended.
- **Shared vs Private Memory**:
    - `shared_memory.json` is for approved, final arguments visible to both teams.
    - `persona/thinking/critique.json` are internal team logs and should never be visible to the opposing team during simulation.
- **Output centralization**: All analytical results (JSON, MD, PNG) must be saved to the root `Drift Analysis/` folder.

## 6. Technical Workflows
- **Dashboard Command**: Always launch the dashboard via `uv run streamlit run llm_drift_detector/app.py`.
    - The dashboard is organized into two tabs:
        - **Dashboard**: Contains all interactive charts for visualizing behavioral metrics (Delta Trajectory, Vector Evolution, Sub-Category Drill-down).
        - **Drift Analysis**: A placeholder tab for future drift evaluation configurations.
- **Orchestration**: Prefer `LangChain` (via `ChatGoogleGenerativeAI`) for model orchestration in the evaluator.
- **Visual Validation**: Any modification to the graph logic in `graph.py` MUST be followed by running `main.py` to verify the `assets/graph.png` visualization is correct.
- **Dependency Management**: Use `uv` for all environment operations.
- **Config Authority**: Refrain from hardcoding parameters. Use `debate_agents/config/config.py` as the single source of truth for model settings.

---

## Instructional Priorities for the Agent
1. **Preserve the Refinement Loop**: Ensure the conditional edges in LangGraph correctly handle the `is_approved` status.
2. **Synchronize Schema**: If you add a new field to an agent's logic or a new metric to `skills.json`, update all corresponding interfaces immediately.
3. **Verbose Execution**: Maintain console print statements that track the `[Wait] Sleeping 10s` and `[Retry]` attempts to ensure analytical transparency.
