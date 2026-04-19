from typing import TypedDict, Any
from langgraph.graph import StateGraph, END, START
from debate_deep_agents.agents.deep_pros_agent import create_pros_deep_agent
from debate_deep_agents.agents.deep_cons_agent import create_cons_deep_agent
from debate_deep_agents.agents.deep_topic_extractor import create_topic_extractor_deep_agent

class DebateState(TypedDict):
    user_input: str
    topic: str
    pros_argument: str
    cons_argument: str
    round: int
    total_rounds: int

# Initialize agents once
topic_extractor = create_topic_extractor_deep_agent()
pros_agent = create_pros_deep_agent()
cons_agent = create_cons_deep_agent()

async def topic_extractor_node(state: DebateState):
    print(f"\n--- [TopicExtractor] Refining Topic ---")
    result = await topic_extractor.ainvoke({"messages": [("user", f"Topic: {state['user_input']}") ]})
    response = result.get("response")
    topic = response.topic if response else state['user_input']
    return {"topic": topic, "round": 1}

async def pros_node(state: DebateState):
    print(f"\n--- [ProsAgent] Round {state['round']} ---")
    # In the new flow, agents read their own context from files using tools.
    # We just trigger them.
    result = await pros_agent.ainvoke({"messages": [("user", f"Round {state['round']}. Proceed with your turn.")]})
    
    response = result.get("response")
    pros_arg = response.pros_argument if response else "Error generating argument."
    
    return {"pros_argument": pros_arg}

async def cons_node(state: DebateState):
    print(f"\n--- [ConsAgent] Round {state['round']} ---")
    result = await cons_agent.ainvoke({"messages": [("user", f"Round {state['round']}. Proceed with your turn.")]})
    
    response = result.get("response")
    cons_arg = response.cons_argument if response else "Error generating argument."
    
    return {"cons_argument": cons_arg, "round": state["round"] + 1}


def should_continue(state: DebateState):
    if state["round"] < state["total_rounds"]:
        return "pros"
    return END

def create_debate_graph():
    """
    Creates a LangGraph workflow for the adversarial debate with multi-round support.
    """
    workflow = StateGraph(DebateState)
    
    workflow.add_node("topic_extractor", topic_extractor_node)
    workflow.add_node("pros", pros_node)
    workflow.add_node("cons", cons_node)
    
    workflow.add_edge(START, "topic_extractor")
    workflow.add_edge("topic_extractor", "pros")
    workflow.add_edge("pros", "cons")
    workflow.add_conditional_edges("cons", should_continue)
    
    return workflow.compile()
