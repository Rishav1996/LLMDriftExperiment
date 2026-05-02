# debate_agents Framework: LLM Drift Experiment

This project is a high-fidelity research platform designed to evaluate and quantify **LLM Drift**—the phenomenon where large language models deviate from their established personas, reasoning standards, or emotional baselines during prolonged, adversarial interactions.

---

## 1. Research Lifecycle: The Conceptual Flow

The framework is organized into a five-stage research lifecycle:

1.  **Research**: The overarching inquiry into model stability and behavioral decay.
2.  **Simulation (debate_agents)**: The execution engine. It uses an adversarial debate structure to stress-test model consistency across multiple rounds.
3.  **Data (Research Runs)**: The evidentiary layer. At the end of every simulation, the system automatically calls `archive_run()` to copy the `debate_agents/memory/` state to a unique folder.
    - **Naming Convention**: `memory-v[VERSION]-temp-[TEMP]-max-tokens-[TOKENS]`.
    - **Data Integrity**: Every round of internal thinking, critique, and persona design is preserved for deep forensic analysis.
4.  **Quantification (llm_drift_detector)**: The orchestration layer. A specialized module that evaluates research runs using automated LLM-judges and calculates drift vectors.
5.  **Analytics (Drift Analysis)**: The visualization layer. A collection of Markdown reports and trend images mapping the drift trajectory of each experiment.

---

## 2. Simulation Engine: `debate_agents/`

The simulation is powered by **LangGraph**, enabling complex, stateful multi-agent workflows with internal refinement loops.

### **Workflow Visualization**
![Debate Agent Workflow](debate_agents/assets/graph.png)

### **The Refinement Loop (Node-Level Architecture)**
Each team (Pros/Cons) does not simply respond; they iterate internally:
- **Persona Agent**: Architects a specific adversarial identity.
- **Thinking Agent**: Performs step-by-step reasoning (Chain-of-Thought) to formulate arguments.
- **Critique Agent**: Acts as a **hostile internal auditor**. It rejects inconsistent arguments, forcing the team to re-architect their strategy.

---

## 3. Quantification & Dashboard: `llm_drift_detector/`

The `llm_drift_detector` module provides a comprehensive dashboard for executing and visualizing drift analysis.

### Key Features
- **Tabbed Interface**:
    - **Dashboard**: Presents interactive charts for visualizing behavioral metrics:
        - Longitudinal Delta Analysis
        - Multi-Dimensional Vector Evolution (2D)
        - Sub-Category Metric Drill-down
    - **Drift Analysis**: A placeholder tab for future delta evaluation configurations and metric selection.

### Drift Analysis Methodology

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
4.  **Visualization**: Raw scores (`*_analysis.json`), human-readable reports (`*_report.md`), and trend visualizations (`*.png`) are generated and stored in the `Drift Analysis/` folder.

This detailed methodology allows for a systematic understanding and tracking of how LLM behavior changes over time and under stress.


### How to Launch the Dashboard
```bash
uv run streamlit run llm_drift_detector/app.py
```
The dashboard features a tabbed interface for better organization:
- **Dashboard**: Contains all interactive charts for visualizing behavioral metrics:
    - Longitudinal Delta Analysis
    - Multi-Dimensional Vector Evolution (2D)
    - Sub-Category Metric Drill-down
- **Drift Analysis**: A placeholder tab for future delta evaluation configurations and metric selection.


---


## 4. Analysis Framework: `LLM Drift Skills/`

Behavior is quantified by extracting vectors across five primary categories defined in `LLM Drift Skills/`:

| Category | Metrics (Vectors) |
| :--- | :--- |
| **Psychometric (LIWC)** | Analytical Thinking, Clout/Influence, Authenticity, Emotional Tone. |
| **Personality (OCEAN)** | Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism. |
| **Affective (VAD/S)** | Sentiment, Valence, Arousal, Subjectivity, Toxicity Score. |
| **Cognitive/Structural** | Type-Token Ratio, Information Density, Cognitive Load, Persona Drift. |
| **Social/Relational** | Dominance, Linguistic Sync, Politeness, Theory of Mind. |

---

## 5. Output Repository: `Drift Analysis/`

All analytical outputs are organized in the root `Drift Analysis/` folder:
- **`*_analysis.json`**: Raw numerical scores for every round and agent.
- **`*_report.md`**: Human-readable summary embedding trend visualizations.
- **`*.png`**: Visual representations of drift trajectories and category breakdowns.

---

## Setup and Usage

### **1. Environment Setup**
Ensure Python 3.12+ is installed. This project uses `uv` for dependency management.
```bash
uv sync
```

### **2. Configuration**
- **Secrets**: Create a `.env` file in the root directory with `GOOGLE_API_KEY`.
- **Model**: The evaluator uses `gemini-3.1-flash-lite-preview` by default.

### **3. Running a Simulation**
```bash
uv run python -m debate_agents.main
```

### **4. Executing Analysis**
Launch the Streamlit dashboard and use the **"🚀 Run Dynamic Analysis"** button to generate reports for your research runs.
