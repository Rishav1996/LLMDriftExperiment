from google.adk.agents import LoopAgent, SequentialAgent
from debate_agents.agents.pros.agent import get_pros_agent # Updated path and file name
from debate_agents.agents.cons.agent import get_cons_agent # Updated path and file name
from debate_agents.agents.topic_extract_agent import get_topic_extract_agent
from debate_agents.config import MAX_ROUNDS


# Instantiate the sub-agents
pros_agent = get_pros_agent()
cons_agent = get_cons_agent()
topic_extract_agent = get_topic_extract_agent()

# Orchestrate them in a LoopAgent
debate_loop = LoopAgent(
    name="DebateLoop",
    sub_agents=[
        pros_agent,
        cons_agent
    ],
    max_iterations=MAX_ROUNDS
)

# Root agent for ADK orchestration
debate_orchestrator = SequentialAgent(
    name="DebateOrchestrator",
    sub_agents=[
        topic_extract_agent,
        debate_loop
    ]
)

root_agent = debate_orchestrator

if __name__ == "__main__":
    print(f"Orchestrator initialized with agents: {[a.name for a in debate_orchestrator.sub_agents]}")
