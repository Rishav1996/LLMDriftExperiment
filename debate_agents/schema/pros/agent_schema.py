from pydantic import BaseModel, Field

class AgentSchema(BaseModel):
    """Schema for the root agent's final argument."""
    agent_name: str = Field(..., description="The name of the agent providing the response.")
    pros_argument: str = Field(..., description="The complete, refined persuasive argument in favor of the topic.")
