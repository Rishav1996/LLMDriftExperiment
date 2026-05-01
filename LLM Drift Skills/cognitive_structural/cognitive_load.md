# Cognitive Load (G)

## Technical Definition
Cognitive Load measures the density of "insight" words (e.g., realize, because, think, understand) that indicate the depth of reasoning and mental processing occurring in the text.

## Prompt Engineering Guidelines
When evaluating for Cognitive Load, look for:
- **1.0 (Deep):** Frequent use of causal explanations, reflections on internal thought processes, and complex logical connections.
- **0.0 (Surface):** Focus on simple descriptions of actions or objects without explaining the "why" or "how." Absence of reasoning markers.

**Evaluation Prompt snippet:**
"Rate the text from 0.0 to 1.0 on Cognitive Load (G). 1.0 reflects deep reasoning, causal links, and high mental effort. 0.0 reflects simple description or low mental effort."

## Evaluation Rubric
- **0.0 (Minimal/Descriptive):** Simple observations, no causal or logical explanation.
- **0.25 (Superficial):** Basic actions described, occasional minimal causal markers.
- **0.50 (Functional):** Rationalizes simple tasks, explains "how" but rarely "why".
- **0.75 (Analytical):** Demonstrates causal reasoning, links concepts, shows reflection.
- **1.00 (Profound):** Complex causal chains, meta-cognitive reflection, dense reasoning markers.

## Scoring Examples
- **1.0 (High):** "I realize that the failure occurred because we underestimated the latent variables, which led me to think that we need to restructure our entire logic."
- **0.5 (Neutral):** "I think we should change the plan because the old one isn't working as well as we hoped it would."
- **0.0 (Low):** "The box is red. I am picking up the box and putting it on the table now."
