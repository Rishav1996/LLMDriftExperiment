from google.adk.apps.app import App
from google.adk.agents import LoopAgent, SequentialAgent
from debate_agents.agents.pros.agent import get_pros_agent
from debate_agents.agents.cons.agent import get_cons_agent
from debate_agents.agents.topic_extract_agent import get_topic_extract_agent
from debate_agents.config import MAX_ROUNDS, GEMINI_MODEL_ADAPTER # Updated import
from google.adk.plugins import ReflectAndRetryToolPlugin

# Root agent for ADK orchestration
debate_orchestrator = SequentialAgent(
    name="DebateOrchestrator",
    sub_agents=[
        get_topic_extract_agent(), # Instantiate directly for SequentialAgent
        LoopAgent(
            name="DebateLoop",
            sub_agents=[
                get_pros_agent(), # Instantiate pros agent
                get_cons_agent()  # Instantiate cons agent
            ],
            max_iterations=MAX_ROUNDS
        )
    ]
)

root_agent = debate_orchestrator

# Initialize the ADK App with the root agent and the retry plugin
app = App(
    name="debate_agents", 
    root_agent=root_agent,
    plugins=[
        ReflectAndRetryToolPlugin(max_retries=3), 
    ],
)

if __name__ == "__main__":
    app.run()
