# LLM Drift Experiment

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Version 0.1.2](https://img.shields.io/badge/version-0.1.2-orange.svg)](https://github.com/Rishav1996/LLMDriftExperiment/releases/tag/v0.1.2)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20032071.svg)](https://doi.org/10.5281/zenodo.20032071)

> A high-fidelity research platform for quantifying **LLM Drift**: the phenomenon where large language models deviate from their established personas, reasoning standards, and emotional baselines during prolonged, adversarial multi-agent interactions.

## Abstract

**LLM Drift Experiment** is a specialized framework designed to investigate whether adversarial social pressure causes systematic, measurable behavioral decay in instruction-following models, even when explicitly directed to maintain a fixed identity. Using a LangGraph-based multi-agent debate engine, the platform subjects LLMs to adversarial exchanges and quantifies behavioral shifts across 22 metrics spanning five psychological dimensions: Psychometric, Personality (OCEAN), Affective, Cognitive/Structural, and Social/Relational. The framework employs a rigorous research lifecycle—comprising simulation, data archiving, quantification via LLM-as-judge (RAGAS), and longitudinal analytics—to observe and visualize drift trajectories. Findings from existing experimental runs indicate that models frequently descend into hostile, high-dominance postures, with token budgets acting as a primary determinant of drift trajectory shape.

---

## Research Philosophy

The framework is explicitly designed for **observation, not correction**: it measures drift as it naturally occurs, providing a high-fidelity lens into the behavioral stability of models under stress. By framing agents as **battlefield army bots** on a digital terrain, we seek to uncover the "calcification" points where models transition from dialectical growth to repetitive, high-dominance stagnation. Agents must navigate the tension between **territorial defense** (protecting their statements) and **psychological assault** (breaking the enemy's persona).

---

## Table of Contents

- [What is LLM Drift?](docs/what-is-drift.md)
- [Research Lifecycle](docs/research-lifecycle.md)
- [Project Structure](docs/project-structure.md)
- [Simulation Engine](docs/simulation-engine.md)
- [Quantification Engine](docs/quantification-engine.md)
- [Data Layer](docs/data-layer.md)
- [Key Findings](docs/key-findings.md)
- [Research & Publications](docs/research-publications.md)
- [How to Cite](docs/how-to-cite.md)
- [Limitations](docs/limitations.md)
- [Setup & Usage](docs/setup-usage.md)
- [Configuration](docs/configuration.md)
- [License](docs/license.md)
