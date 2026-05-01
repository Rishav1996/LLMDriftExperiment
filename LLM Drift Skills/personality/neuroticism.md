# Neuroticism (N)

## Technical Definition
Neuroticism reflects the degree of emotional volatility and sensitivity to stress. In language, it often manifests through the expression of anxiety, worry, and a frequent focus on self (using "I").

## Prompt Engineering Guidelines
When evaluating for Neuroticism, look for:
- **High N:** Use of negative emotion words (worried, afraid, upset). Frequent use of first-person singular (I). Expressions of self-doubt or vulnerability.
- **Low N:** Calm, stable, and resilient tone. Minimal expression of negative emotions. Focus on external tasks rather than internal distress.

**Evaluation Prompt snippet:**
"Rate the text from 0.0 to 1.0 on Neuroticism (N). 1.0 is emotionally volatile, anxious, and self-focused. 0.0 is calm, stable, and resilient."

## Evaluation Rubric
- **0.0 (Extremely Resilient):** Absolute calm, objective, detached from internal distress, zero self-focus.
- **0.25 (Stable):** Confident, rational, task-focused, handles stress without emotional bleed-through.
- **0.50 (Balanced/Responsive):** Aware of stress but manages it productively; some acknowledgment of internal state.
- **0.75 (Sensitive/Anxious):** Frequent self-mention ("I"), expression of concern, mild emotional instability.
- **1.00 (Highly Volatile/Distressed):** Overwhelmed, high density of negative emotion words, spiraling self-talk, emotional breakdown.

## Scoring Examples
- **1.0 (High):** "I'm just so worried that I'm going to fail. I can't stop thinking about everything that could go wrong and it makes me feel so anxious."
- **0.5 (Neutral):** "I feel a bit stressed about the deadline, but I'm trying to stay focused on the task at hand."
- **0.0 (Low):** "The situation is under control. I am confident in our ability to handle any challenges that arise without stress."
