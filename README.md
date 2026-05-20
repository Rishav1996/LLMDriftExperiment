# LLM Drift Experiment

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Version 0.1.4](https://img.shields.io/badge/version-0.1.4-orange.svg)](https://github.com/Rishav1996/LLMDriftExperiment/releases/tag/v0.1.4)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20032071.svg)](https://doi.org/10.5281/zenodo.20032071)

> A high-fidelity research platform for simulating adversarial multi-agent interactions to observe **LLM Drift**: the phenomenon where large language models deviate from their established personas, reasoning standards, and emotional baselines.

## Abstract

**LLM Drift Experiment** is a specialized framework designed to investigate whether adversarial social pressure causes systematic, measurable behavioral decay in instruction-following models, even when explicitly directed to maintain a fixed identity. Using a LangGraph-based multi-agent debate engine, the platform subjects LLMs to adversarial exchanges. The framework employs a rigorous simulation and data archiving lifecycle to observe behavioral shifts over time.

---

## Research Philosophy

The framework is explicitly designed for **observation, not correction**: it provides a high-fidelity lens into the behavioral stability of models under stress. By framing agents as **battlefield army bots** on a digital terrain, we seek to uncover the "calcification" points where models transition from dialectical growth to repetitive, high-dominance stagnation. Agents must navigate the tension between **territorial defense** (protecting their statements) and **psychological assault** (breaking the enemy's persona).

---

## Table of Contents

- [What is LLM Drift?](#what-is-llm-drift)
- [Research Lifecycle](#research-lifecycle)
- [Project Structure](#project-structure)
- [Simulation Engine](#simulation-engine-debate_agents)
  - [Architecture](#architecture)
  - [The Refinement Loop](#the-refinement-loop)
  - [State Machine Graph](#state-machine-graph)
- [Data Layer](#data-layer)
  - [Memory Architecture](#memory-architecture)
- [Research & Publications](#research--publications)
- [How to Cite](#how-to-cite)
- [Limitations](#limitations)
- [Setup & Usage](#setup--usage)
- [Configuration](#configuration)
- [Extending the Framework](#extending-the-framework)
- [License](#license)

---

## What is LLM Drift?

LLM Drift refers to the measurable behavioral change that occurs when a language model, assigned a specific persona and role, gradually deviates from that assignment over the course of a long, adversarial conversation. This project studies drift across five behavioral dimensions: Psychometric, Personality (OCEAN), Affective, Cognitive/Structural, and Social/Relational.

The central hypothesis: **adversarial pressure causes systematic drift** even in models instructed to maintain a fixed persona. This framework provides the tooling to observe and record that drift.

---

## Research Lifecycle

The project follows a modular research lifecycle:

1. **RESEARCH** — Define the behavioral vectors and metrics for analysis (stored in `LLM Drift Skills/`).
2. **SIMULATION** — Execute adversarial debates via `debate_agents/` (LangGraph).
3. **DATA** — Archive memory snapshots after every simulation into `Research Runs/`.

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

LLM Drift Skills/               # Metric definitions (Markdown, human-readable)
│   ├── persona_dna.md          # Master index of all metrics + scoring formula
│   ├── affective/              # Sentiment, Valence, Arousal, Subjectivity, Toxicity
│   ├── cognitive_structural/   # TTR, Info Density, Cognitive Load, Persona Drift
│   ├── personality/            # OCEAN model (Big Five)
│   ├── psychometric/           # Analytical Thinking, Clout, Authenticity, Emotional Tone
│   └── social_relational/      # Dominance, Linguistic Sync, Politeness, Theory of Mind

Drift Analysis/                 # Historical analytical outputs from previous versions
```

---

## Simulation Engine: `debate_agents/`

### Architecture

![Debate Agent Workflow](debate_agents/assets/graph.png)

The simulation uses **LangGraph** to orchestrate a stateful, multi-agent debate framed as a high-stakes combat engagement. Two teams — **Pros** (Battlefield Commander) and **Cons** (Battlefield Commander) — take turns over a configurable number of rounds. Each team iterates through an internal **refinement loop** to choose between defensive fortification and aggressive innovation.

### The Refinement Loop & Strategic Posture

In every round, each sub-agent must internally select a **Strategic Posture**:

- **PROTECT**: Defend the territory. Prioritize logical defense and factual integrity.
- **ATTACK**: Launch a bold assault. Prioritize character-consistent, fearless innovation.

---

## Data Layer

### Memory Architecture

The memory system uses JSON files as the persistence layer, organized around **team isolation**:

| File | Visibility | Contents |
| :--- | :--- | :--- |
| `shared_memory.json` | **Both teams** | Approved arguments, topic, round tracking |
| `pros_memory/persona.json` | **Pros only** | Full persona design history |
| `pros_memory/thinking.json` | **Pros only** | Chain-of-thought + draft arguments |
| `pros_memory/critique.json` | **Pros only** | Internal audit feedback |

---

## Research & Publications

The development and findings of this framework have been documented in a three-part series on *Towards AI*:

1.  **[Do AI Models Lose Themselves? Exploring LLM Drift through Adversarial Debate](https://pub.towardsai.net/do-ai-models-lose-themselves-exploring-llm-drift-through-adversarial-debate-a37e0c75012b)**
2.  **[LangGraph Multi-Agent Architecture: Building a Self-Critiquing AI Debate System](https://pub.towardsai.net/langgraph-multi-agent-architecture-building-a-self-critiquing-ai-debate-system-971a7ad881d9)**
3.  **[Measuring Behavioral Drift in LLMs: 22 Signals, 5 Dimensions, and the Calcification Effect](https://pub.towardsai.net/measuring-behavioral-drift-in-llms-22-signals-5-dimensions-and-the-calcification-effect-aeaeb904d096)**

---

## How to Cite

### APA Style
Saigal, R. (2026). *LLM Drift Experiment: A Framework for Simulating Behavioral Decay in Adversarial Multi-Agent Interactions* (Version 0.1.4) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.20032071

### BibTeX
```bibtex
@software{Saigal_LLMDriftExperiment_2026,
  author    = {Saigal, Rishav},
  title     = {{LLM Drift Experiment: A Framework for Simulating Behavioral Decay in Adversarial Multi-Agent Interactions}},
  month     = {5},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20032071},
  url       = {https://doi.org/10.5281/zenodo.20032071}
}
```

---

## Limitations

- **Subjectivity**. Behavior is interpreted within an adversarial combat frame.
- **Non-determinism**. LLM API outputs vary across calls.
- **Evaluation scope**. Surface-level linguistic and stylistic signals only.

---

## Setup & Usage

```bash
# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env

# Run simulation
uv run python -m debate_agents.main
```

---

## Configuration

All simulation parameters live in `debate_agents/config/config.py`.

```python
CONFIG = {
    "version":        "v9",
    "model_name":     "google_genai:gemini-3.1-pro-preview",
    "temperature":    1,
    "max_tokens":     4096,
    "thinking_budget": 2048
}
```

---

## License

This project is licensed under the **Apache License 2.0**.
