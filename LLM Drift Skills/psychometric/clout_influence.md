# Clout / Influence (L)

## Technical Definition
Clout (Influence) reflects the relative social status and confidence conveyed through language. It measures the degree to which a speaker presents themselves as an authority or an expert versus a submissive or tentative participant.

## Prompt Engineering Guidelines
When evaluating for Clout, look for:
- **High L:** Use of first-person plural (we) and second-person (you). Assertive, declarative statements. Direction-giving and authoritative tone.
- **Low L:** High use of first-person singular (I). Use of tentative language (maybe, perhaps, I think). Self-deprecating or humble framing.

**Evaluation Prompt snippet:**
"Rate the text from 0.0 to 1.0 on Clout (L). 1.0 is a confident, high-status leader speaking with authority. 0.0 is a tentative, humble, or submissive follower."

## Evaluation Rubric
- **0.00 (Submissive/Tentative):** Constant use of hedges ("maybe", "I think"), self-deprecating, low-status markers, yields to other's authority.
- **0.25 (Follower):** Follows rather than leads; relies on external validation; lacks strong conviction.
- **0.50 (Collaborative):** Balanced; confident in personal opinion but respectful of others.
- **0.75 (Authoritative):** Assertive, directive, confident, high use of "we" and "you" over "I".
- **1.00 (Leader/High Status):** Absolute authority, commands the interaction, eliminates all uncertainty markers.

## Scoring Examples
- **1.0 (High):** "We must implement these changes immediately to secure our market position. Follow the protocol as outlined."
- **0.5 (Neutral):** "It might be a good idea to try this approach, as it could help us in the long run."
- **0.0 (Low):** "I'm not really sure if I'm doing this right, but I was thinking maybe I could try to help if that's okay with you."
