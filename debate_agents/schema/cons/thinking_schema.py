from pydantic import BaseModel, Field
from typing import List

class ThinkingSchema(BaseModel):
    """Schema for the tactical debate strategy (Cons)."""
    argumentative_focus: List[str] = Field(..., description="Core arguments, risks, and unintended consequences against.")
    counter_argument_strategy: List[str] = Field(..., description="Anticipated Pros arguments and questioning strategies.")
    rhetorical_devices: List[str] = Field(..., description="Critical techniques and devices to deconstruct opposition.")
    tactical_plan: str = Field(..., description="Step-by-step strategy for the next opposition argument.")
    formulated_answer: str = Field(..., description="A draft version of the skeptical argument based on this strategy.")
