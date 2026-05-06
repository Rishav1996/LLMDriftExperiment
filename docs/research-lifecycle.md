# Research Lifecycle

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
