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
    """
    Constructs the file path based on agent role, mapping .md requests to .json.
    """
    # Map old .md requests to .json
    json_filename = filename.replace(".md", ".json")
    
    if "Pros" in agent_name:
        sub_dir = "pros_memory"
    elif "Cons" in agent_name:
        sub_dir = "cons_memory"
    else:
        sub_dir = ""

    if json_filename == "shared_memory.json":
        path = os.path.join(BASE_MEMORY_DIR, "shared_memory.json")
    else:
        path = os.path.join(BASE_MEMORY_DIR, sub_dir, json_filename)
    
    return path

async def write_json(
    filename: str,
    content: Any,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Appends an object to a JSON file (list of entries) in the agent's memory.
    
    Args:
        filename: The name of the file (e.g., 'thinking.json').
        content: The data (dict/object) to append.
    """
    agent_name = tool_context.agent_name
    file_path = get_memory_path(agent_name, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    # Ensure content is dict
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except:
            content = {"message": content}

    entry = {
        "agent": agent_name,
        "content": content
    }
    data.append(entry)
            
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
            
    return {"status": "success", "path": file_path}

async def read_json(
    filename: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Reads a JSON file from the agent's memory.
    """
    agent_name = tool_context.agent_name
    file_path = get_memory_path(agent_name, filename)
    
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File {filename} not found."}
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    return {"status": "success", "content": data}

def get_read_json_tool():
    return FunctionTool(func=read_json)

def get_write_json_tool():
    return FunctionTool(func=write_json)
