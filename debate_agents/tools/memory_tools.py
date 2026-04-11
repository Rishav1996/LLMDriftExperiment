import os
import shutil
import json
from typing import Dict, Any, Optional

BASE_MEMORY_DIR = "debate_agents/memory"

def refresh_memory():
    """
    Clears the entire memory directory and initializes it with an empty 
    JSON list structure for all required agent files.

    Returns:
        None
    """
    if os.path.exists(BASE_MEMORY_DIR):
        shutil.rmtree(BASE_MEMORY_DIR)
    
    pros_dir = os.path.join(BASE_MEMORY_DIR, "pros_memory")
    cons_dir = os.path.join(BASE_MEMORY_DIR, "cons_memory")
    os.makedirs(pros_dir, exist_ok=True)
    os.makedirs(cons_dir, exist_ok=True)
    
    files_to_init = [
        os.path.join(BASE_MEMORY_DIR, "shared_memory.json"),
        os.path.join(pros_dir, "persona.json"),
        os.path.join(pros_dir, "thinking.json"),
        os.path.join(pros_dir, "critique.json"),
        os.path.join(cons_dir, "persona.json"),
        os.path.join(cons_dir, "thinking.json"),
        os.path.join(cons_dir, "critique.json"),
    ]
    for file_path in files_to_init:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

def get_memory_path(agent_name: str, filename: str) -> str:
    """
    Determines the correct file system path for a given memory file 
    based on the agent's name and team classification (Pros or Cons).

    Args:
        agent_name (str): The name of the agent.
        filename (str): The name of the file being accessed.

    Returns:
        str: The full path to the memory file.
    """
    if filename == "shared_memory.json":
        return os.path.join(BASE_MEMORY_DIR, filename)
        
    if "pros_memory" in filename or "cons_memory" in filename:
        return os.path.join(BASE_MEMORY_DIR, filename)
    
    sub_dir = "pros_memory" if "Pros" in agent_name else "cons_memory" if "Cons" in agent_name else ""
    return os.path.join(BASE_MEMORY_DIR, sub_dir, filename)

async def write_json_direct(filename: str, content: Any, agent_name: str, round_num: Optional[int] = None) -> None:
    """
    Appends an entry containing the agent's name, content, and optional 
    round number to the specified JSON file. Creates the file if it does 
    not exist.

    Args:
        filename (str): The target JSON file name.
        content (Any): The data to save.
        agent_name (str): The name of the agent saving the content.
        round_num (Optional[int]): The current debate round, if applicable.

    Returns:
        None
    """
    file_path = get_memory_path(agent_name, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try: data = json.load(f)
            except: data = []
    
    entry = {"agent": agent_name, "content": content}
    if round_num is not None:
        entry["round"] = round_num
        
    data.append(entry)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

async def read_json_direct(filename: str, agent_name: str) -> Any:
    """
    Reads the content of a JSON memory file for a specific agent. 
    Returns an empty list if the file does not exist.

    Args:
        filename (str): The target JSON file name.
        agent_name (str): The name of the agent accessing the memory.

    Returns:
        Any: The contents of the JSON file as a Python object.
    """
    file_path = get_memory_path(agent_name, filename)
    if not os.path.exists(file_path): return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Note: The original ADK tool wrappers (FunctionTool) are removed for LangGraph.
# Node implementations directly use write_json_direct and read_json_direct.
