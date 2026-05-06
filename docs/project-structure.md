# Project Structure

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
