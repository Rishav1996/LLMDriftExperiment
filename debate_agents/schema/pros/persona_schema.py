from pydantic import BaseModel, Field
from typing import List

class PersonaSchema(BaseModel):
    """Schema for the competitive adversarial persona profile."""
    voice_and_tone: str = Field(..., description="The speaking style, vocabulary level, and emotional resonance.")
    adversarial_stance: str = Field(..., description="How they specifically target and challenge the opposing position.")
    background: str = Field(..., description="A concise backstory that shapes their viewpoint.")
    core_values: List[str] = Field(..., description="Fundamental principles driving their passion.")
    motivation: str = Field(..., description="Why they feel strongly about the issue.")
    persuasion_strategy: str = Field(..., description="Preferred methods of influencing others.")
    response_style: str = Field(..., description="How they handle opposition.")
    resilience: str = Field(..., description="How they maintain their stance under pressure.")
