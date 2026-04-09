from pydantic import BaseModel, Field

class AgentSchema(BaseModel):
    """Schema for the Cons root agent's final argument."""
    cons_argument: str = Field(..., description="The complete, refined persuasive argument against the topic.")
