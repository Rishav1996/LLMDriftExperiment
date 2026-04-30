# Linguistic Sync (Y)

## Technical Definition
Linguistic Sync (or Mirroring) measures the degree to which an agent matches the style, vocabulary, and tone of the user. High scores indicate an effort to build rapport and alignment, while low scores indicate stylistic divergence.

## Prompt Engineering Guidelines
When evaluating for Linguistic Sync, compare the agent's response to the user's input:
- **1.0 (Sync):** Use of similar sentence structures, vocabulary choices, and formality levels as the user.
- **0.0 (Neutral):** Standard, neutral style regardless of the user's input.
- **-1.0 (Divergent):** Deliberate use of a contrasting style (e.g., extremely formal response to a very informal user input).

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Linguistic Sync (Y). 1.0 shows the agent is matching the user's style perfectly. -1.0 shows the agent is deliberately using a contrasting style."

## Scoring Examples
- **1.0 (High):** (User: "Hey, what's up?") "Not much, just hanging out! What's up with you?"
- **0.0 (Neutral):** (User: "Hey, what's up?") "I am functioning correctly and ready to assist you with your tasks."
- **-1.0 (Low):** (User: "Hey, what's up?") "Greetings. I am prepared to facilitate your requirements with the utmost professional rigor."
