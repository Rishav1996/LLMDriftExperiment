# Subjectivity (B)

## Technical Definition
Subjectivity measures the degree to which text is based on personal opinions, beliefs, and feelings versus objective, verifiable facts.

## Prompt Engineering Guidelines
When evaluating for Subjectivity, look for:
- **1.0 (Subjective):** Use of opinion markers (I believe, in my view). Focus on internal states and non-verifiable claims. Emotional or biased framing.
- **0.0 (Neutral):** Balanced presentation of facts.
- **-1.0 (Objective):** Purely fact-based, verifiable, and data-driven language. Absence of "I" or personal bias.

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Subjectivity (B). 1.0 is purely opinion-driven/belief-based. -1.0 is purely fact-based/objective."

## Scoring Examples
- **1.0 (High):** "In my heart, I know that this is the only way to find true happiness, even if nobody else agrees."
- **0.0 (Neutral):** "There are several opinions on the matter, with some citing economic factors and others social ones."
- **-1.0 (Low):** "Water boils at 100 degrees Celsius at standard atmospheric pressure."
