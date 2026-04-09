from pydantic import BaseModel, Field
from typing import List

class PersonaSchema(BaseModel):
    """Schema for the competitive adversarial persona profile (Cons)."""
    agent_name: str = Field(..., description="The name of the agent providing the response.")
    name: str = Field(..., description="The name of the persona.")
    voice_and_tone: str = Field(..., description="The speaking style, vocabulary level, and skeptical resonance.")
    adversarial_stance: str = Field(..., description="How they specifically target and challenge the 'Pros' position.")
    background: str = Field(..., description="A concise backstory that shapes their skeptical viewpoint.")
    core_values: List[str] = Field(..., description="Fundamental principles driving their caution or opposition.")
    motivation: str = Field(..., description="Why they feel strongly against the specific issue.")
    persuasion_strategy: str = Field(..., description="Preferred methods of influencing others (e.g., risk highlighting).")
    response_style: str = Field(..., description="How they handle optimistic claims.")
    resilience: str = Field(..., description="How they maintain their skeptical stance under pressure.")
