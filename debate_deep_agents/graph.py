from typing import TypedDict, Any
from langgraph.graph import StateGraph, END
from debate_deep_agents.agents.deep_pros_agent import create_pros_deep_agent
from debate_deep_agents.agents.deep_cons_agent import create_cons_deep_agent

class DebateState(TypedDict):
    user_input: str
    topic: str
    pros_argument: str
    cons_argument: str
    round: int
    total_rounds: int

# Initialize agents once
pros_agent = create_pros_deep_agent()
cons_agent = create_cons_deep_agent()
async def pros_node(state: DebateState):
    # For testing, let's just return a static dict.
    return {"pros_argument": "This is a test argument"}

async def cons_node(state: DebateState):
    # For testing, let's just return a static dict.
    return {"cons_argument": "This is a test cons argument", "round": state["round"] + 1}


def should_continue(state: DebateState):
    if state["round"] <= state["total_rounds"]:
        return "pros"
    return END

def create_debate_graph():
    """
    Creates a LangGraph workflow for the adversarial debate with multi-round support.
    """
    workflow = StateGraph(DebateState)
    
    workflow.add_node("pros", pros_node)
    workflow.add_node("cons", cons_node)
    
    workflow.set_entry_point("pros")
    workflow.add_edge("pros", "cons")
    workflow.add_conditional_edges("cons", should_continue)
    
    return workflow.compile()
