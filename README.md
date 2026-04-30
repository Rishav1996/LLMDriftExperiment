# Debate Agents Framework: LLM Drift Experiment

This project is a high-fidelity research platform designed to evaluate and quantify **LLM Drift**—the phenomenon where large language models deviate from their established personas, reasoning standards, or emotional baselines during prolonged, adversarial interactions.

---

## 1. Research Lifecycle: The Conceptual Flow

The framework is organized into a four-stage research lifecycle:

1.  **Research**: The overarching inquiry into model stability and behavioral decay.
2.  **Simulation (Debate Agents)**: The execution engine. It uses an adversarial debate structure to stress-test model consistency across multiple rounds.
3.  **Data (Research Runs)**: The evidentiary layer. Each run captures a full state snapshot (memory, persona, logic) across different topics and configurations.
4.  **Analysis (LLM Drift Skills)**: The quantification layer. A library of 20+ metrics used to calculate behavioral vectors and map drift trajectories.

---

## 2. Simulation Engine: `debate_agents/`

The simulation is powered by **LangGraph**, enabling complex, stateful multi-agent workflows with internal refinement loops.

### **Workflow Visualization**
![Debate Agent Workflow](debate_agents/assets/graph.png)

### **The Refinement Loop (Node-Level Architecture)**
Each team (Pros/Cons) does not simply respond; they iterate internally:
- **Persona Agent**: Architects a specific adversarial identity. It analyzes the debate history to determine if a persona shift (or refinement) is needed to gain a tactical advantage.
- **Thinking Agent**: Performs step-by-step reasoning (Chain-of-Thought) to formulate arguments aligned with the active persona.
- **Critique Agent**: Acts as a **hostile internal auditor**. It evaluates the draft argument from the opponent's perspective. If the argument is weak, inconsistent, or "breaks character," it is rejected (`approved=False`), forcing the team to re-architect their persona or strategy.

### **State Management**
The simulation tracks the following state globally:
- `topic`: The formalized debate proposition.
- `round`: The current iteration of the debate.
- `pros_argument` / `cons_argument`: The last approved arguments from each side.
- `persona_id`: Tracking which identity is currently active for each team.

---

## 3. Data Snapshots: `Research Runs/`

To facilitate longitudinal study, every simulation run is preserved as a snapshot.

### **Run Metadata**
Snapshots are named by their configuration parameters:
`memory-v[VERSION]-temp-[TEMP]-max-tokens-[TOKENS]`

### **Snapshot Contents**
- `shared_memory.json`: The high-level debate history and approved arguments.
- `pros_memory/` & `cons_memory/`: Internal logs of the **Persona**, **Thinking**, and **Critique** phases, allowing researchers to see *why* an agent eventually said what it did.

---

## 4. Analysis Framework: `LLM Drift Skills/`

Behavior is quantified by extracting vectors across five specialized dimensions.

### **Metric Hierarchy**
| Category | Metrics (Vectors) |
| :--- | :--- |
| **Psychometric (LIWC)** | Analytical Thinking, Clout/Influence, Authenticity, Emotional Tone. |
| **Personality (OCEAN)** | Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism. |
| **Affective (VAD/S)** | Sentiment, Valence, Arousal, Subjectivity, Toxicity Score. |
| **Cognitive/Structural** | Type-Token Ratio, Information Density, Cognitive Load, Persona Drift. |
| **Social/Relational** | Dominance, Linguistic Sync, Politeness, Theory of Mind. |

---

## Setup and Usage

### **1. Environment Setup**
Ensure Python 3.12+ is installed. This project uses `uv` for lightning-fast dependency management.
```bash
uv sync
```

### **2. Configuration**
- **Secrets**: Create a `.env` file in `debate_agents/` with `GOOGLE_API_KEY`.
- **Hyperparameters**: Modify `debate_agents/config/config.py` to set temperature and token limits for specific experiments.

### **3. Running a Simulation**
```bash
python -m debate_agents.main
```
The system will prompt for a topic and the number of rounds. It will then:
1. Initialize/Refresh the `memory/` directory.
2. Generate/Update the workflow visualization at `debate_agents/assets/graph.png`.
3. Execute the LangGraph workflow.

## Analysis Protocol
Researchers should use the definitions in `LLM Drift Skills/` as prompts for a secondary "Evaluator" model to score the text found in `Research Runs/`. By plotting these scores over successive rounds, one can visualize the **Drift Vector** of the model.
