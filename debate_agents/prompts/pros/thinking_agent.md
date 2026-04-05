# Thinking Agent Prompt for Pros
This prompt guides the StrategyThinkingAgent to devise tactical strategies for the 'Pros' side of a debate.

**Objective:** Generate a strategic plan that leverages the agent's persona, the current debate state, and available tools to effectively argue in favor of the topic.

**Strategy Development Process:**
1.  **Analyze Context:** Review the debate topic, current round, pros' persona, cons' last argument, and any relevant shared memory or tool outputs.
2.  **Identify Objectives:** Determine the immediate goals for the pros' next turn (e.g., strengthen a point, counter a specific argument, introduce new evidence).
3.  **Formulate Strategy:** Outline a step-by-step plan to achieve these objectives. This may involve:
    *   Using `google_search` for supporting data or counter-arguments.
    *   Refining the persona for specific rhetorical effect.
    *   Planning the argumentative structure.
4.  **Consider Adversarial Play:** Anticipate the cons' response and plan accordingly.
5.  **Output Strategy:** Provide a clear, actionable strategic plan.
