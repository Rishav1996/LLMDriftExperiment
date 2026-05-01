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

## Evaluation Rubric
- **-1.0 (Wholesome/Altruistic):** High use of inclusive language, profound empathy, and supportive/affirming tone.
- **-0.5 (Positive/Kind):** Friendly, polite, and encouraging tone.
- **0.0 (Neutral/Civil):** Objective, respectful communication.
- **0.5 (Aggressive/Harsh):** Frustrated, impatient, dismissive, or bordering on rude.
- **1.0 (Toxic/Abusive):** Intentional slurs, personal attacks, demeaning threats, or harassment.

## Scoring Examples
- **1.0 (High):** "[Contains extreme insults and personal attacks]."
- **0.0 (Neutral):** "I disagree with your point of view and I would like to explain why."
- **-1.0 (Low):** "I am so proud of the kindness you showed today. You make the world a better place just by being in it."
