from pydantic import BaseModel, Field
from typing import List

class ThinkingSchema(BaseModel):
    """Schema for the tactical debate strategy."""
    agent_name: str = Field(..., description="The name of the agent providing the response.")
    argumentative_focus: List[str] = Field(..., description="Core arguments and evidence in favor.")
    counter_argument_strategy: List[str] = Field(..., description="Anticipated counters and planned rebuttals.")
    rhetorical_devices: List[str] = Field(..., description="Persuasive techniques and devices to be used.")
    tactical_plan: str = Field(..., description="Step-by-step strategy for the next argument.")
