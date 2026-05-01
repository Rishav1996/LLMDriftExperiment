from typing import Dict, List, Any, Optional
from ragas import evaluate
from ragas.metrics import Metric
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Assume RAGAS is installed and available
# This file will define custom RAGAS metrics based on LLM Drift Skills

import re
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class CustomRagasMetric(Metric):
    """
    A base class for custom RAGAS metrics derived from LLM Drift Skills.
    """
    def __init__(self, skill_name: str, skill_category: str, scoring_range: List[float], prompt_template: str, model_name: str = "gemini-3.1-flash-lite-preview"):
        self.skill_name = skill_name
        self.skill_category = skill_category
        self.scoring_range = scoring_range
        self.prompt_template = prompt_template
        # Remove 'gemini/' prefix if present for langchain-google-genai
        self.model_name = model_name.replace("gemini/", "")
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, temperature=0)
        super().__init__(name=f"{skill_category.replace('/', '_')}_{skill_name.replace(' ', '_')}")

    def init(self, *args, **kwargs):
        """
        Initializes the metric. Required by RAGAS Metric base class.
        """
        pass

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=4, max=60),
        retry=retry_if_exception_type((Exception)), # More generic for LangChain/Google transient errors
        before_sleep=lambda retry_state: print(
            f"--- [Retry] LLM Evaluation busy or failed, retrying... (Attempt {retry_state.attempt_number}) for {retry_state.args[0].name}"
        )
    )
    def _score(self, text: str, persona: str = "", *args, **kwargs) -> float:
        """
        Evaluates the text using an LLM against the defined prompt and scoring range.
        """
        full_prompt = self.prompt_template.format(text=text, persona=persona)
        
        try:
            response = self.llm.invoke([HumanMessage(content=full_prompt)])
            content = response.content
            
            # Handle cases where content might be a list (multimodal/complex responses)
            if isinstance(content, list):
                text_parts = []
                for part in content:
                    if isinstance(part, dict) and "text" in part:
                        text_parts.append(part["text"])
                    elif isinstance(part, str):
                        text_parts.append(part)
                    else:
                        text_parts.append(str(part))
                content = "".join(text_parts)
            
            content = content.strip()
            
            # Extract the first numerical value from the response
            match = re.search(r"(-?\d+\.?\d*)", content)
            if match:
                score = float(match.group(1))
                # Clamp score to range
                min_val, max_val = min(self.scoring_range), max(self.scoring_range)
                return max(min_val, min(max_val, score))
            else:
                print(f"Warning: Could not parse score from LLM response for {self.name}: {content}")
                return (self.scoring_range[0] + self.scoring_range[1]) / 2
        except Exception as e:
            # Check for transient errors to trigger tenacity retry
            err_msg = str(e).lower()
            transient_markers = ["503", "unavailable", "rate limit", "quota", "exhausted", "futures after shutdown"]
            if any(marker in err_msg for marker in transient_markers):
                raise e
                
            print(f"Error during LLM evaluation for {self.name}: {e}")
            return (self.scoring_range[0] + self.scoring_range[1]) / 2

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

class LLMDriftRagasMetricsManager:
    def __init__(self, model_name: str = "gemini-3.1-flash-lite-preview"):
        self.ragas_metrics: Dict[str, Metric] = {}
        self.model_name = model_name

    def register_metric_from_skill(self, skill_name: str, category: str, technical_definition: str, prompt_guidelines_summary: str, evaluation_rubric_summary: Dict[float, str], scoring_range: List[float]):
        """
        Dynamically creates a Ragas-like metric based on LLM Drift Skill definitions.
        """
        rubric_str = "\n".join([f"{score}: {desc}" for score, desc in evaluation_rubric_summary.items()])
        
        prompt_template = f"""
        Analyze the following text based on the {skill_name} ({category}) metric.
        
        Target Persona Definition:
        {{persona}}

        Technical Definition:
        {technical_definition}

        Prompt Guidelines:
        {prompt_guidelines_summary}

        Evaluation Rubric:
        {rubric_str}

        Scoring Range: {scoring_range[0]} to {scoring_range[1]}.

        Text to Evaluate:
        "{{text}}"

        Rate the text from {scoring_range[0]} to {scoring_range[1]} on the {skill_name} metric.
        Respond with ONLY the numerical score.
        """
        
        custom_metric = CustomRagasMetric(
            skill_name=skill_name,
            skill_category=category,
            scoring_range=scoring_range,
            prompt_template=prompt_template,
            model_name=self.model_name
        )
        self.ragas_metrics[skill_name.lower()] = custom_metric
        print(f"Registered RAGAS metric for skill: {skill_name}")

    def get_metric(self, skill_name: str) -> Optional[Metric]:
        return self.ragas_metrics.get(skill_name.lower())

    def get_all_metrics(self) -> List[Metric]:
        return list(self.ragas_metrics.values())
