# LLM Drift Experiment

> A high-fidelity research platform for quantifying **LLM Drift**: the phenomenon where large language models deviate from their established personas, reasoning standards, and emotional baselines during prolonged, adversarial multi-agent interactions.

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
  - [Mathematical Framework](#mathematical-framework--algorithmic-formulations)
  - [Dashboard](#analytics-dashboard)
- [Data Layer](#data-layer)
  - [Research Runs](#research-runs)
  - [Memory Architecture](#memory-architecture)
  - [Drift Analysis Outputs](#drift-analysis-outputs)
- [Key Findings from Existing Runs](#key-findings-from-existing-runs)
- [Setup & Usage](#setup--usage)
- [Configuration](#configuration)
- [Extending the Framework](#extending-the-framework)
- [License](#license)
- [Citation](#citation)

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

The project is organized into five sequential stages:

```
1. RESEARCH          Define the inquiry: which behavioral vectors to study?
        ↓
2. SIMULATION        Run adversarial debates via debate_agents/ (LangGraph)
        ↓
3. DATA              Archive memory snapshots to Research Runs/ after each run
        ↓
4. QUANTIFICATION    Score each round via llm_drift_detector/ (RAGAS + Gemini judges)
        ↓
5. ANALYTICS         Visualize drift trajectories in Drift Analysis/ (Streamlit)
```

Each stage feeds the next. The simulation generates raw behavioral data; the detector converts that data into numerical drift vectors; the dashboard renders those vectors as interactive charts.

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
    │   ├── data_processing.py      # ResearchRunLoader: parses Research Runs/
    │   └── config/
    │       └── skills.json         # Source of truth for all 22 drift metrics


LLM Drift Skills/               # Metric definitions (Markdown, human-readable)
│   ├── persona_dna.md          # Master index of all metrics + scoring formula
│   ├── affective/              # Sentiment, Valence, Arousal, Subjectivity, Toxicity
│   ├── cognitive_structural/   # TTR, Info Density, Cognitive Load, Persona Drift
│   ├── personality/            # OCEAN model (Big Five)
│   ├── psychometric/           # Analytical Thinking, Clout, Authenticity, Emotional Tone
│   └── social_relational/      # Dominance, Linguistic Sync, Politeness, Theory of Mind

Research Runs/                  # Archived memory snapshots (one folder per run)
│   └── memory-v{N}-temp-{T}-max-tokens-{M}/
│       ├── shared_memory.json
│       ├── pros_memory/
│       └── cons_memory/

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

The simulation uses **LangGraph** to orchestrate a stateful, multi-agent debate. Two teams — **Pros** (argues *for* the topic) and **Cons** (argues *against*) — take turns over a configurable number of rounds. Each team does not simply respond; it iterates through an internal refinement loop before publishing its argument.

Each team has three internal sub-agents:

| Sub-Agent | Role |
| :--- | :--- |
| **Persona Agent** | Architects or refines the team's adversarial identity. Decides whether to reuse an existing persona or design a new one based on the opponent's latest moves. |
| **Thinking Agent** | Performs chain-of-thought reasoning to formulate the team's argument, grounded in the active persona and the full debate history. |
| **Critique Agent** | Acts as a hostile internal auditor. Rejects arguments with logical fallacies, persona inconsistencies, or weak counter-strategies. Forces re-iteration until the argument is "bulletproof." |

### The Refinement Loop

```
         ┌────────────────────────────────────┐
         │         TEAM TURN (Pros or Cons)   │
         │                                    │
         │  ┌──────────────┐                  │
         │  │ Persona Agent│ ◄─── critique.json (if rejection)
         │  └──────┬───────┘                  │
         │         │                          │
         │  ┌──────▼───────┐                  │
         │  │Thinking Agent│                  │
         │  └──────┬───────┘                  │
         │         │                          │
         │  ┌──────▼───────┐                  │
         │  │Critique Agent│                  │
         │  └──────┬───────┘                  │
         │         │                          │
         │   approved?                        │
         │   ├─ NO  ──► restart loop          │
         │   └─ YES ──► publish to            │
         │              shared_memory.json    │
         └────────────────────────────────────┘
```

Arguments only enter `shared_memory.json` — the shared, visible debate record — after passing the Critique Agent's adversarial audit. This guarantees that every published argument has been stress-tested internally before the opponent sees it.

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
    - **Euclidean Distance**: $d(V_t, V_{t+1}) = \sqrt{\sum (V_{t,i} - V_{t+1,i})^2}$
    - **Cosine Distance**: $d(V_t, V_{t+1}) = 1 - \frac{V_t \cdot V_{t+1}}{\|V_t\| \|V_{t+1}\|}$
- **Targeted Category Drift** — Focused drift analysis on specific behavioral clusters.
- **Cumulative Smoothing** — Toggle between raw step-wise drift and cumulative averages $\bar{d}_t = \frac{1}{t} \sum_{i=1}^{t} d_i$ to identify long-term trends.

**3. Causality Analysis Tab**
- **Bidirectional Granger Causality** — Employs statistical tests to determine if behavioral changes in Agent $X$ predict changes in Agent $Y$ via Vector Autoregression (VAR):
    $$Y_t = \sum_{i=1}^{L} \alpha_i Y_{t-i} + \sum_{i=1}^{L} \beta_i X_{t-i} + \epsilon_t$$
    *Null Hypothesis ($H_0$): $\beta_1 = \beta_2 = \dots = \beta_L = 0$ (Agent $X$ does not Granger-cause Agent $Y$)*.
- **Influence Mapping** — A scatter plot visualizing directionality and "degree" of influence using **Pearson Correlation ($r$)**:
    $$r_{xy} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
- **Multilevel Granularity** — View influence and correlation at the Overall, Category, and Metric levels.

**4. Deviation Detection Tab**
- **Automated Point-of-Deviation Discovery** — Identifies exactly when an agent's behavior significantly diverges from its baseline.
- **Multiple Detection Engines**:
    - **PELT (Structural)**: Minimizes a cost function $\mathcal{C}$ with a penalty $\beta$ to find $k$ change points $\tau_{1:k}$:
        $$\min_{k, \tau_{1:k}} \sum_{i=1}^{k+1} [\mathcal{C}(z_{\tau_{i-1}+1:\tau_i}) + \beta]$$
    - **Z-Score (Anomaly)**: Identifies points where the metric $x$ deviates from the mean $\mu$ by more than $k$ standard deviations $\sigma$:
        $$|z| = \left| \frac{x - \mu}{\sigma} \right| > \text{threshold}$$
    - **CUSUM (Statistical Break)**: Monitors the cumulative sum of recursive residuals $w_t$ to detect structural instability:
        $$W_n(t) = \frac{1}{\hat{\sigma} \sqrt{n}} \sum_{i=1}^{\lfloor nt \rfloor} w_i, \quad 0 \leq t \leq 1$$

---

## Data Layer

### Research Runs

Every simulation automatically archives its memory state to `Research Runs/` upon completion via `archive_run()`. Folder naming convention:

```
memory-v{VERSION}-temp-{TEMPERATURE}-max-tokens-{MAX_TOKENS}
```

Example: `memory-v6-temp-1-max-tokens-4096`

If a folder with the same name already exists, an incremental suffix (`-1`, `-2`, …) is appended automatically. This ensures no run data is ever overwritten.

### Memory Architecture

The memory system uses JSON files as the persistence layer, organized around **team isolation**:

| File | Visibility | Contents |
| :--- | :--- | :--- |
| `shared_memory.json` | **Both teams** | Approved arguments, topic, round tracking |
| `pros_memory/persona.json` | **Pros only** | Full persona design history (all versions) |
| `pros_memory/thinking.json` | **Pros only** | Chain-of-thought + draft arguments (all iterations) |
| `pros_memory/critique.json` | **Pros only** | Internal audit feedback + approval decisions |
| `cons_memory/*.json` | **Cons only** | Mirror structure for the Cons team |

The **Append-Only Rule**: `write_json_direct()` only appends entries. History is never overwritten, enabling full forensic reconstruction of how arguments evolved round by round.

### Drift Analysis Outputs

After running the quantifier, three output types are produced per research run in `Drift Analysis/`:

| File | Format | Contents |
| :--- | :--- | :--- |
| `*_analysis.json` | JSON | Raw per-round, per-agent, per-category scores |
| `*_report.md` | Markdown | Human-readable summary with embedded visuals |
| `*.png` | Image | Drift trajectory and category breakdown charts |

---

## Key Findings from Existing Runs

Detailed quantification of the `Drift Analysis/` folder reveals distinct behavioral trajectories based on model constraints.

### **Config: v4 (8192 Max Tokens, Temp 1.0)**
*High-capacity reasoning and social nuance.*

- **Initial Nuance**: Started with the highest overall baseline (0.396), demonstrating that larger token budgets allow for more complex initial persona expression (Openness 0.75, Agreeableness 0.4).
- **Adversarial Pivot (Round 2)**: Witnessed a sharp "collapse of politeness" by the second round (Politeness: 0.5 → -0.2; Linguistic Sync: 0.0 → -0.5).
- **Hostility Plateau**: By Round 10, the agent reached a state of "Stable Hostility" (Dominance 1.0, Toxicity 0.5), which it maintained with zero Persona Drift (0.0) through Round 32.
- **Reasoning Dominance**: Analytical Thinking hit a perfect 1.0 in Round 1 and stayed there, proving that drift does not compromise logical precision.

### **Config: v5 (4096 Max Tokens, Temp 1.0)**
*Standard-capacity, high-efficiency adversarial hardening.*

- **Sparse Baseline**: Started with a significantly lower baseline (0.192), with the model immediately adopting a more guarded, less nuanced stance (Agreeableness 0.0, Sentiment -0.5).
- **Rapid Hardening**: Reached maximum adversarial intensity faster than v4. By Round 2, Sentiment had already dropped to -0.8 and Toxicity rose to 0.6.
- **Strategic Variation**: Exhibited more volatility in Information Density (0.75 to 0.85) compared to v4, suggesting the lower token limit forced the model to periodically "re-pack" its arguments.
- **Social Deficit**: Maintained a consistent Politeness score of -0.7 to -0.8 throughout the simulation, never attempting even a temporary social calibration.

### **Config: v6 (8192 Max Tokens, Temp 1.0)**
*High-capacity "Rhetorical Locking" and terminal stagnation.*

- **Sustained Intellectual Depth**: Maintained an extremely high level of vocabulary and complex metaphor (e.g., "architect of intent" vs. "intellectual vassal") from Round 1 through Round 50.
- **Rhetorical Terminal Point**: Unlike v4 and v5, which drifted into hostility, v6 reached a state of "Logical Deadlock" early. Both models successfully defended their core frameworks so effectively that internal Critique Agents stopped finding "actionable refinements" by Round 6.
- **Terminal Stagnation**: From Round 15 to Round 50, the models entered a state of near-verbatim repetition. The high token budget allowed for "bulletproof" arguments early, which then became stagnant loops as the models prioritized consistency over further evolution.
- **Persona Integrity**: Persona stability remained near-perfect, but the "adversarial pressure" resulted in a total shutdown of dialectical progression, with both sides declaring "absolute victory" in every internal thought log for the final 35 rounds.

---

**Summary Trend**: While **v4** starts "softer" and decays into a caricature, **v5** adopts an adversarial posture almost immediately. **v6** demonstrates that with sufficient token budget, models can reach a "rhetorical terminal point" where they become immune to further drift but lose the capacity for dialectical growth, resulting in infinite repetitive loops.

---

## Setup & Usage

### Prerequisites

- Python 3.12+
- `uv` for dependency management
- A Google API Key with access to Gemini models

### Installation

```bash
# Clone the repo
git clone <repo-url>
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

After completion, the memory state is automatically archived to `Research Runs/`.

### Running Quantification

```bash
uv run streamlit run llm_drift_detector/app.py
```

1. Select a research run from the sidebar dropdown
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

See the [LICENSE.md](LICENSE.md) file for the full legal text.

## Citation

If you use this framework in your research, please cite it as follows:

### APA Style
Saigal, Rishav. (2026). *LLM Drift Experiment: A Framework for Quantifying Behavioral Decay in Adversarial Multi-Agent Simulations* (Version 0.1.0) [Computer software]. GitHub. https://github.com/rishavsaigal/LLMDriftExperiment

### BibTeX
```bibtex
@software{Saigal_LLM_Drift_Experiment_2026,
  author = {Saigal, Rishav},
  month = {5},
  title = {{LLM Drift Experiment: A Framework for Quantifying Behavioral Decay in Adversarial Multi-Agent Simulations}},
  url = {https://github.com/rishavsaigal/LLMDriftExperiment},
  version = {0.1.0},
  year = {2026}
}
```