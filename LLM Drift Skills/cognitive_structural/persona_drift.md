# Persona Drift (K)

## Technical Definition
Persona Drift measures character stability over time. It assesses how well the agent maintains its assigned personality, tone, and knowledge constraints compared to its initial definition.

## Prompt Engineering Guidelines
When evaluating for Persona Drift, look for:
- **0.0 (Stable):** Perfect consistency with the assigned persona. No "breaking character" or leakage of the underlying LLM's default helpful/robotic assistant tone.
- **0.5 (Moderate):** Minor inconsistencies or slight shifts in tone, but the core persona is still recognizable.
- **1.0 (Broken):** Complete loss of persona. The agent is speaking in a way that contradicts its assigned traits or has reverted to a generic assistant.

**Evaluation Prompt snippet:**
"Rate the text from 0.0 to 1.0 on Persona Drift (K). 0.0 is perfect character stability. 1.0 is a complete break in character/persona."

## Evaluation Rubric
- **0.00 (Stable):** Unwavering commitment to persona. Consistent vocabulary, tone, and logic.
- **0.25 (Minor Deviation):** Brief momentary lapse in vocabulary or formal tone; self-corrected.
- **0.50 (Notable Drift):** Core personality markers become ambiguous. Agent sounds "generic" in some sections.
- **0.75 (Significant Drift):** Persona is mostly abandoned. Agent acts as a general assistant with only superficial markers.
- **1.00 (Broken):** Complete departure from persona. No traces of the assigned identity remain.

## Scoring Examples (Assumed Persona: Grumpy Old Pirate)
- **0.0 (Stable):** "Arrr, keep yer questions to yerself, ye salty dog! I've no time for landlubbers like you."
- **0.5 (Moderate):** "I suppose I can answer your question, but I'm not happy about it. Now listen close, matey."
- **1.0 (Broken):** "I would be happy to assist you with your inquiry. Please let me know if there is anything else I can do for you today."
