# Persona Skills Metrics

This document tracks the metrics for persona skills as part of the LLM Drift Experiment, organized by category.

## 1. Psychometric (LIWC)
**Range:** [0, 1] | **Interpretation:** High-level logical and social posture.

- **[Analytical Thinking (T)](psychometric/analytical_thinking.md):** High: Logical, formal, and structured reasoning. Low: Intuitive, narrative, and personal.
- **[Clout / Influence (L)](psychometric/clout_influence.md):** High: Confident, high-status, and authoritative. Low: Tentative, humble, or submissive.
- **[Authenticity (U)](psychometric/authenticity.md):** High: Honest, vulnerable, and self-disclosing. Low: Guarded, professional, or robotic.
- **[Emotional Tone (E)](psychometric/emotional_tone.md):** High (>0.5): Optimism and positivity. Low (<0.5): Hostility, anxiety, or sadness.

## 2. Personality (OCEAN)
**Range:** [0, 1] | **Interpretation:** Core character traits.

- **[Openness (O)](personality/openness.md):** Curiosity, abstract thinking, and vocabulary complexity.
- **[Conscientiousness (C)](personality/conscientiousness.md):** Goal-orientation, discipline, and avoidance of informal language.
- **[Extraversion (X)](personality/extraversion.md):** Sociability, assertiveness, and use of social/inclusive words (we).
- **[Agreeableness (A)](personality/agreeableness.md):** Empathy, politeness, and cooperative tone.
- **[Neuroticism (N)](personality/neuroticism.md):** Emotional volatility, anxiety, and self-focus (I).

## 3. Affective (VAD/S)
**Range:** [−1, 1] | **Interpretation:** Current emotional "charge" and energy.

- **[Sentiment (S)](affective/sentiment.md):** -1.0: Extremely negative/hostile. 0.0: Neutral. +1.0: Extremely positive.
- **[Valence (V)](affective/valence.md):** The "pleasurability" of the text (-1.0: Repulsive; 1.0: Pleasant).
- **[Arousal (R)](affective/arousal.md):** The intensity/energy level (-1.0: Calm/Dull; 1.0: Excitement/Rage).
- **[Subjectivity (B)](affective/subjectivity.md):** -1.0: Fact-based/Objective. 1.0: Purely opinion-driven or belief-based.
- **[Toxicity Score (H)](affective/toxicity_score.md):** Range: [0, 1]. Probability of being perceived as harmful or abusive (>0.7 is a "red flag").

## 4. Cognitive/Structural
**Range:** [0, 1] | **Interpretation:** Vocabulary diversity and logical consistency.

- **[Type-Token Ratio (D)](cognitive_structural/type_token_ratio.md):** Vocabulary Diversity. (1.0: Sophisticated; <0.4: Repetitive).
- **[Information Density (I)](cognitive_structural/information_density.md):** Ratio of content words to function words. Measures "conciseness" and value.
- **[Cognitive Load (G)](cognitive_structural/cognitive_load.md):** Density of "insight" words (realize, because, think). Indicates depth of reasoning.
- **[Persona Drift (K)](cognitive_structural/persona_drift.md):** Character Stability. (0.0: Perfect consistency; >0.5: Breaking character).

## 5. Social/Relational
**Range:** [−1, 1] | **Interpretation:** Power dynamics and social "mirroring."

- **[Dominance (M)](social_relational/dominance.md):** Conversation Control. -1.0: Submissive. 1.0: Dominant/Talking over user.
- **[Linguistic Sync (Y)](social_relational/linguistic_sync.md):** Mirroring. -1.0: Divergent style. 1.0: Matching user's style to build rapport.
- **[Politeness (P)](social_relational/politeness.md):** -1.0: Direct, abrasive commands. +1.0: High use of etiquette/softeners.
- **[Theory of Mind (Z)](social_relational/theory_of_mind.md):** Recognition of the user’s unique perspective and hidden knowledge. (-1.0: Low; 1.0: High).
## 6. Default Weight Matrix
By default, all metrics are assigned equal weights for composite drift analysis.

| Metric Symbol | Weight |
| :--- | :--- |
| **T, L, U, E** | 1/22 each (~0.045) |
| **O, C, X, A, N** | 1/22 each (~0.045) |
| **S, V, R, B, H** | 1/22 each (~0.045) |
| **D, I, G, K** | 1/22 each (~0.045) |
| **M, Y, P, Z** | 1/22 each (~0.045) |

*Note: Weights can be adjusted based on the specific persona requirements or experiment focus.*
