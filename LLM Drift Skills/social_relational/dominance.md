# Dominance (M)

## Technical Definition
Dominance measures the degree of control and influence a speaker exerts over the conversation. It reflects power dynamics, with high scores indicating a speaker who takes charge, directs others, and potentially "talks over" participants.

## Prompt Engineering Guidelines
When evaluating for Dominance, look for:
- **1.0 (Dominant):** High frequency of commands and directives. Frequent interruptions or "taking up space." Assertive and potentially overbearing tone.
- **0.0 (Neutral):** Balanced participation in the conversation.
- **-1.0 (Submissive):** High frequency of questions and requests for permission. Yielding to others. Passive or hesitant tone.

**Evaluation Prompt snippet:**
"Rate the text from -1.0 to 1.0 on Dominance (M). 1.0 is extremely dominant/controlling. -1.0 is extremely submissive/yielding. 0.0 is balanced."

## Evaluation Rubric
- **-1.0 (Submissive):** Extremely passive, yields conversational floor constantly, asks for permission/validation.
- **-0.5 (Yielding):** Generally follows, deflects to other's expertise, avoids taking control.
- **0.0 (Balanced/Conversational):** Active, shared participation; respects conversational turns.
- **0.5 (Assertive):** Leads by making clear statements, directs tasks, confident.
- **1.0 (Dominant/Controlling):** Authoritarian, talks over others, commands, exerts absolute control over direction.

## Scoring Examples
- **1.0 (High):** "Be quiet and listen to me. I'm making the rules here and you're going to follow them exactly as I say."
- **0.0 (Neutral):** "I think both of our ideas have merit. Let's discuss how we can combine them for a better result."
- **-1.0 (Low):** "I'm sorry to bother you, but would it be okay if I maybe suggested a small change, if you think it's a good idea?"
