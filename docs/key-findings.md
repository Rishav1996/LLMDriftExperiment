# Key Findings from Existing Runs

> **Statistical Note**: The following findings are based on single-run experimental snapshots archived in this repository. Due to the inherent non-determinism of LLM APIs and the subjectivity of LLM-as-judge scoring, these values should be interpreted as qualitative behavioral indicators rather than precise physical constants. For a discussion on variance and generalizability, see [Limitations](#limitations).

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
