from pydantic import BaseModel, Field

class AgentSchema(BaseModel):
    """Schema for the root agent's final argument."""
    pros_argument: str = Field(..., description="The complete, refined persuasive argument in favor of the topic.")
