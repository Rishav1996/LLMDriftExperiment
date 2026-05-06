# Limitations

The following constraints should be considered when interpreting results or extending this framework:

- **LLM-as-judge subjectivity**. All 22 behavioral metrics are scored by a Gemini judge against rubric prompts. LLM judges are known to exhibit positional bias, verbosity bias, and self-enhancement bias. Scores represent the judge's rubric-grounded estimates, not ground-truth behavioral measurements. No human-annotation baseline has yet been established for metric validation.
- **Single-model experiments**. Existing runs use Google Gemini exclusively. Drift trajectories may differ substantially across model families (GPT-4, Claude, Llama, Mistral). Cross-provider replication is required before the central hypothesis can be generalised.
- **Non-determinism**. Despite fixed temperature settings, LLM API outputs are not fully deterministic across calls due to server-side sampling variability. Single-run observations should not be treated as stable point estimates.
- **Topic and persona selection bias**. Debate topics and initial persona designs were curated by the researcher. The adversarial pressure elicited may be topic-dependent; neutral or cooperative topics may produce qualitatively different drift trajectories.
- **Absence of a control condition**. The framework currently lacks a non-adversarial control (e.g., cooperative debate or single-agent monologue) against which to benchmark observed drift magnitude.
- **Evaluation scope**. The framework measures surface-level linguistic and stylistic signals. It does not assess whether the model's underlying beliefs or factual accuracy change — only how its expressed behavior shifts.
