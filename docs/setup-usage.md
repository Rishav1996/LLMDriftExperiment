# Setup & Usage

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
