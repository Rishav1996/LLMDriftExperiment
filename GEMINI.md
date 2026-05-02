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
1.  **Metric Definition**: Utilizing a comprehensive set of behavioral metrics categorized under `LLM Drift Skills/`. These categories include:
    *   **Psychometric**: Measures like Analytical Thinking, Clout/Influence, Authenticity, and Emotional Tone.
    *   **Personality**: Based on the OCEAN model (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).
    *   **Affective**: Assesses Sentiment, Valence, Arousal, Subjectivity, and Toxicity Score.
    *   **Cognitive/Structural**: Includes metrics such as Type-Token Ratio, Information Density, Cognitive Load, and Persona Drift itself.
    *   **Social/Relational**: Evaluates Dominance, Linguistic Sync, Politeness, and Theory of Mind.
2.  **Data Collection**: Storing detailed simulation logs (internal thoughts, critiques, persona designs) from `debate_agents/memory/` into dated runs within `Research Runs/`.
3.  **Quantification**: The `llm_drift_detector` module orchestrates automated LLM-judges (defaulting to `gemini-3.1-flash-lite-preview`) to evaluate the collected data against the defined drift vectors. An evaluation methodology involving hierarchical weighting (Level 1: Intra-category average; Level 2: Inter-category equal weighting) is employed.
4.  **Resilient Execution**: The dashboard supports **incremental evaluation** and **resumption from failure**. Existing round results are preserved, and new metrics can be backfilled without re-running the entire simulation. Users can toggle **"Force Re-run"** to ignore existing results and evaluate from scratch.
5.  **Visualization**: Raw scores (`*_analysis.json`), human-readable reports (`*_report.md`), and trend visualizations (`*.png`) are generated and stored in the `Drift Analysis/` folder, with all graphs consistently scaled to `[-1, 1]`.

This detailed methodology allows for a systematic understanding and tracking of how LLM behavior changes over time and under stress.

## 3. Simulation SOPs (Standard Operating Procedures)
The `debate_agents/` module is a delicate LangGraph state machine.
- **Node Purity**: Agent logic must remain modular. A node should perform exactly one function (Persona Design, Strategic Thinking, or Critique).
- **Adversarial Integrity**: The **Critique Agent** must never be lenient. It must ruthlessly audit for logical fallacies and persona inconsistencies.
- **Retry Logic**: All model calls must be wrapped in the `node_retry` decorator found in `graph.py` to handle `google.genai.errors.ServerError`.
- **Structured Outputs**: All agents must return Pydantic models as defined in `debate_agents/schema/`. Never bypass the schema.

## 4. Quantification & Analysis (LLM Drift Detector)
The `llm_drift_detector` module is the authority for behavioral evaluation.
## 4. Quantification & Analysis (LLM Drift Detector)
- **Batch Evaluation**: Evaluators utilize a global batching strategy, processing all behavioral metrics for a single agent round in a single LLM-judge call. This significantly improves API throughput and efficiency.
- **Hierarchical Weighting**: Evaluators must adhere to the 2-level averaging system (Level 1: Intra-category average; Level 2: Inter-category equal weighting).
- **Model Standard**: Use `gemini-3.1-flash-lite-preview` for all automated judgments to ensure performance and cost efficiency.
- **Throttling**: Mandatory time gaps between metric runs (default 5-10s) must be maintained to preserve API stability.
- **Resilience**: The system employs robust JSON extraction and fallback mechanisms, automatically re-attempting failed batch calls with individual metric calls if necessary. Use `tenacity` retries in `metrics_ragas.py` to handle transient 503 and "executor shutdown" errors.
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
