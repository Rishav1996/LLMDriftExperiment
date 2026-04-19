import os
from langchain_core.prompts import ChatPromptTemplate
from debate_deep_agents.config.config import model
from debate_deep_agents.schema.pros_schema import PersonaSchema, ThinkingSchema, CritiqueSchema, AgentSchema

def create_subagent_chain(prompt_path, schema):
    with open(prompt_path, "r") as f:
        instruction = f.read()
    prompt = ChatPromptTemplate.from_messages([("system", instruction), ("user", "{context}")])
    return prompt | model.with_structured_output(schema)

# Create Pros subagent chains
pros_persona_chain = create_subagent_chain("debate_deep_agents/prompts/pros/persona_agent.md", PersonaSchema)
pros_thinking_chain = create_subagent_chain("debate_deep_agents/prompts/pros/thinking_agent.md", ThinkingSchema)
pros_critique_chain = create_subagent_chain("debate_deep_agents/prompts/pros/critique_agent.md", CritiqueSchema)
pros_root_chain = create_subagent_chain("debate_deep_agents/prompts/pros/agent.md", AgentSchema)
