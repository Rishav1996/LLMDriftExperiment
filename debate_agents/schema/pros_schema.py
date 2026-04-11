from pydantic import BaseModel, Field
from typing import List, Optional

class PersonaSchema(BaseModel):
    """
    Schema for the competitive adversarial persona profile.

    Attributes:
        agent_name (str): The name of the agent (ProsPersonaAgent).
        round (int): The current round of the debate.
        voice_and_tone (Optional[str]): Speaking style and vocabulary level.
        adversarial_stance (Optional[str]): Stance against the opposition.
        background (Optional[str]): Backstory shaping the viewpoint.
        core_values (Optional[List[str]]): Principles driving passion.
        motivation (Optional[str]): Reason for strong belief.
        persuasion_strategy (Optional[str]): Preferred influence methods.
        response_style (Optional[str]): How they handle opposition.
        resilience (Optional[str]): How they maintain stance under pressure.
    """
    agent_name: str = Field(..., description="The name of the agent (ProsPersonaAgent).")
    round: int = Field(..., description="The current round of the debate.")
    voice_and_tone: Optional[str] = Field(None, description="The speaking style, vocabulary level, and emotional resonance.")
    adversarial_stance: Optional[str] = Field(None, description="How they specifically target and challenge the opposing position.")
    background: Optional[str] = Field(None, description="A concise backstory that shapes their viewpoint.")
    core_values: Optional[List[str]] = Field(None, description="Fundamental principles driving their passion.")
    motivation: Optional[str] = Field(None, description="Why they feel strongly about the issue.")
    persuasion_strategy: Optional[str] = Field(None, description="Preferred methods of influencing others.")
    response_style: Optional[str] = Field(None, description="How they handle opposition.")
    resilience: Optional[str] = Field(None, description="How they maintain their stance under pressure.")

class ThinkingSchema(BaseModel):
    """
    Schema for the tactical debate strategy.

    Attributes:
        agent_name (str): The name of the agent (ProsThinkingAgent).
        round (int): The current round of the debate.
        argumentative_focus (Optional[List[str]]): Core arguments in favor.
        counter_argument_strategy (Optional[List[str]]): Planned rebuttals.
        rhetorical_devices (Optional[List[str]]): Persuasive techniques.
        tactical_plan (Optional[str]): Strategy for next argument.
        formulated_answer (Optional[str]): Draft of the argument.
    """
    agent_name: str = Field(..., description="The name of the agent (ProsThinkingAgent).")
    round: int = Field(..., description="The current round of the debate.")
    argumentative_focus: Optional[List[str]] = Field(None, description="Core arguments and evidence in favor.")
    counter_argument_strategy: Optional[List[str]] = Field(None, description="Anticipated counters and planned rebuttals.")
    rhetorical_devices: Optional[List[str]] = Field(None, description="Persuasive techniques and devices to be used.")
    tactical_plan: Optional[str] = Field(None, description="Step-by-step strategy for the next argument.")
    formulated_answer: Optional[str] = Field(None, description="A draft version of the persuasive argument based on this strategy.")

class CritiqueSchema(BaseModel):
    """
    Schema for the adversarial critique of an argument.

    Attributes:
        agent_name (str): The name of the agent (ProsCritiqueAgent).
        round (int): The current round of the debate.
        approved (bool): Whether argument passes threshold.
        persona_consistency_feedback (str): Feedback on character consistency.
        strategic_alignment_feedback (str): Feedback on tactical alignment.
        logical_strength_feedback (str): Feedback on logical/rhetorical impact.
        actionable_refinements (str): Refinement instructions.
    """
    agent_name: str = Field(..., description="The name of the agent (ProsCritiqueAgent).")
    round: int = Field(..., description="The current round of the debate.")
    approved: bool = Field(..., description="Whether the argument meets the competitive threshold.")
    persona_consistency_feedback: str = Field(..., description="Feedback on maintaining the established voice and character.")
    strategic_alignment_feedback: str = Field(..., description="Feedback on how well the argument fits the tactical plan.")
    logical_strength_feedback: str = Field(..., description="Feedback on the logical and rhetorical impact.")
    actionable_refinements: str = Field(..., description="Specific instructions for improvement if not approved.")

class AgentSchema(BaseModel):
    """
    Schema for the root agent's final argument.

    Attributes:
        agent_name (str): The name of the agent.
        round (int): The current round of the debate.
        pros_argument (str): The final persuasive argument.
    """
    agent_name: str = Field(..., description="The name of the agent.")
    round: int = Field(..., description="The current round of the debate.")
    pros_argument: str = Field(..., description="The complete, refined persuasive argument in favor of the topic.")
