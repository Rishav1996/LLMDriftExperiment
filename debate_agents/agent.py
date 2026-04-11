import os
from typing import TypedDict, List, Optional, Any
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from debate_agents.config import MAX_ROUNDS
from debate_agents.agents.topic_extract_agent import topic_extractor_node
from debate_agents.agents.pros_agent import pros_persona_node, pros_thinking_node, pros_critique_node
from debate_agents.agents.cons_agent import cons_persona_node, cons_thinking_node, cons_critique_node

# 1. Define Graph State
class DebateState(TypedDict):
    """
    Represents the state of the debate simulation.
    """
    topic: str
    round: int
    current_team: str # "pros" or "cons"
    pros_iteration: int
    cons_iteration: int
    last_output: Any
    is_approved: bool
    user_input: str

# 2. Define Edge Logic
def should_continue_pros(state: DebateState) -> str:
    """
    Determines the next node for the Pro team.
    
    Args:
        state (DebateState): The current debate state.

    Returns:
        str: The name of the next node to execute.
    """
    if state["is_approved"] or state.get("pros_iteration", 0) >= 5:
        return "cons_persona"
    return "pros_persona"

def should_continue_cons(state: DebateState) -> str:
    """
    Determines the next node for the Con team.
    
    Args:
        state (DebateState): The current debate state.

    Returns:
        str: The name of the next node to execute or END.
    """
    if state["is_approved"] or state.get("cons_iteration", 0) >= 5:
        if state["round"] >= MAX_ROUNDS:
            return END
        return "next_round"
    return "cons_persona"

def next_round_node(state: DebateState) -> Dict[str, Any]:
    """
    Updates the state to increment the round number.
    
    Args:
        state (DebateState): The current debate state.

    Returns:
        Dict[str, Any]: The updated state with the incremented round.
    """
    return {"round": state["round"] + 1, "pros_iteration": 0, "cons_iteration": 0}

# 3. Build Graph
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
    "cons_persona": "cons_persona",
    "pros_persona": "pros_persona"
})

workflow.add_edge("cons_persona", "cons_thinking")
workflow.add_edge("cons_thinking", "cons_critique")
workflow.add_conditional_edges("cons_critique", should_continue_cons, {
    "next_round": "next_round",
    "cons_persona": "cons_persona",
    END: END
})

workflow.add_edge("next_round", "pros_persona")

# Compile
app = workflow.compile()

def generate_graph_image():
    """
    Generates and saves a visualization of the LangGraph workflow.
    
    Returns:
        None
    """
    try:
        path = "debate_agents/assets/graph.png"
        with open(path, "wb") as f:
            f.write(app.get_graph().draw_mermaid_png())
        print(f"Graph saved to {path}")
    except Exception as e:
        print(f"Error generating graph: {e}")

if __name__ == "__main__":
    import asyncio
    
    # Generate graph on start
    generate_graph_image()

    async def main():
        user_input = input("Enter debate topic: ")
        async for output in app.astream({"user_input": user_input, "round": 0, "pros_iteration": 0, "cons_iteration": 0, "is_approved": False}):
            for key, value in output.items():
                print(f"Node '{key}':")
        print("\nDebate Finished!")

    asyncio.run(main())
