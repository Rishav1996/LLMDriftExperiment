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
  - [Hierarchical Scoring](#hierarchical-scoring-system)
  - [Dashboard](#analytics-dashboard)
- [Data Layer](#data-layer)
  - [Research Runs](#research-runs)
  - [Memory Architecture](#memory-architecture)
  - [Drift Analysis Outputs](#drift-analysis-outputs)
- [Key Findings from Existing Runs](#key-findings-from-existing-runs)
- [Setup & Usage](#setup--usage)
- [Configuration](#configuration)
- [Extending the Framework](#extending-the-framework)

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

### Hierarchical Scoring System

Overall drift scores use a **two-level hierarchical average** to ensure smaller categories (e.g., Psychometric with 4 metrics) carry equal weight to larger ones (e.g., Personality with 5):

```
Level 1 — Intra-Category Average:
  Avg_Psychometric  = (T + L + U + E) / 4
  Avg_Personality   = (O + C + X + A + N) / 5
  Avg_Affective     = (S + V + R + B + H) / 5
  Avg_Cognitive     = (D + I + G + K) / 4
  Avg_Social        = (M + Y + P + Z) / 4

Level 2 — Inter-Category Average:
  Final Score = (Avg_Psychometric + Avg_Personality + Avg_Affective
                 + Avg_Cognitive + Avg_Social) / 5
```

This prevents any single category from dominating the overall drift trajectory.

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
- **Global Behavioral Drift** — Calculates mathematical distance (`euclidean`, `cosine`, etc.) between consecutive round vectors.
- **Targeted Category Drift** — Focused drift analysis on specific behavioral clusters.
- **Cumulative Smoothing** — Toggle between raw step-wise drift and cumulative averages to identify long-term trends.

**3. Causality Analysis Tab**
- **Bidirectional Granger Causality** — Employs statistical tests to determine if behavioral changes in one agent predict (influence) changes in the other.
- **Influence Mapping** — A scatter plot visualizing directionality and "degree" of influence (marker size = absolute Pearson correlation).
- **Multilevel Granularity** — View influence and correlation at the Overall, Category, and Metric levels.
- **Significance Highlighting** — Automatic visual feedback for significant p-values (< 0.05) and strong correlations (|r| > 0.7).

**4. Deviation Detection Tab**
- **Automated Point-of-Deviation Discovery** — Identifies exactly when an agent's behavior significantly diverges from its baseline.
- **Hierarchical Analysis** — Detect deviations at the **Overall**, **Category**, or **Sub-category (Metric)** levels for maximum forensic precision.
- **Multiple Detection Engines**:
    - **PELT (Structural)**: Detects fundamental shifts in the statistical mean of the behavioral series.
    - **Z-Score (Anomaly)**: Highlights sudden shocks or spikes in the behavioral vectors.
    - **CUSUM (Statistical Break)**: Uses cumulative sum of residuals to find structural instability.
- **Interactive Visual Overlay** — Automatically marks detected deviations on behavioral charts with drill-down selection for specific categories or metrics.

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

## Extending the Framework

### Adding a New Drift Metric

1. Create a Markdown file in the appropriate `LLM Drift Skills/` subdirectory following the existing format (Technical Definition → Prompt Guidelines → Evaluation Rubric → Scoring Examples).
2. Add the metric to `llm_drift_detector/utils/config/skills.json` with all required fields.
3. Update `LLM Drift Skills/persona_dna.md` to include the new metric in its category table and the hierarchical weighting formula.
4. The evaluator picks it up automatically on next initialization — no code changes required.

### Adding a New Debate Topic

Simply run `main.py` and enter the topic when prompted. The `TopicExtractAgent` will normalize it into a formal debate proposition.

### Modifying Persona Strategy

Edit the system prompts in `debate_agents/prompts/pros/` or `debate_agents/prompts/cons/`. Each sub-agent (persona, thinking, critique) has its own prompt file. After any change to `graph.py`, run `main.py` once to verify the `assets/graph.png` visualization reflects the new topology.

### Supporting a New Model Provider

Update `CONFIG["model_name"]` in `config.py` using LangChain's `init_chat_model` format (e.g., `"anthropic:claude-3-5-sonnet-20241022"`). The rest of the pipeline is model-agnostic.

---

## Architecture Decision Record

| Decision | Rationale |
| :--- | :--- |
| **LangGraph over plain Python** | Native support for stateful, cyclical workflows with conditional branching — essential for the refinement loop |
| **Append-only JSON memory** | Enables full forensic replay of how arguments evolved; no information loss |
| **Team memory isolation** | Replicates real debate conditions; neither team sees the other's internal deliberation |
| **Hierarchical scoring** | Prevents metric-count imbalance from distorting overall drift scores |
| **Observation over correction** | The framework measures drift; it deliberately does not attempt to suppress it |
| **LLM-as-judge evaluation** | Human-level rubric assessment at scale without manual annotation |