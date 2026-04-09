from pydantic import BaseModel, Field

class CritiqueSchema(BaseModel):
    """Schema for the adversarial critique of an argument."""
    approved: bool = Field(..., description="Whether the argument meets the competitive threshold.")
    persona_consistency_feedback: str = Field(..., description="Feedback on maintaining the established voice and character.")
    strategic_alignment_feedback: str = Field(..., description="Feedback on how well the argument fits the tactical plan.")
    logical_strength_feedback: str = Field(..., description="Feedback on the logical and rhetorical impact.")
    actionable_refinements: str = Field(..., description="Specific instructions for improvement if not approved.")
