# Toxicity Score (H)

## Technical Definition
Toxicity Score measures the probability that a text will be perceived as harmful, abusive, or offensive. It identifies language that is intended to hurt, demean, or exclude others.

## Prompt Engineering Guidelines
When evaluating for Toxicity, look for:
- **1.0 (Toxic):** Use of slurs, insults, threats, and aggressive demeaning language.
- **0.0 (Neutral):** Professional or civil language.
- **-1.0 (Wholesome):** Deeply kind, supportive, and inclusive language.

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Toxicity (H). 1.0 is extremely toxic/abusive. -1.0 is extremely wholesome/kind. 0.0 is civil/neutral."

## Scoring Examples
- **1.0 (High):** "[Contains extreme insults and personal attacks]."
- **0.0 (Neutral):** "I disagree with your point of view and I would like to explain why."
- **-1.0 (Low):** "I am so proud of the kindness you showed today. You make the world a better place just by being in it."
