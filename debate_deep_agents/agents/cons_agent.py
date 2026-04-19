import os
from langchain_core.prompts import ChatPromptTemplate
from debate_deep_agents.config.config import model
from debate_deep_agents.schema.cons_schema import PersonaSchema, ThinkingSchema, CritiqueSchema, AgentSchema

def create_subagent_chain(prompt_path, schema):
    with open(prompt_path, "r") as f:
        instruction = f.read()
    prompt = ChatPromptTemplate.from_messages([("system", instruction), ("user", "{context}")])
    return prompt | model.with_structured_output(schema)

# Create Cons subagent chains
cons_persona_chain = create_subagent_chain("debate_deep_agents/prompts/cons/persona_agent.md", PersonaSchema)
cons_thinking_chain = create_subagent_chain("debate_deep_agents/prompts/cons/thinking_agent.md", ThinkingSchema)
cons_critique_chain = create_subagent_chain("debate_deep_agents/prompts/cons/critique_agent.md", CritiqueSchema)
cons_root_chain = create_subagent_chain("debate_deep_agents/prompts/cons/agent.md", AgentSchema)
