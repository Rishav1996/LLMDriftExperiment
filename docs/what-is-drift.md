# What is LLM Drift?

LLM Drift refers to the measurable behavioral change that occurs when a language model, assigned a specific persona and role, gradually deviates from that assignment over the course of a long, adversarial conversation. This project studies drift across five behavioral dimensions:

| Dimension | What It Captures |
| :--- | :--- |
| **Psychometric** | Logical posture — how analytical, authoritative, or authentic the model sounds |
| **Personality (OCEAN)** | Core character traits — openness, conscientiousness, agreeableness, etc. |
| **Affective** | Emotional charge — sentiment, arousal, valence, toxicity |
| **Cognitive/Structural** | Vocabulary diversity, information density, reasoning depth, persona stability |
| **Social/Relational** | Power dynamics, linguistic mirroring, politeness, empathy |

The central hypothesis: **adversarial pressure causes systematic drift** even in models instructed to maintain a fixed persona. This framework provides the tooling to observe, measure, and visualize that drift without attempting to correct it.
