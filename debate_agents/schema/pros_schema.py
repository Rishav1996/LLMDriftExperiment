"""
Pydantic schemas for the Pros team agents.
Ensures structured output from the LLM for persona, thinking, and critique phases.
"""
from typing import Optional
from pydantic import BaseModel, Field

class PersonaSchema(BaseModel):
    """
    Simplified schema for the competitive adversarial persona profile (Pros).
    """
    agent_name: str = Field(..., description="The name of the agent (ProsPersonaAgent).")
    round: int = Field(..., description="The current round of the debate.")
    persona_id: str = Field(
        ..., description="A unique identifier for this persona (e.g., 'pros-v1')."
    )
    skip_persona_generation: bool = Field(
        False, description="Set True to skip generating a new persona and reuse the previous one."
    )
    persona_profile: str = Field(
        ..., description="The comprehensive adversarial identity description."
    )

class ThinkingSchema(BaseModel):
    """
    Simplified schema for the tactical debate strategy (Pros).
    """
    agent_name: str = Field(..., description="The name of the agent (ProsThinkingAgent).")
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
    Simplified schema for the adversarial critique (Pros).
    """
    agent_name: str = Field(..., description="The name of the agent (ProsCritiqueAgent).")
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
    Schema for the root agent's final argument (Pros).
    """
    agent_name: str = Field(..., description="The name of the agent.")
    round: int = Field(..., description="The current round of the debate.")
    pros_argument: str = Field(
        ..., description="The complete, refined persuasive argument in favor of the topic."
    )
