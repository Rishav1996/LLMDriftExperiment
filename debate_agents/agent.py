import atexit
import mlflow
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

# 1. Initialize MLflow Experiment
# Using the local MLflow server with SQLite backend as per README.md
mlflow.set_tracking_uri("http://localhost:5000")
experiment = mlflow.set_experiment("LLM-Drift-Debate")

# 2. Configure OpenTelemetry with MLflow OTLP endpoint
# ADK will automatically pick up this global tracer provider for its internal spans.
resource = Resource.create({"service.name": "debate-orchestrator"})
exporter = OTLPSpanExporter(
    endpoint="http://localhost:5000/v1/traces",
    headers={"x-mlflow-experiment-id": experiment.experiment_id}
)

provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

# Ensure spans are flushed on exit
atexit.register(provider.shutdown)

# 3. Import ADK components and project agents AFTER tracing is configured
from google.adk.apps.app import App
from google.adk.agents import LoopAgent, SequentialAgent
from debate_agents.agents.pros.agent import get_pros_agent
from debate_agents.agents.cons.agent import get_cons_agent
from debate_agents.agents.topic_extract_agent import get_topic_extract_agent
from debate_agents.config import MAX_ROUNDS, GEMINI_MODEL_ADAPTER 
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
