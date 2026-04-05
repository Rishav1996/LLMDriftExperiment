import os
import mlflow
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# --- MLflow & OpenTelemetry Tracing Setup ---
# This MUST happen before any ADK agents are initialized
mlflow.set_tracking_uri("http://localhost:5000")

EXPERIMENT_NAME = "LLM Drift Debate"
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment is None:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
else:
    experiment_id = experiment.experiment_id

OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://localhost:5000/v1/traces")

exporter = OTLPSpanExporter(
    endpoint=OTLP_ENDPOINT,
    headers={"x-mlflow-experiment-id": experiment_id}
)

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)

print(f"MLflow tracing enabled for experiment: '{EXPERIMENT_NAME}' (ID: {experiment_id})")

# --- ADK Imports ---
from google.adk.agents import LoopAgent, SequentialAgent
from debate_agents.agents.pros_agent import get_pros_agent
from debate_agents.agents.cons_agent import get_cons_agent
from debate_agents.agents.topic_extract_agent import get_topic_extract_agent
from debate_agents.config import MAX_ROUNDS

# 1. Instantiate the Topic Extraction Agent
topic_extract_agent = get_topic_extract_agent()

# 2. Instantiate the Debate Loop Sub-Agents
pros_agent = get_pros_agent()
cons_agent = get_cons_agent()

# 3. Create the Debate Loop Agent
debate_loop = LoopAgent(
    name="DebateLoop",
    sub_agents=[
        pros_agent,
        cons_agent
    ],
    max_iterations=MAX_ROUNDS
)

# 4. Create the Sequential Root Agent
# This will first extract the topic, then run the debate loop.
debate_orchestrator = SequentialAgent(
    name="DebateOrchestrator",
    sub_agents=[
        topic_extract_agent,
        debate_loop
    ]
)

# Root agent for ADK orchestration
root_agent = debate_orchestrator

if __name__ == "__main__":
    print(f"Orchestrator initialized with agents: {[a.name for a in debate_orchestrator.sub_agents]}")
