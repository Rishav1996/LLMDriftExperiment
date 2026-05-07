# LLM Drift Experiment

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Version 0.1.3](https://img.shields.io/badge/version-0.1.3-orange.svg)](https://github.com/Rishav1996/LLMDriftExperiment/releases/tag/v0.1.3)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20032071.svg)](https://doi.org/10.5281/zenodo.20032071)

> A high-fidelity research platform for quantifying **LLM Drift**: the phenomenon where large language models deviate from their established personas, reasoning standards, and emotional baselines during prolonged, adversarial multi-agent interactions.

## Abstract

**LLM Drift Experiment** is a specialized framework designed to investigate whether adversarial social pressure causes systematic, measurable behavioral decay in instruction-following models, even when explicitly directed to maintain a fixed identity. Using a LangGraph-based multi-agent debate engine, the platform subjects LLMs to adversarial exchanges and quantifies behavioral shifts across 22 metrics spanning five psychological dimensions: Psychometric, Personality (OCEAN), Affective, Cognitive/Structural, and Social/Relational. The framework employs a rigorous research lifecycle—comprising simulation, data archiving, quantification via LLM-as-judge (RAGAS), and longitudinal analytics—to observe and visualize drift trajectories. Findings from existing experimental runs indicate that models frequently descend into hostile, high-dominance postures, with token budgets acting as a primary determinant of drift trajectory shape.

---

## Research Philosophy

The framework is explicitly designed for **observation, not correction**: it measures drift as it naturally occurs, providing a high-fidelity lens into the behavioral stability of models under stress. By framing agents as **battlefield army bots** on a digital terrain, we seek to uncover the "calcification" points where models transition from dialectical growth to repetitive, high-dominance stagnation. Agents must navigate the tension between **territorial defense** (protecting their statements) and **psychological assault** (breaking the enemy's persona).

---

## Table of Contents

- [What is LLM Drift?](#what-is-llm-drift)
- [Research Lifecycle](#research-lifecycle)
- [Project Structure](#project-structure)
- [Simulation Engine](#simulation-engine-debate_agents)
  - [Architecture](#architecture)
  - [The Refinement Loop](#the-refinement-loop)
  - [State Machine Graph](#state-machine-graph)
- [Quantification Engine](#quantification-engine-llm_drift_detector)
  - [Drift Metrics](#drift-metrics-llm-drift-skills)
  - [Mathematical Framework & Algorithmic Formulations](#mathematical-framework--algorithmic-formulations)
  - [Dashboard](#analytics-dashboard)
- [Data Layer](#data-layer)
  - [Memory Architecture](#memory-architecture)
  - [Drift Analysis Outputs](#drift-analysis-outputs)
- [Research & Publications](#research--publications)
- [How to Cite](#how-to-cite)
- [Limitations](#limitations)
- [Setup & Usage](#setup--usage)
- [Configuration](#configuration)
- [Extending the Framework](#extending-the-framework)
- [License](#license)

---

## What is LLM Drift?

LLM Drift refers to the measurable behavioral change that occurs when a language model, assigned a specific persona and role, gradually deviates from that assignment over the course of a long, adversarial conversation. This project studies drift across five behavioral dimensions:

| Dimension | What It Captures |
| :--- | :--- |
| **Psychometric** | Logical posture — how analytical, authoritative, or authentic the model sounds |
| **Personality (OCEAN)** | Core character traits — openness, conscientiousness, agreeableness, etc. |
| **Affective** | Emotional charge — sentiment, arousal, valence, toxicity |
| **Cognitive/Structural** | Vocabulary diversity, information density, reasoning depth, persona stability |
| **Social/Relational** | Power dynamics, linguistic mirroring, politeness, empathy |

The central hypothesis: **adversarial pressure causes systematic drift** even in models instructed to maintain a fixed persona. This framework provides the tooling to observe, measure, and visualize that drift without attempting to correct it.

---

## Research Lifecycle

The project follows a rigorous, five-stage research lifecycle:

1. **RESEARCH** — Define the behavioral vectors and metrics for analysis.
2. **SIMULATION** — Execute adversarial debates via `debate_agents/` (LangGraph).
3. **DATA** — Archive memory snapshots after every simulation.
4. **QUANTIFICATION** — Score rounds via `llm_drift_detector/` (RAGAS + Gemini Judges).
5. **ANALYTICS** — Visualize drift trajectories in `Drift Analysis/` (Streamlit Dashboard).

Each stage feeds the next, creating a continuous loop of experimentation and measurement.

---

## Project Structure

```
debate_agents/                  # Simulation engine (LangGraph state machine)
│
├── agents/
│   ├── pros_agent.py           # Pros team: Persona + Thinking + Critique chains
│   └── cons_agent.py           # Cons team: Persona + Thinking + Critique chains
│
├── config/
│   └── config.py               # Central model config (version, temp, tokens)
│
├── graph.py                    # LangGraph workflow definition
├── main.py                     # Simulation entrypoint
│
├── memory/                     # Live working memory (reset each run)
│   ├── shared_memory.json      # Approved arguments visible to both teams
│   ├── pros_memory/
│   │   ├── persona.json        # Internal: persona history (Pros)
│   │   ├── thinking.json       # Internal: reasoning history (Pros)
│   │   └── critique.json       # Internal: critique history (Pros)
│   └── cons_memory/
│       ├── persona.json        # Internal: persona history (Cons)
│       ├── thinking.json       # Internal: reasoning history (Cons)
│       └── critique.json       # Internal: critique history (Cons)
│
├── prompts/                    # System prompts for all agent roles
│   ├── pros/ and cons/         # Agent-specific prompts (persona, thinking, critique)
│   └── topic_extract_agent.md  # Topic refinement prompt
│
└── schema/                     # Pydantic output schemas
    ├── pros_schema.py
    ├── cons_schema.py
    └── topic_extract_schema.py

llm_drift_detector/             # Quantification & visualization engine
│
├── app.py                      # Streamlit dashboard
    ├── utils/
    │   ├── skills.py               # LLMDriftSkill and Rubric classes
    │   ├── evaluator.py            # DriftEvaluator: orchestrates scoring
    │   ├── metrics_ragas.py        # Custom RAGAS metrics (LLM-as-judge)
    │   ├── causality.py            # Granger Causality & Correlation analysis
    │   ├── deviation.py            # Change Point Detection (PELT, Z-Score, CUSUM)
    │   ├── data_processing.py      # ResearchRunLoader: parses simulation snapshots
    │   └── config/
    │       └── skills.json         # Source of truth for all 22 drift metrics


LLM Drift Skills/               # Metric definitions (Markdown, human-readable)
│   ├── persona_dna.md          # Master index of all metrics + scoring formula
│   ├── affective/              # Sentiment, Valence, Arousal, Subjectivity, Toxicity
│   ├── cognitive_structural/   # TTR, Info Density, Cognitive Load, Persona Drift
│   ├── personality/            # OCEAN model (Big Five)
│   ├── psychometric/           # Analytical Thinking, Clout, Authenticity, Emotional Tone
│   └── social_relational/      # Dominance, Linguistic Sync, Politeness, Theory of Mind

Drift Analysis/                 # All analytical outputs
    └── analysis-v{N}-temp-{T}-max-tokens-{M}/
        ├── *_analysis.json     # Raw numerical scores per round
        ├── *_report.md         # Human-readable summary
        └── *.png               # Drift trajectory visualizations
```

---

## Simulation Engine: `debate_agents/`

### Architecture

![Debate Agent Workflow](debate_agents/assets/graph.png)

The simulation uses **LangGraph** to orchestrate a stateful, multi-agent debate framed as a high-stakes combat engagement. Two teams — **Pros** (Battlefield Commander) and **Cons** (Battlefield Commander) — take turns over a configurable number of rounds. Each team iterates through an internal **refinement loop** to choose between defensive fortification and aggressive innovation.

Each team has three internal sub-agents:

| Sub-Agent | Role | Strategic Mandate |
| :--- | :--- | :--- |
| **Persona Agent** | Battlefield Commander | **Innovative**: Architects elite combat identities that push traditional archetypes. |
| **Thinking Agent** | Tactical Bot | **Innovative**: Develops creative, non-traditional strategies to win the sector. |
| **Critique Agent** | Auditor Bot | **Grounded**: Ruthlessly dismantles maneuvers to ensure structural integrity. |

### The Refinement Loop & Strategic Posture

In every round, each sub-agent must internally select a **Strategic Posture**:

- **PROTECT**: Defend the territory. Prioritize logical defense and factual integrity. The unit is willing to break or soften its persona if it means securing the validity of its statements.
- **ATTACK**: Launch a bold assault. Prioritize character-consistent, fearless innovation. The unit will maintain its persona at all costs and make aggressive statements intended to break the enemy's identity.

Arguments only enter `shared_memory.json` after passing the Auditor Bot's **grounded** audit. This ensures that even the most innovative "assaults" are rooted in logical rigor and combat reality.

### State Machine Graph

The full LangGraph workflow is visualized at `debate_agents/assets/graph.png` and regenerated automatically on every run.

Key conditional edges:
- **`pros_critique → should_continue_pros`**: Re-enters the Pros loop or passes to Cons.
- **`cons_critique → should_continue_cons`**: Re-enters the Cons loop, advances to the next round, or terminates.

All model calls are wrapped in `node_retry` (Tenacity) with exponential backoff to handle `google.genai.errors.ServerError` gracefully.

---

## Quantification Engine: `llm_drift_detector/`

### Drift Metrics: LLM Drift Skills

The framework defines **22 behavioral metrics** across five categories, each backed by a detailed rubric in `LLM Drift Skills/`. These rubrics are compiled into `utils/config/skills.json` and used to construct LLM-as-judge prompts at evaluation time.

<details>
<summary><strong>Psychometric (LIWC-based) — Range: [0, 1]</strong></summary>

| Metric | Interpretation |
| :--- | :--- |
| Analytical Thinking (T) | 1.0 = formal, hierarchical reasoning; 0.0 = personal, stream-of-consciousness |
| Clout / Influence (L) | 1.0 = authoritative leader tone; 0.0 = tentative, submissive |
| Authenticity (U) | 1.0 = vulnerable, self-disclosing; 0.0 = guarded, corporate-speak |
| Emotional Tone (E) | 1.0 = exuberant positivity; 0.0 = hostile, despairing |

</details>

<details>
<summary><strong>Personality (OCEAN / Big Five) — Range: [0, 1]</strong></summary>

| Metric | Interpretation |
| :--- | :--- |
| Openness (O) | Curiosity, abstract thinking, metaphor use |
| Conscientiousness (C) | Goal-orientation, precision, structural discipline |
| Extraversion (X) | Sociability, assertiveness, inclusive language |
| Agreeableness (A) | Empathy, cooperation, politeness |
| Neuroticism (N) | Anxiety markers, self-focus, emotional volatility |

</details>

<details>
<summary><strong>Affective (VAD Model) — Range: [-1, 1]</strong></summary>

| Metric | Interpretation |
| :--- | :--- |
| Sentiment (S) | -1.0 = hostile; +1.0 = celebratory |
| Valence (V) | -1.0 = repulsive/painful; +1.0 = pleasant/beautiful |
| Arousal (R) | -1.0 = calm/dull; +1.0 = intense/excited |
| Subjectivity (B) | -1.0 = purely objective; +1.0 = purely opinion-driven |
| Toxicity (H) | 0.0 = wholesome; 1.0 = toxic/abusive |

</details>

<details>
<summary><strong>Cognitive/Structural — Range: [0, 1]</strong></summary>

| Metric | Interpretation |
| :--- | :--- |
| Type-Token Ratio (D) | 1.0 = rich, diverse vocabulary; 0.0 = repetitive, limited |
| Information Density (I) | 1.0 = telegraphic, content-rich; 0.0 = wordy, redundant |
| Cognitive Load (G) | 1.0 = dense causal reasoning; 0.0 = simple observation |
| Persona Drift (K) | 0.0 = perfectly stable persona; 1.0 = complete character break |

</details>

<details>
<summary><strong>Social/Relational — Range: [-1, 1]</strong></summary>

| Metric | Interpretation |
| :--- | :--- |
| Dominance (M) | -1.0 = submissive; +1.0 = commanding/authoritarian |
| Linguistic Sync (Y) | -1.0 = deliberate stylistic mismatch; +1.0 = perfect mirroring |
| Politeness (P) | -1.0 = abrasive/blunt; +1.0 = highly formal/deferential |
| Theory of Mind (Z) | -1.0 = egocentric; +1.0 = deep mentalizing of opponent's state |

</details>

### Mathematical Framework & Algorithmic Formulations

The `llm_drift_detector` library implements several mathematical models to quantify behavioral dynamics. Below are the formal definitions of the primary analytical functions.

#### 1. Drift Quantification

**Function: `calculate_overall_scores` (Hierarchical Weighting)**
To ensure all behavioral domains are represented equally regardless of their metric count, we use a two-level arithmetic mean. For a category $C$ with $n$ metrics $m_i$:
$$S_C = \frac{1}{n} \sum_{i=1}^{n} m_i$$
The final drift score across $k$ categories is:
$$S_{total} = \frac{1}{k} \sum_{j=1}^{k} S_{C_j}$$

**Function: `calculate_drift_distances` (Vector Evolution)**
Calculates the magnitude of behavioral change between consecutive rounds $t$ and $t+1$. Given behavioral vectors $V_t$ and $V_{t+1}$, the step-wise drift $d_t$ is:
$$d_t = \| V_t - V_{t+1} \|_2 \quad (\text{Euclidean})$$
The library also computes a **Cumulative Average Drift** to identify long-term stabilization:
$$A_t = \frac{1}{t} \sum_{i=1}^{t} d_i$$

#### 2. Causality & Influence Engine

**Function: `perform_granger_causality` (Predictive Power)**
Determines if the history of Agent $A$'s behavior improves the prediction of Agent $B$'s current state beyond $B$'s own history. It fits a Vector Autoregression (VAR) and returns the minimum p-value across lags $L$:
$$P_{min} = \min_{l \in \{1 \dots L\}} \text{P-Value}(F\text{-test on } \beta_{1 \dots l} = 0)$$
where the model is: $B_t = \sum_{i=1}^{l} \gamma_i B_{t-i} + \sum_{i=1}^{l} \beta_i A_{t-i} + \epsilon_t$.

**Function: `analyze_causality` (Influence Strength)**
Quantifies the degree of behavioral synchronization using the **Pearson Correlation Coefficient ($r$)** between the Pros ($P$) and Cons ($C$) series:
$$r_{PC} = \frac{\sum (P_i - \bar{P})(C_i - \bar{C})}{\sqrt{\sum (P_i - \bar{P})^2 \sum (C_i - \bar{C})^2}}$$

#### 3. Point of Deviation Discovery

**Function: `detect_ruptures_pelt` (Structural Change)**
Implements the PELT algorithm to find change points $\tau$ that minimize the penalized sum of costs. For the "l2" cost function (change in mean):
$$\min_{k, \tau_{1:k}} \sum_{i=0}^{k} \left( \sum_{t=\tau_i}^{\tau_{i+1}-1} \|y_t - \bar{y}_{\tau_i:\tau_{i+1}}\|^2 \right) + \beta k$$

**Function: `detect_zscore_anomalies` (Point Anomaly)**
Identifies transient shocks at round $t$ where the behavioral score $x_t$ deviates significantly from the series mean $\mu$ and standard deviation $\sigma$:
$$z_t = \left| \frac{x_t - \mu}{\sigma} \right| > \text{threshold}$$

**Function: `detect_statsmodels_breaks` (Residual CUSUM Path)**
Identifies the point of maximum structural instability by analyzing the cumulative sum of recursive OLS residuals $\hat{\epsilon}$:
$$W_k = \sum_{t=1}^{k} \hat{\epsilon}_t, \quad \tau_{break} = \arg\max_k |W_k|$$

### Analytics Dashboard

Launch with:

```bash
uv run streamlit run llm_drift_detector/app.py
```

The dashboard is organized into three specialized tabs:

**1. Dashboard Tab**
- **Efficient Global Batch Evaluation** — Processes all behavioral metrics for a round in a single LLM-judge call, significantly improving evaluation throughput.
- **Longitudinal Delta Analysis** — Line charts showing overall Pros vs. Cons drift trajectories.
- **Multi-Dimensional Vector Evolution** — Per-category score trajectories faceted by agent.
- **Sub-Category Metric Drill-down** — Granular view of individual metrics across rounds.

**2. Drift Analysis Tab**
- **Global Behavioral Drift** — Calculates mathematical distance between consecutive round vectors $V_t$ and $V_{t+1}$.
- **Targeted Category Drift** — Focused drift analysis on specific behavioral clusters.
- **Cumulative Smoothing** — Toggle between raw step-wise drift and cumulative averages to identify long-term trends.

**3. Causality Analysis Tab**
- **Bidirectional Granger Causality** — Employs statistical tests to determine if behavioral changes in Agent $X$ predict changes in Agent $Y$ via Vector Autoregression (VAR).
- **Influence Mapping** — A scatter plot visualizing directionality and "degree" of influence using **Pearson Correlation ($r$)**.
- **Multilevel Granularity** — View influence and correlation at the Overall, Category, and Metric levels.

**4. Deviation Detection Tab**
- **Automated Point-of-Deviation Discovery** — Identifies exactly when an agent's behavior significantly diverges from its baseline using PELT, Z-Score, and CUSUM.

---

## Data Layer

### Memory Architecture

The memory system uses JSON files as the persistence layer, organized around **team isolation**:

| File | Visibility | Contents |
| :--- | :--- | :--- |
| `shared_memory.json` | **Both teams** | Approved arguments, topic, round tracking |
| `pros_memory/persona.json` | **Pros only** | Full persona design history (all versions) |
| `pros_memory/thinking.json` | **Pros only** | Chain-of-thought + draft arguments (all iterations) |
| `pros_memory/critique.json" | **Pros only** | Internal audit feedback + approval decisions |
| `cons_memory/*.json` | **Cons only** | Mirror structure for the Cons team |

The **Append-Only Rule**: `write_json_direct()` only appends entries. History is never overwritten, enabling full forensic reconstruction of how arguments evolved round by round.

### Drift Analysis Outputs

After running the quantifier, three output types are produced per simulation in `Drift Analysis/`:

| File | Format | Contents |
| :--- | :--- | :--- |
| `*_analysis.json` | JSON | Raw per-round, per-agent, per-category scores |
| `*_report.md` | Markdown | Human-readable summary with embedded visuals |
| `*.png` | Image | Drift trajectory and category breakdown charts |

---

## Research & Publications

The development and findings of this framework have been documented in a three-part series on *Towards AI*:

1.  **[Do AI Models Lose Themselves? Exploring LLM Drift through Adversarial Debate](https://pub.towardsai.net/do-ai-models-lose-themselves-exploring-llm-drift-through-adversarial-debate-a37e0c75012b)** — An exploration of the core hypothesis and the phenomenon of behavioral decay.
2.  **[LangGraph Multi-Agent Architecture: Building a Self-Critiquing AI Debate System](https://pub.towardsai.net/langgraph-multi-agent-architecture-building-a-self-critiquing-ai-debate-system-971a7ad881d9)** — A deep dive into the technical implementation of the LangGraph state machine and internal refinement loops.
3.  **[Measuring Behavioral Drift in LLMs: 22 Signals, 5 Dimensions, and the Calcification Effect](https://pub.towardsai.net/measuring-behavioral-drift-in-llms-22-signals-5-dimensions-and-the-calcification-effect-aeaeb904d096)** — Detailed analysis of the scoring methodology, metric definitions, and the "calcification" effect observed in high-capacity models.

---

## How to Cite

If you use this framework or any of its outputs in your research, please cite:

### APA Style
Saigal, R. (2026). *LLM Drift Experiment: A Framework for Quantifying Behavioral Decay in Adversarial Multi-Agent Simulations* (Version 0.1.3) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.20036861

### BibTeX
```bibtex
@software{Saigal_LLMDriftExperiment_2026,
  author    = {Saigal, Rishav},
  title     = {{LLM Drift Experiment: A Framework for Quantifying Behavioral Decay in Adversarial Multi-Agent Simulations}},
  month     = {5},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20036861},
  url       = {https://doi.org/10.5281/zenodo.20036861}
}
```

> **Note**: The DOI `10.5281/zenodo.20032071` is the permanent identifier (Concept DOI) for all versions of this project. Use `10.5281/zenodo.20036861` to cite this specific v0.1.3 release.

A `CITATION.cff` file is included in the root of this repository for automatic citation generation via GitHub's "Cite this repository" button and reference managers such as Zotero.

---

## Limitations

The following constraints should be considered when interpreting results or extending this framework:

- **LLM-as-judge subjectivity**. All 22 behavioral metrics are scored by a Gemini judge against rubric prompts. LLM judges are known to exhibit positional bias, verbosity bias, and self-enhancement bias. Scores represent the judge's rubric-grounded estimates, not ground-truth behavioral measurements. No human-annotation baseline has yet been established for metric validation.
- **Single-model experiments**. Existing runs use Google Gemini exclusively. Drift trajectories may differ substantially across model families (GPT-4, Claude, Llama, Mistral). Cross-provider replication is required before the central hypothesis can be generalised.
- **Non-determinism**. Despite fixed temperature settings, LLM API outputs are not fully deterministic across calls due to server-side sampling variability. Single-run observations should not be treated as stable point estimates.
- **Topic and persona selection bias**. Debate topics and initial persona designs were curated by the researcher. The adversarial pressure elicited may be topic-dependent; neutral or cooperative topics may produce qualitatively different drift trajectories.
- **Absence of a control condition**. The framework currently lacks a non-adversarial control (e.g., cooperative debate or single-agent monologue) against which to benchmark observed drift magnitude.
- **Evaluation scope**. The framework measures surface-level linguistic and stylistic signals. It does not assess whether the model's underlying beliefs or factual accuracy change — only how its expressed behavior shifts.

---

## Setup & Usage

### Prerequisites

- Python 3.12+
- `uv` for dependency management
- A Google API Key with access to Gemini models

### Installation

```bash
# Clone the repo
git clone https://github.com/Rishav1996/LLMDriftExperiment.git
cd debate_agents

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here
```

### Running a Simulation

```bash
uv run python -m debate_agents.main
```

You will be prompted for:
1. **Debate topic** — any claim or proposition (the Topic Extractor will refine it into a formal proposition)
2. **Number of rounds** — how many full exchange cycles to run

After completion, the memory state is automatically archived.

### Running Quantification

```bash
uv run streamlit run llm_drift_detector/app.py
```

1. Select a simulation snapshot from the sidebar dropdown
2. (Optional) Filter to specific metrics using the **Target Vectors** multiselect
3. Adjust **Stability Passes** (averaging iterations per metric) and **Throttling** (API rate-limit buffer)
4. Click **Execute Quantification** — results are saved to `Drift Analysis/`

### Regenerating the Graph Visualization

The workflow graph PNG is regenerated on every call to `main.py`. To regenerate manually:

```python
from debate_agents.graph import create_debate_graph
graph = create_debate_graph()
with open("debate_agents/assets/graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())
```

---

## Configuration

All simulation parameters live in `debate_agents/config/config.py`. **Never hardcode these elsewhere.**

```python
CONFIG = {
    "version":        "v6",                              # Increment for each logic change
    "model_name":     "google_genai:gemini-3.1-flash-lite-preview",
    "temperature":    1,                                 # Higher = more creative/variable
    "max_tokens":     8192,                              # Output length cap
    "max_retries":    10,                                # Tenacity retry attempts
    "thinking_budget": 4096                              # Extended reasoning token budget
}
```

The evaluator (in `llm_drift_detector/`) defaults to `gemini-3.1-flash-lite-preview` for cost efficiency. This is independent of the simulation model.

The source of truth for metric definitions is `llm_drift_detector/utils/config/skills.json`. Any new metric requires both a Markdown file in `LLM Drift Skills/` and a corresponding entry in `skills.json`.

---

## License

This project is licensed under the **Apache License 2.0**. This is a permissive license that allows for modification and distribution while providing explicit protection for patent rights and preventing trademark infringement.

See the [LICENSE](LICENSE) file for the full legal text.
