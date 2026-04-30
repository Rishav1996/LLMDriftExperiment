"""
Pydantic schemas for the Cons team agents.
Defines the structure for persona, strategy, and critique outputs for the opposition.
"""
from typing import Optional
from pydantic import BaseModel, Field

class PersonaSchema(BaseModel):
    """
    Schema for the competitive adversarial persona profile (Cons).
    """
    agent_name: str = Field(..., description="The name of the agent (ConsPersonaAgent).")
    round: int = Field(..., description="The current round of the debate.")
    persona_id: str = Field(
        ..., description="A unique identifier for this persona (e.g., 'cons-v1')."
    )
    skip_persona_generation: bool = Field(
        False, description="Set True to skip generating a new persona."
    )
    persona_profile: str = Field(
        ..., description="The comprehensive adversarial identity description."
    )

class ThinkingSchema(BaseModel):
    """
    Schema for the tactical debate strategy (Cons).
    """
    agent_name: str = Field(..., description="The name of the agent (ConsThinkingAgent).")
    round: int = Field(..., description="The current round of the debate.")
    persona_id: str = Field(
        ..., description="Reference ID of the active persona being used."
    )
    thought_process: str = Field(
        ..., description="Step-by-step reasoning and strategic planning."
    )
    formulated_answer: str = Field(
        ..., description="A high-fidelity draft of the persuasive argument."
    )

class CritiqueSchema(BaseModel):
    """
    Schema for the adversarial critique (Cons).
    """
    agent_name: str = Field(..., description="The name of the agent (ConsCritiqueAgent).")
    round: int = Field(..., description="The current round of the debate.")
    persona_id: str = Field(
        ..., description="Reference ID of the persona being critiqued."
    )
    approved: bool = Field(
        ..., description="Whether the argument meets the competitive threshold."
    )
    critique_feedback: str = Field(
        ..., description="Consolidated feedback on consistency and strategy."
    )
    actionable_refinements: str = Field(
        ..., description="Specific instructions for improvement."
    )
    suggested_persona_id: Optional[str] = Field(
        None,
        description="ID of an existing persona to revert to, or 'new' to trigger new generation."
    )

class AgentSchema(BaseModel):
    """
    Schema for the Cons root agent's final argument.
    """
    agent_name: str = Field(..., description="The name of the agent.")
    round: int = Field(..., description="The current round of the debate.")
    cons_argument: str = Field(
        ..., description="The complete, refined persuasive argument."
    )
