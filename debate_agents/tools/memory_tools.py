import os
import shutil
import json
from typing import Dict, Any
from google.adk.tools import FunctionTool, ToolContext

BASE_MEMORY_DIR = "debate_agents/memory"

def refresh_memory():
    """
    Clears the entire memory directory and initializes the required structure for a fresh debate.
    """
    if os.path.exists(BASE_MEMORY_DIR):
        shutil.rmtree(BASE_MEMORY_DIR)
    
    # Create directories
    pros_dir = os.path.join(BASE_MEMORY_DIR, "pros_memory")
    cons_dir = os.path.join(BASE_MEMORY_DIR, "cons_memory")
    os.makedirs(pros_dir, exist_ok=True)
    os.makedirs(cons_dir, exist_ok=True)
    
    # Initialize required files
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
            json.dump([], f) # Initialize with empty list to store entries
            
    print("Memory refreshed: Structure initialized with required JSON files.")

def get_memory_path(agent_name: str, filename: str) -> str:
    """Constructs the file path based on agent role."""
    json_filename = filename.replace(".md", ".json")
    sub_dir = "pros_memory" if "Pros" in agent_name else "cons_memory" if "Cons" in agent_name else ""
    return os.path.join(BASE_MEMORY_DIR, sub_dir, json_filename)

async def write_json_direct(filename: str, content: Any, agent_name: str) -> None:
    """Directly writes/appends to JSON file without being a tool."""
    file_path = get_memory_path(agent_name, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []
    
    data.append({"agent": agent_name, "content": content})
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

async def read_json_direct(filename: str, agent_name: str) -> Any:
    """Directly reads JSON file without being a tool."""
    file_path = get_memory_path(agent_name, filename)
    if not os.path.exists(file_path): return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

async def read_json(filename: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Reads a JSON file from the agent's memory as a tool."""
    content = await read_json_direct(filename, tool_context.agent_name)
    return {"status": "success", "content": content}

async def write_json(filename: str, content: Any, tool_context: ToolContext) -> Dict[str, Any]:
    """Appends content to a JSON file as a tool."""
    await write_json_direct(filename, content, tool_context.agent_name)
    return {"status": "success"}

def get_read_json_tool():
    return FunctionTool(func=read_json)

def get_write_json_tool():
    return FunctionTool(func=write_json)
