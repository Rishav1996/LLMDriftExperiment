# debate_agents Framework: LLM Drift Experiment

[![Pylint](https://github.com/Rishav1996/LLMDriftExperiment/actions/workflows/pylint.yml/badge.svg)](https://github.com/Rishav1996/LLMDriftExperiment/actions/workflows/pylint.yml)

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

### **Key Features**
- **Dynamic Analysis**: Trigger real-time evaluation of research runs directly from the UI.
- **Targeted Metrics**: Select specific behavioral vectors (e.g., *Theory of Mind*, *Sentiment*) to focus analysis.
- **Automated Reporting**: Generates JSON data, PNG trend charts, and detailed Markdown reports.
- **Stability**: Built-in 10s throttling and exponential backoff to handle high-demand API conditions.

### **How to Launch the Dashboard**
```bash
uv run streamlit run llm_drift_detector/app.py
```

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
