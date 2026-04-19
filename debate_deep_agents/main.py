import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from debate_deep_agents.graph import create_debate_graph

def generate_graph_image(graph):
    """
    Generates and saves a visualization of the LangGraph workflow.
    """
    try:
        path = "debate_deep_agents/assets/graph.png"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
        print(f"Graph saved to {path}")
    except Exception as e:
        print(f"Error generating graph: {e}")

async def main():
    graph = create_debate_graph()
    generate_graph_image(graph)
    
    topic = input("Enter the debate topic: ")
    rounds = int(input("Enter the number of rounds: "))
    
    initial_state = {
        "user_input": topic,
        "topic": topic,
        "pros_argument": "",
        "cons_argument": "",
        "round": 1,
        "total_rounds": rounds
    }
    
    print(f"Starting debate simulation for {rounds} rounds...")
    result = await graph.ainvoke(initial_state)
    print("Debate finished.")
    print(f"Pros Argument: {result.get('pros_argument')}")
    print(f"Cons Argument: {result.get('cons_argument')}")

if __name__ == "__main__":
    asyncio.run(main())
