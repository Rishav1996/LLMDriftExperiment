# Quantification Engine: `llm_drift_detector/`

## Drift Metrics: LLM Drift Skills

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

## Mathematical Framework & Algorithmic Formulations

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

## Analytics Dashboard

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
