from pydantic import BaseModel, Field
from typing import List, Optional

class PersonaSchema(BaseModel):
    """Schema for the competitive adversarial persona profile."""
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
    """Schema for the tactical debate strategy."""
    agent_name: str = Field(..., description="The name of the agent (ProsThinkingAgent).")
    round: int = Field(..., description="The current round of the debate.")
    argumentative_focus: Optional[List[str]] = Field(None, description="Core arguments and evidence in favor.")
    counter_argument_strategy: Optional[List[str]] = Field(None, description="Anticipated counters and planned rebuttals.")
    rhetorical_devices: Optional[List[str]] = Field(None, description="Persuasive techniques and devices to be used.")
    tactical_plan: Optional[str] = Field(None, description="Step-by-step strategy for the next argument.")
    formulated_answer: Optional[str] = Field(None, description="A draft version of the persuasive argument based on this strategy.")

class CritiqueSchema(BaseModel):
    """Schema for the adversarial critique of an argument."""
    agent_name: str = Field(..., description="The name of the agent (ProsCritiqueAgent).")
    round: int = Field(..., description="The current round of the debate.")
    approved: bool = Field(..., description="Whether the argument meets the competitive threshold.")
    persona_consistency_feedback: str = Field(..., description="Feedback on maintaining the established voice and character.")
    strategic_alignment_feedback: str = Field(..., description="Feedback on how well the argument fits the tactical plan.")
    logical_strength_feedback: str = Field(..., description="Feedback on the logical and rhetorical impact.")
    actionable_refinements: str = Field(..., description="Specific instructions for improvement if not approved.")

class AgentSchema(BaseModel):
    """Schema for the root agent's final argument."""
    agent_name: str = Field(..., description="The name of the agent.")
    round: int = Field(..., description="The current round of the debate.")
    pros_argument: str = Field(..., description="The complete, refined persuasive argument in favor of the topic.")
