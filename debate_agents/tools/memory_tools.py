import os
import shutil
import json
from typing import Dict, Any

BASE_MEMORY_DIR = "debate_agents/memory"

def refresh_memory():
    """Clears the memory directory and initializes the required structure."""
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
    Constructs the file path.
    If filename is shared_memory.json, use it directly in BASE_MEMORY_DIR.
    If filename already includes the team folder, use it directly.
    Otherwise, prepend team folder based on agent_name.
    """
    if filename == "shared_memory.json":
        return os.path.join(BASE_MEMORY_DIR, filename)
        
    if "pros_memory" in filename or "cons_memory" in filename:
        return os.path.join(BASE_MEMORY_DIR, filename)
    
    sub_dir = "pros_memory" if "Pros" in agent_name else "cons_memory" if "Cons" in agent_name else ""
    return os.path.join(BASE_MEMORY_DIR, sub_dir, filename)

async def write_json_direct(filename: str, content: Any, agent_name: str) -> None:
    """Directly writes/appends to JSON file."""
    file_path = get_memory_path(agent_name, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try: data = json.load(f)
            except: data = []
    
    data.append({"agent": agent_name, "content": content})
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

async def read_json_direct(filename: str, agent_name: str) -> Any:
    file_path = get_memory_path(agent_name, filename)
    if not os.path.exists(file_path): return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Note: The original ADK tool wrappers (FunctionTool) are removed for LangGraph.
# Node implementations directly use write_json_direct and read_json_direct.
