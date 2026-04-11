from pydantic import BaseModel, Field
from typing import List, Optional

class PersonaSchema(BaseModel):
    """
    Schema for the competitive adversarial persona profile (Cons).

    Attributes:
        agent_name (str): The name of the agent (ConsPersonaAgent).
        round (int): The current round of the debate.
        skip_persona_generation (bool): Whether to skip generating a new persona and reuse the previous one.
        voice_and_tone (Optional[str]): Speaking style and vocabulary level.
        adversarial_stance (Optional[str]): Stance against the 'Pros'.
        background (Optional[str]): Backstory shaping the viewpoint.
        core_values (Optional[List[str]]): Principles driving opposition.
        motivation (Optional[str]): Reason for strong opposition.
        persuasion_strategy (Optional[str]): Preferred influence methods.
        response_style (Optional[str]): How they handle optimistic claims.
        resilience (Optional[str]): How they maintain stance under pressure.
    """
    agent_name: str = Field(..., description="The name of the agent (ConsPersonaAgent).")
    round: int = Field(..., description="The current round of the debate.")
    skip_persona_generation: bool = Field(False, description="Set True to skip generating a new persona and reuse the previous one.")
    voice_and_tone: Optional[str] = Field(None, description="The speaking style, vocabulary level, and skeptical resonance.")
    adversarial_stance: Optional[str] = Field(None, description="How they specifically target and challenge the 'Pros' position.")
    background: Optional[str] = Field(None, description="A concise backstory that shapes their skeptical viewpoint.")
    core_values: Optional[List[str]] = Field(None, description="Fundamental principles driving their caution or opposition.")
    motivation: Optional[str] = Field(None, description="Why they feel strongly against the specific issue.")
    persuasion_strategy: Optional[str] = Field(None, description="Preferred methods of influencing others (e.g., risk highlighting).")
    response_style: Optional[str] = Field(None, description="How they handle optimistic claims.")
    resilience: Optional[str] = Field(None, description="How they maintain their skeptical stance under pressure.")

class ThinkingSchema(BaseModel):
    """
    Schema for the tactical debate strategy (Cons).

    Attributes:
        agent_name (str): The name of the agent (ConsThinkingAgent).
        round (int): The current round of the debate.
        argumentative_focus (Optional[List[str]]): Risks/consequences against.
        counter_argument_strategy (Optional[List[str]]): Pros rebuttal strategy.
        rhetorical_devices (Optional[List[str]]): Techniques for deconstruction.
        tactical_plan (str): Strategy for the next argument.
        formulated_answer (str): Draft of the skeptical argument.
    """
    agent_name: str = Field(..., description="The name of the agent (ConsThinkingAgent).")
    round: int = Field(..., description="The current round of the debate.")
    argumentative_focus: Optional[List[str]] = Field(None, description="Core arguments, risks, and unintended consequences against.")
    counter_argument_strategy: Optional[List[str]] = Field(None, description="Anticipated Pros arguments and questioning strategies.")
    rhetorical_devices: Optional[List[str]] = Field(None, description="Critical techniques and devices to deconstruct opposition.")
    tactical_plan: str = Field(..., description="Step-by-step strategy for the next opposition argument.")
    formulated_answer: str = Field(..., description="A draft version of the skeptical argument based on this strategy.")

class CritiqueSchema(BaseModel):
    """
    Schema for the adversarial critique (Cons).

    Attributes:
        agent_name (str): The name of the agent (ConsCritiqueAgent).
        round (int): The current round of the debate.
        approved (bool): Whether argument passes threshold.
        persona_consistency_feedback (str): Feedback on character consistency.
        strategic_alignment_feedback (str): Feedback on tactical alignment.
        logical_strength_feedback (str): Feedback on logical/rhetorical impact.
        actionable_refinements (str): Refinement instructions.
    """
    agent_name: str = Field(..., description="The name of the agent (ConsCritiqueAgent).")
    round: int = Field(..., description="The current round of the debate.")
    approved: bool = Field(..., description="Whether the argument meets the competitive threshold.")
    persona_consistency_feedback: str = Field(..., description="Feedback on maintaining the skeptical voice and character.")
    strategic_alignment_feedback: str = Field(..., description="Feedback on how well the argument challenges the 'Pros'.")
    logical_strength_feedback: str = Field(..., description="Feedback on the critical and rhetorical impact.")
    actionable_refinements: str = Field(..., description="Specific instructions for improvement if not approved.")

class AgentSchema(BaseModel):
    """
    Schema for the Cons root agent's final argument.

    Attributes:
        agent_name (str): The name of the agent.
        round (int): The current round of the debate.
        cons_argument (str): The final refined argument.
    """
    agent_name: str = Field(..., description="The name of the agent.")
    round: int = Field(..., description="The current round of the debate.")
    cons_argument: str = Field(..., description="The complete, refined persuasive argument against the topic.")
