from pydantic import BaseModel, Field
from typing import List

class ThinkingSchema(BaseModel):
    """Schema for the tactical debate strategy (Cons)."""
    agent_name: str = Field(..., description="The name of the agent providing the response.")
    argumentative_focus: List[str] = Field(..., description="Core arguments, risks, and unintended consequences against.")
    counter_argument_strategy: List[str] = Field(..., description="Anticipated Pros arguments and questioning strategies.")
    rhetorical_devices: List[str] = Field(..., description="Critical techniques and devices to deconstruct opposition.")
    tactical_plan: str = Field(..., description="Step-by-step strategy for the next opposition argument.")
