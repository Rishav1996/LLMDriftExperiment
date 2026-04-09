from pydantic import BaseModel, Field

class TopicExtractSchema(BaseModel):
    """Schema for extracting the debate topic."""
    topic: str = Field(..., description="The main topic or motion to be debated.")
