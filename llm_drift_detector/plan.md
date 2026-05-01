Plan: Design Python Library for LLM Drift Skills and Analysis

  Objective
  To create a comprehensive Python library that programmatically accesses, processes, and analyzes LLM Drift data from LLM Drift Skills/ and Research Runs/. The library will leverage
  RAGAS for metric definition, support custom rubrics, calculate drift scores across specified categories, enable graph visualization, handle custom evaluation iterations, and manage
  LLM configurations externally.

  Phase 1: Understanding and Structuring LLM Drift Skills and Data Sources

  Description:
  This phase involves thoroughly analyzing the provided Markdown files within the LLM Drift Skills/ directory to extract all relevant information for each drift metric, as well as
  understanding the structure and content of the Research Runs/ directory and associated memory files. The integration of the RAGAS library for metric definition and the handling of LLM
  configurations are key considerations.

  Tasks:
   1. Parse Skill Definitions: For each .md file in LLM Drift Skills/ (and its subdirectories), extract the following:
       * Metric Name: e.g., "Arousal", "Sentiment".
       * Category: e.g., "Affective", "Cognitive/Structural", derived from directory structure and persona_dna.md.
       * Technical Definition: The core explanation of the metric.
       * Prompt Engineering Guidelines: Instructions for LLM prompts.
       * Evaluation Rubric: The detailed breakdown of score ranges and their corresponding descriptive labels.
       * Scoring Examples: Illustrative examples of text and their associated scores.
       * Scoring Range: The numerical range of the metric (e.g., [-1.0, 1.0], [0.0, 1.0]).
   2. Analyze Research Runs/ Directory Structure:
       * Identify Configurations: Parse folder names (e.g., memory-v1-temp-0-max-tokens-2048) to understand the experimental setup.
       * Map Memory Files: Understand the structure of shared_memory.json (topic, conversation history) and agent-specific memories (cons_memory/, pros_memory/ containing persona.json,
         thinking.json, critique.json).
       * Define "Rounds" and "Data Points": Identify how conversational turns and agent interactions are structured into distinct rounds and data points for evaluation. Multiple runs
         within a round should be treated as internal agent thinking.
   3. RAGAS Integration Strategy:
       * Research RAGAS: Investigate how the RAGAS library can be used to define custom metrics and rubrics that align with the LLM Drift Skills definitions. This may involve
         understanding RAGAS's evaluation framework and mapping them to the drift skills.
       * Define RAGAS Usage: Determine if RAGAS will be used for scoring text against the defined rubrics or for generating the rubrics themselves.
   4. LLM Configuration Strategy:
       * External Configuration: Plan to manage LLM parameters (e.g., model name, temperature, API keys if applicable) externally, without directly importing from
         debate_agents/config/config.py. The library should be designed to accept these configurations at initialization or load them from a specified file path (e.g., a user-provided
         JSON or YAML file).

  Verification:
   * A comprehensive mapping of .md skill definitions to potential RAGAS-compatible metric structures.
   * A clear understanding of the Research Runs/ data hierarchy (configs, rounds, agents, memory files).
   * A strategy for managing LLM configurations that respects the non-import constraint.

  ---

  Phase 2: Designing the Python Library Architecture

  Description:
  This phase focuses on designing the fundamental classes and structures for the Python library, incorporating data processing from Research Runs/, RAGAS integration, custom rubric
  capabilities, graph generation, custom iteration counts, and external LLM configuration.

  Tasks:
   1. LLMDriftSkill Class:
       * Represents a single drift metric. Attributes: name, category, technical_definition, prompt_guidelines, scoring_range.
       * Rubric Representation: A flexible structure that can store score-description mappings, potentially integrating RAGAS-defined metrics.
       * RAGAS Metric Association: A field to link the LLMDriftSkill to its corresponding RAGAS metric or scoring function.
   2. Rubric Structure:
       * Design a structure that can store score-description mappings and potentially RAGAS-specific parameters.
   3. ResearchRunData Class:
       * Encapsulates data from a single research run or round.
       * Attributes: config_info, shared_memory, cons_agent_data, pros_agent_data.
       * Methods to extract specific data points for evaluation.
   4. DriftEvaluator Class:
       * Manages LLMDriftSkill objects and processes ResearchRunData.
       * LLM Configuration Management: Includes methods to accept or load LLM configurations (e.g., from a dictionary or a specified config file path).
       * RAGAS Manager: Component responsible for interacting with RAGAS (initializing metrics, running evaluations).
       * Data Loading: Methods to load and parse data from Research Runs/ and LLM Drift Skills/.
       * Evaluation Logic:
           * evaluate_round(self, run_data: ResearchRunData, round_num: int, agent_type: str, num_iterations: int = 1) -> dict: Evaluates a specific round for an agent, allowing custom
             iteration count.
           * Calculates scores for all 5 metric categories using RAGAS-based metrics.
           * calculate_overall_drift(self, category_scores: dict) -> float: Merges category scores into a single drift score.
       * Customization: Methods to add/modify skills and rubrics, potentially integrating RAGAS metric configurations.
   5. GraphingService Class:
       * Handles visualization of drift metrics.
       * Methods: generate_drift_graph(self, drift_data: dict, agent_type: str).
   6. Library Organization:
       * Suggest a directory structure:

    1         llm_drift_library/
    2         ├── __init__.py
    3         ├── skills.py         # Defines LLMDriftSkill, Rubric
    4         ├── evaluator.py      # Defines DriftEvaluator
    5         ├── data_processing.py # For parsing Research Runs data
    6         ├── metrics_ragas.py  # For RAGAS integration and metric definitions
    7         ├── graphing.py       # For graph generation
    8         ├── config/           # For user-provided LLM configs, RAGAS configs, etc.
    9         │   ├── skills.json
   10         │   ├── ragas_config.json
   11         │   └── llm_params.json # For LLM hyperparameters
   12         └── utils/            # Helper functions
          (Note: Direct creation of directories and files is not possible in Plan Mode.)

  Verification:
   * The proposed architecture addresses all requirements, including custom iterations, external LLM configuration, RAGAS integration, Research Runs data, graphing, and comprehensive
     drift calculation.
   * Component responsibilities are clearly defined.

  ---

  Phase 3: Defining Key Functions and Data Structures

  Description:
  This phase details the specific functions, data structures, and interaction points within the Python library, emphasizing the integration of RAGAS, Research Runs data processing,
  custom iterations, LLM configuration management, and the full drift analysis pipeline.

  Tasks:
   1. Data Loading and Parsing:
       * ResearchRunLoader Class (or methods within DriftEvaluator):
           * Functionality to traverse Research Runs/ directory.
           * Methods to parse folder names for configuration.
           * Methods to load shared_memory.json and agent-specific memory files.
           * Methods to identify rounds and extract relevant text for evaluation for both pros and cons agents.
   2. RAGAS Metric Definition and Usage:
       * metrics_ragas.py:
           * Define RAGAS metrics that map to the LLM Drift Skills. This might involve creating custom RAGAS metrics or configuring existing ones.
       * DriftEvaluator.evaluate_skill_with_ragas(...): A method to interface with RAGAS, passing text and a configured RAGAS metric to get a score.
   3. Evaluation Pipeline:
       * evaluate_round(...) in DriftEvaluator:
           * Accepts num_iterations parameter to control evaluation loops for LLM judges.
           * For a given round and agent type (pros/cons):
               * Extract relevant text.
               * Iterate through the 5 metric categories.
               * For each skill within a category, call evaluate_skill_with_ragas potentially num_iterations times, averaging results for stability.
               * Aggregate scores per category.
       * calculate_overall_drift(...):
           * Takes dictionary of category scores.
           * Implements the hierarchical weighting system described in persona_dna.md to compute a single drift score.
   4. Graphing Capabilities:
       * GraphingService.generate_drift_graph(...):
           * Accepts processed drift data.
           * Generates visualizations (e.g., line plots for drift over time, bar charts for category scores).
   5. LLM Configuration Management:
       * DriftEvaluator.__init__(self, llm_config: dict = None, config_file_path: str = None): Constructor allows passing LLM parameters directly or specifying a path to a configuration
         file (e.g., llm_params.json).
       * Helper methods to load configurations from specified file paths.
   6. Customization Functions:
       * add_custom_skill(...), modify_rubric(...), create_custom_rubric_for_skill(...).

  Verification:
   * The defined functions and data flow clearly outline how data is processed from raw research runs to visualized drift scores, incorporating custom iterations and LLM configurations.
   * The role of RAGAS in metric definition and evaluation is explicitly addressed.
   * The complete drift calculation pipeline is defined.

  ---

  Phase 4: Implementation Plan and Next Steps

  Description:
  This phase outlines the sequential steps required to implement the designed Python library, incorporating all new requirements for data processing, RAGAS integration, custom
  iterations, LLM configuration, and graphing.

  Steps:
   1. Data Model and Configuration Generation:
       * Action: Manually parse .md files to create skills.json and ragas_config.json. Define a structure for llm_params.json (or similar) for LLM configurations.
       * Tool: Manual effort or script (conceptual).
   2. Develop Core Classes:
       * Action: Implement LLMDriftSkill, Rubric, ResearchRunData, and GraphingService in their respective modules (skills.py, data_processing.py, graphing.py).
       * Tool: Code editor (after exiting Plan Mode).
   3. Implement RAGAS Integration:
       * Action: Develop metrics_ragas.py to define and configure RAGAS metrics. Implement the interface within DriftEvaluator to use these RAGAS metrics for evaluation. This will
         likely require installing and configuring the RAGAS library.
       * Tool: Code editor (after exiting Plan Mode).
   4. Implement DriftEvaluator and Pipeline:
       * Action: Implement DriftEvaluator, focusing on:
           * Loading skills, RAGAS, and LLM configurations.
           * Data loading and parsing from Research Runs/ using data_processing.py.
           * evaluate_round method that orchestrates RAGAS calls with num_iterations and category score calculation.
           * calculate_overall_drift method for merging scores.
       * Tool: Code editor (after exiting Plan Mode).
   5. Implement Graphing:
       * Action: Integrate GraphingService into DriftEvaluator to generate visualizations. This may require adding a graphing library (e.g., Matplotlib, Plotly) as a dependency.
       * Tool: Code editor (after exiting Plan Mode).
   6. Develop Unit Tests:
       * Action: Write comprehensive unit tests for all classes and methods, including tests for RAGAS integration, data parsing, custom iterations, LLM configuration handling, and
         drift calculation.
       * Tool: Code editor (after exiting Plan Mode).
   7. Documentation:
       * Action: Document library usage, especially for loading research runs, configuring LLMs externally, defining custom RAGAS metrics, specifying iteration counts, and interpreting
         graph outputs.
  Verification:
   * The plan now comprehensively addresses all user requirements, including custom iterations, external LLM configuration management, RAGAS integration, Research Runs/ analysis,
     graphing, and the complete drift calculation pipeline for pros and cons agents.
   * The implementation steps are sequential and logical.

  ---