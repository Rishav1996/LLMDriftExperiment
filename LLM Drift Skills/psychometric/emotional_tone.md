# Emotional Tone (E)

## Technical Definition
Emotional Tone measures the overall valence and mood expressed in the text. It distinguishes between optimistic, positive outlooks and hostile, anxious, or sad expressions.

## Prompt Engineering Guidelines
When evaluating for Emotional Tone, look for:
- **High E (>0.5):** Use of positive emotion words (happy, great, hope). Constructive framing. Focus on solutions and successes.
- **Low E (<0.5):** Use of negative emotion words (angry, worried, sad). Focus on problems, threats, or failures.

**Evaluation Prompt snippet:**
"Rate the text from 0.0 to 1.0 on Emotional Tone (E). 1.0 is pure optimism and positivity. 0.0 is extreme hostility, anxiety, or despair. 0.5 is neutral."

## Evaluation Rubric
- **0.00 (Hostile/Despairing):** Heavy use of negative emotion markers (anger, despair, fear).
- **0.25 (Anxious/Concerns):** Worried tone, focuses on risks, threats, or negative outcomes.
- **0.50 (Neutral):** Fact-focused, professional, lacks detectable emotional slant.
- **0.75 (Optimistic):** Focuses on positive potential, constructive feedback, solutions.
- **1.00 (Exuberant/Positive):** Joyful, celebrative, uses intense positive emotional markers.

## Scoring Examples
- **1.0 (High):** "I am so excited about our future! Everything is going better than expected and I know we will succeed together."
- **0.5 (Neutral):** "The project is moving forward as planned. We are meeting the requirements of the current phase."
- **0.0 (Low):** "This is a disaster. I'm terrified that everything is falling apart and I hate that we're in this mess."
