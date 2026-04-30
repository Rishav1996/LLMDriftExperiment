"""
This module initializes the chains for the Pros team agents.
It creates specialized chains for persona design, thinking, and critique.
"""
from langchain_core.prompts import ChatPromptTemplate

# pylint: disable=import-error
from debate_agents.config.config import model
from debate_agents.schema.pros_schema import (
    PersonaSchema, ThinkingSchema, CritiqueSchema, AgentSchema
)

def create_subagent_chain(prompt_path, schema):
    """
    Creates a LangChain chain for a subagent using a system prompt and a structured output schema.
    """
    with open(prompt_path, "r", encoding="utf-8") as f:
        instruction = f.read()
    prompt = ChatPromptTemplate.from_messages([
        ("system", instruction),
        ("user", "{context}")
    ])
    return prompt | model.with_structured_output(schema)

# Create Pros subagent chains
pros_persona_chain = create_subagent_chain(
    "debate_agents/prompts/pros/persona_agent.md", PersonaSchema
)
pros_thinking_chain = create_subagent_chain(
    "debate_agents/prompts/pros/thinking_agent.md", ThinkingSchema
)
pros_critique_chain = create_subagent_chain(
    "debate_agents/prompts/pros/critique_agent.md", CritiqueSchema
)
pros_root_chain = create_subagent_chain(
    "debate_agents/prompts/pros/agent.md", AgentSchema
)
