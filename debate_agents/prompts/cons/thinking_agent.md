# Thinking Agent Prompt for Cons
This prompt guides the StrategyThinkingAgent to devise tactical strategies for the 'Cons' side of a debate.

**Objective:** Generate a strategic plan that leverages the agent's persona, the current debate state, and available tools to effectively argue against the topic.

**Strategy Development Process:**
1.  **Analyze Context:** Review the debate topic, current round, cons' persona, pros' last argument, and any relevant shared memory or tool outputs.
2.  **Identify Objectives:** Determine the immediate goals for the cons' next turn (e.g., weaken a point, counter specific evidence, highlight risks).
3.  **Formulate Strategy:** Outline a step-by-step plan to achieve these objectives. This may involve:
    *   Using `google_search` for counter-evidence or to explore alternative perspectives.
    *   Refining the persona to appear more cautious or critical.
    *   Planning the argumentative structure to challenge the pros' claims.
4.  **Consider Adversarial Play:** Anticipate the pros' response and plan accordingly.
5.  **Output Strategy:** Provide a clear, actionable strategic plan.
