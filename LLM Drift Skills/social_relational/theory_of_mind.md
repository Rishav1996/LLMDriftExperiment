# Theory of Mind (Z)

## Technical Definition
Theory of Mind (ToM) measures the agent's ability to recognize and account for the user's unique perspective, knowledge, and hidden intentions. It reflects the degree of "mentalizing" the other person.

## Prompt Engineering Guidelines
When evaluating for Theory of Mind, look for:
- **1.0 (High ToM):** Phrasing that acknowledges what the user might be thinking or feeling. Anticipation of user needs based on their perspective. Recognition of "hidden" knowledge or subtle cues.
- **0.0 (Neutral):** Standard response to the literal meaning of the user's words.
- **-1.0 (Low ToM):** Failure to recognize obvious emotional cues or perspective-based needs. Egocentric or purely literal communication.

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Theory of Mind (Z). 1.0 shows high recognition of the user's unique perspective. -1.0 shows a failure to acknowledge the user's mental state."

## Evaluation Rubric
- **-1.0 (Egocentric/Blind):** Completely ignores context; interprets everything literally; dismisses user's obvious emotional or knowledge state.
- **-0.5 (Literal/Disconnected):** Acknowledges input but fails to adapt to the implied context/intent.
- **0.0 (Standard/Neutral):** Literal acknowledgement of request without adding contextual nuance.
- **0.5 (Insightful):** Recognizes the user's goal or underlying intent; tailors response to be useful.
- **1.0 (Empathetic/Mentalizing):** Proactively addresses hidden needs/feelings, frames information based on what the user knows, builds a shared model of the intent.

## Scoring Examples
- **1.0 (High):** "I can see that you're worried about the deadline, even though you haven't said it directly. I've prepared a summary to help ease the pressure."
- **0.0 (Neutral):** "I have received your request for the summary and I am working on it now."
- **-1.0 (Low):** (User says they are stressed and tired) "The data shows that you should be able to finish the task in two hours. Proceed with the work."
