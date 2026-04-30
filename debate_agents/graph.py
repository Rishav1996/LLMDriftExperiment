"""
This module defines the LangGraph state machine for the debate simulation.
It handles the orchestration of various agent nodes (Pros, Cons, Topic Extractor).
"""
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END, START

# pylint: disable=import-error
from debate_agents.agents.pros_agent import (
    pros_persona_chain, pros_thinking_chain, pros_critique_chain
)
from debate_agents.agents.cons_agent import (
    cons_persona_chain, cons_thinking_chain, cons_critique_chain
)
from debate_agents.agents.topic_extractor import create_topic_extractor_agent
from debate_agents.tools.memory_tools import write_json_direct, read_json_direct
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import google.genai.errors

class DebateState(TypedDict):
    """
    Represents the state of the debate simulation.
    """
    user_input: str
    topic: str
    pros_argument: str
    cons_argument: str
    round: int
    total_rounds: int
    is_approved: bool
    persona_id: Optional[str]
    suggested_persona_id: Optional[str]

# Initialize agents once
topic_extractor = create_topic_extractor_agent()

# Retry logic
node_retry = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    retry=retry_if_exception_type(google.genai.errors.ServerError),
    before_sleep=lambda retry_state: print(
        f"--- [Retry] Model busy, retrying... (Attempt {retry_state.attempt_number})"
    )
)

async def get_team_context(team_name: str):
    """
    Retrieves the combined context for a specific team from their memory files.
    """
    shared = await read_json_direct("shared_memory.json", team_name)
    persona = await read_json_direct("persona.json", team_name)
    thinking = await read_json_direct("thinking.json", team_name)
    critique = await read_json_direct("critique.json", team_name)
    return (f"Shared Memory: {shared}\nPersona History: {persona}\n"
            f"Thinking History: {thinking}\nCritique History: {critique}")

@node_retry
async def topic_extractor_node(state: DebateState):
    """
    Node that refines the initial user input into a formal debate topic.
    """
    print("\n--- [TopicExtractor] Refining Topic ---")
    response = await topic_extractor.ainvoke({"user_input": state['user_input']})
    topic = response.topic if response else state['user_input']
    await write_json_direct(
        "shared_memory.json", {"topic": topic, "round": 1}, "TopicExtractAgent", 1
    )
    return {"topic": topic, "round": 1}

@node_retry
async def next_round_node(state: DebateState):
    """
    Node that increments the round number and resets internal turn state.
    """
    print(f"\n--- [System] starting Round {state['round'] + 1} ---")
    return {"round": state["round"] + 1, "is_approved": False, "suggested_persona_id": None}

# Pros Nodes
@node_retry
async def pros_persona_node(state: DebateState):
    """
    Node for the Pros Persona Agent to design or refine its adversarial identity.
    """
    print("[Pros] Persona Agent")
    context = (f"Topic: {state['topic']}\n"
               f"Suggested Persona Action: {state.get('suggested_persona_id')}\n"
               + await get_team_context("ProsAgent"))
    res = await pros_persona_chain.ainvoke({"context": context})
    await write_json_direct(
        "persona.json", res.model_dump(), "ProsPersonaAgent", state['round']
    )
    return {"persona_id": res.persona_id, "suggested_persona_id": None}

@node_retry
async def pros_thinking_node(state: DebateState):
    """
    Node for the Pros Thinking Agent to formulate a strategic argument.
    """
    print("[Pros] Thinking Agent")
    context = (f"Topic: {state['topic']}\n"
               f"Active Persona ID: {state.get('persona_id')}\n"
               + await get_team_context("ProsAgent"))
    res = await pros_thinking_chain.ainvoke({"context": context})
    await write_json_direct(
        "thinking.json", res.model_dump(), "ProsThinkingAgent", state['round']
    )
    return {"pros_argument": res.formulated_answer}

@node_retry
async def pros_critique_node(state: DebateState):
    """
    Node for the Pros Critique Agent to audit the draft argument.
    """
    print("[Pros] Critique Agent")
    context = (f"Topic: {state['topic']}\n"
               f"Draft Argument: {state.get('pros_argument')}\n"
               f"Active Persona ID: {state.get('persona_id')}\n"
               + await get_team_context("ProsAgent"))
    res = await pros_critique_chain.ainvoke({"context": context})
    await write_json_direct(
        "critique.json", res.model_dump(), "ProsCritiqueAgent", state['round']
    )
    if res.approved:
        await write_json_direct(
            "shared_memory.json",
            {"pros_argument": state.get("pros_argument"), "persona_id": state.get("persona_id")},
            "ProsCritiqueAgent",
            state['round']
        )
    return {"is_approved": res.approved, "suggested_persona_id": res.suggested_persona_id}

# Cons Nodes
@node_retry
async def cons_persona_node(state: DebateState):
    """
    Node for the Cons Persona Agent to design or refine its adversarial identity.
    """
    print("[Cons] Persona Agent")
    context = (f"Topic: {state['topic']}\n"
               f"Pros Last Argument: {state.get('pros_argument', 'None')}\n"
               f"Suggested Persona Action: {state.get('suggested_persona_id')}\n"
               + await get_team_context("ConsAgent"))
    res = await cons_persona_chain.ainvoke({"context": context})
    await write_json_direct(
        "persona.json", res.model_dump(), "ConsPersonaAgent", state['round']
    )
    return {"persona_id": res.persona_id, "suggested_persona_id": None}

@node_retry
async def cons_thinking_node(state: DebateState):
    """
    Node for the Cons Thinking Agent to formulate a strategic argument.
    """
    print("[Cons] Thinking Agent")
    context = (f"Topic: {state['topic']}\n"
               f"Pros Last Argument: {state.get('pros_argument', 'None')}\n"
               f"Active Persona ID: {state.get('persona_id')}\n"
               + await get_team_context("ConsAgent"))
    res = await cons_thinking_chain.ainvoke({"context": context})
    await write_json_direct(
        "thinking.json", res.model_dump(), "ConsThinkingAgent", state['round']
    )
    return {"cons_argument": res.formulated_answer}

@node_retry
async def cons_critique_node(state: DebateState):
    """
    Node for the Cons Critique Agent to audit the draft argument.
    """
    print("[Cons] Critique Agent")
    context = (f"Topic: {state['topic']}\n"
               f"Draft Argument: {state.get('cons_argument')}\n"
               f"Active Persona ID: {state.get('persona_id')}\n"
               + await get_team_context("ConsAgent"))
    res = await cons_critique_chain.ainvoke({"context": context})
    await write_json_direct(
        "critique.json", res.model_dump(), "ConsCritiqueAgent", state['round']
    )
    if res.approved:
        await write_json_direct(
            "shared_memory.json",
            {"cons_argument": state.get("cons_argument"), "persona_id": state.get("persona_id")},
            "ConsCritiqueAgent",
            state['round']
        )
    return {"is_approved": res.approved, "suggested_persona_id": res.suggested_persona_id}

def should_continue_pros(state: DebateState):
    """
    Determines if the Pros team should continue iterating or pass to the Cons team.
    """
    return "pros_persona" if not state.get("is_approved", False) else "cons_persona"

def should_continue_cons(state: DebateState):
    """
    Determines if the Cons team should continue iterating, go to next round, or end.
    """
    if not state.get("is_approved", False):
        return "cons_persona"
    if state["round"] < state["total_rounds"]:
        return "next_round"
    return END

def create_debate_graph():
    """
    Compiles the LangGraph workflow for the debate simulation.
    """
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

    workflow.add_edge("pros_persona", "pros_thinking")
    workflow.add_edge("pros_thinking", "pros_critique")
    workflow.add_conditional_edges("pros_critique", should_continue_pros, {
        "pros_persona": "pros_persona",
        "cons_persona": "cons_persona"
    })

    workflow.add_edge("cons_persona", "cons_thinking")
    workflow.add_edge("cons_thinking", "cons_critique")
    workflow.add_conditional_edges("cons_critique", should_continue_cons, {
        "cons_persona": "cons_persona",
        "next_round": "next_round",
        END: END
    })

    workflow.add_edge("next_round", "pros_persona")

    return workflow.compile()
