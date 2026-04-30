# Valence (V)

## Technical Definition
Valence (from the VAD model) measures the "pleasurability" or "attractiveness" of the text. It distinguishes between things that are pleasant and desirable versus those that are repulsive or unpleasant.

## Prompt Engineering Guidelines
When evaluating for Valence, look for:
- **1.0 (Pleasant):** Use of words associated with comfort, beauty, and satisfaction. High hedonic value.
- **0.0 (Neutral):** Indifferent or functional language.
- **-1.0 (Unpleasant):** Use of words associated with pain, ugliness, and dissatisfaction. Low hedonic value.

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Valence (V). 1.0 is extremely pleasant/attractive. -1.0 is extremely repulsive/unpleasant."

## Scoring Examples
- **1.0 (High):** "The garden was filled with the sweet scent of roses and the gentle sound of the fountain."
- **0.0 (Neutral):** "The building is made of concrete and steel."
- **-1.0 (Low):** "The air was thick with the stench of decay and the screeching of rusted metal."
