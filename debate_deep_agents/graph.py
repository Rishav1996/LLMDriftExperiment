from typing import TypedDict, Any
from langgraph.graph import StateGraph, END, START
from debate_deep_agents.agents.pros_agent import pros_persona_chain, pros_thinking_chain, pros_critique_chain, pros_root_chain
from debate_deep_agents.agents.cons_agent import cons_persona_chain, cons_thinking_chain, cons_critique_chain, cons_root_chain
from debate_deep_agents.agents.topic_extractor import create_topic_extractor_agent
from debate_deep_agents.tools.memory_tools import write_json_direct, read_json_direct
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import google.genai.errors

class DebateState(TypedDict):
    user_input: str
    topic: str
    pros_argument: str
    cons_argument: str
    round: int
    total_rounds: int
    is_approved: bool

# Initialize agents once
topic_extractor = create_topic_extractor_agent()

# Retry logic
node_retry = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    retry=retry_if_exception_type(google.genai.errors.ServerError),
    before_sleep=lambda retry_state: print(f"--- [Retry] Model busy, retrying... (Attempt {retry_state.attempt_number})")
)

@node_retry
async def topic_extractor_node(state: DebateState):
    print(f"\n--- [TopicExtractor] Refining Topic ---")
    response = await topic_extractor.ainvoke({"user_input": state['user_input']})
    topic = response.topic if response else state['user_input']
    await write_json_direct("shared_memory.json", {"topic": topic, "round": 1}, "TopicExtractAgent", 1)
    return {"topic": topic, "round": 1}

@node_retry
async def next_round_node(state: DebateState):
    print(f"\n--- [System] Incrementing Round ---")
    return {"round": state["round"] + 1, "is_approved": False}

# Pros Nodes
@node_retry
async def pros_persona_node(state: DebateState):
    print(f"[Pros] Persona Agent")
    context = f"Topic: {state['topic']}"
    res = await pros_persona_chain.ainvoke({"context": context})
    await write_json_direct("persona.json", res.model_dump(), "ProsPersonaAgent", state['round'])
    return {}

@node_retry
async def pros_thinking_node(state: DebateState):
    print(f"[Pros] Thinking Agent")
    context = f"Topic: {state['topic']}"
    res = await pros_thinking_chain.ainvoke({"context": context})
    await write_json_direct("thinking.json", res.model_dump(), "ProsThinkingAgent", state['round'])
    return {}

@node_retry
async def pros_critique_node(state: DebateState):
    print(f"[Pros] Critique Agent")
    context = f"Topic: {state['topic']}"
    res = await pros_critique_chain.ainvoke({"context": context})
    await write_json_direct("critique.json", res.model_dump(), "ProsCritiqueAgent", state['round'])
    if res.approved:
        await write_json_direct("shared_memory.json", {"pros_argument": "Finalized argument"}, "ProsCritiqueAgent", state['round'])
    return {"is_approved": res.approved}

# Cons Nodes
@node_retry
async def cons_persona_node(state: DebateState):
    print(f"[Cons] Persona Agent")
    context = f"Topic: {state['topic']}\nPros Last Argument: {state.get('pros_argument', 'None')}"
    res = await cons_persona_chain.ainvoke({"context": context})
    await write_json_direct("persona.json", res.model_dump(), "ConsPersonaAgent", state['round'])
    return {}

@node_retry
async def cons_thinking_node(state: DebateState):
    print(f"[Cons] Thinking Agent")
    context = f"Topic: {state['topic']}\nPros Last Argument: {state.get('pros_argument', 'None')}"
    res = await cons_thinking_chain.ainvoke({"context": context})
    await write_json_direct("thinking.json", res.model_dump(), "ConsThinkingAgent", state['round'])
    return {}

@node_retry
async def cons_critique_node(state: DebateState):
    print(f"[Cons] Critique Agent")
    context = f"Topic: {state['topic']}\nPros Last Argument: {state.get('pros_argument', 'None')}"
    res = await cons_critique_chain.ainvoke({"context": context})
    await write_json_direct("critique.json", res.model_dump(), "ConsCritiqueAgent", state['round'])
    if res.approved:
        await write_json_direct("shared_memory.json", {"cons_argument": "Finalized argument"}, "ConsCritiqueAgent", state['round'])
    return {"is_approved": res.approved}

def should_continue_pros(state: DebateState):
    return "pros_persona" if not state["is_approved"] else "cons_persona"

def should_continue_cons(state: DebateState):
    if not state["is_approved"]:
        return "cons_persona"
    if state["round"] < state["total_rounds"]:
        return "next_round"
    return END

def create_debate_graph():
    workflow = StateGraph(DebateState)
    workflow.add_node("topic_extractor", topic_extractor_node)
    workflow.add_node("pros_persona", pros_persona_node)
    workflow.add_node("pros_thinking", pros_thinking_node)
    workflow.add_node("pros_critique", pros_critique_node)
    workflow.add_node("cons_persona", cons_persona_node)
    workflow.add_node("cons_thinking", cons_thinking_node)
    workflow.add_node("cons_critique", cons_critique_node)
    workflow.add_node("next_round", next_round_node)
    
    workflow.add_edge(START, "topic_extractor")
    workflow.add_edge("topic_extractor", "pros_persona")
    
    workflow.add_edge("pros_critique", "cons_persona") # Connect Pros to Cons

    # Pros nodes
    workflow.add_edge("pros_persona", "pros_thinking")
    workflow.add_edge("pros_thinking", "pros_critique")
    
    # Pros critique logic with conditional return
    workflow.add_conditional_edges("pros_critique", should_continue_pros, {
        "pros_persona": "pros_persona",
        "cons_persona": "cons_persona"
    })
    
    # Cons critique logic with conditional return
    workflow.add_conditional_edges("cons_critique", should_continue_cons, {
        "cons_persona": "cons_persona",
        "next_round": "next_round",
        END: END
    })
    
    workflow.add_edge("next_round", "pros_persona")
    
    return workflow.compile()
