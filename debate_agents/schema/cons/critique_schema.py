from pydantic import BaseModel, Field

class CritiqueSchema(BaseModel):
    """Schema for the adversarial critique (Cons)."""
    approved: bool = Field(..., description="Whether the argument meets the competitive threshold.")
    persona_consistency_feedback: str = Field(..., description="Feedback on maintaining the skeptical voice and character.")
    strategic_alignment_feedback: str = Field(..., description="Feedback on how well the argument challenges the 'Pros'.")
    logical_strength_feedback: str = Field(..., description="Feedback on the critical and rhetorical impact.")
    actionable_refinements: str = Field(..., description="Specific instructions for improvement if not approved.")
