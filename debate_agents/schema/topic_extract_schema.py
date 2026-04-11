from pydantic import BaseModel, Field

class TopicExtractSchema(BaseModel):
    """
    Schema for extracting the debate topic.

    Attributes:
        agent_name (str): The name of the agent (TopicExtractAgent).
        topic (str): The main topic or motion to be debated.
        round (int): The current round of the debate.
    """
    agent_name: str = Field(..., description="The name of the agent (TopicExtractAgent).")
    topic: str = Field(..., description="The main topic or motion to be debated.")
    round: int = Field(..., description="The initial round number (usually 1).")
