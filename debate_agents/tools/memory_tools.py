import os
import shutil
import json
from typing import Dict, Any, Optional
from langchain_core.tools import tool

BASE_MEMORY_DIR = "debate_deep_agents/memory"

def refresh_memory():
    """
    Clears the entire memory directory and initializes it with an empty 
    JSON list structure for all required agent files.
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
    """
    if filename == "shared_memory.json":
        return os.path.join(BASE_MEMORY_DIR, filename)
        
    sub_dir = "pros_memory" if "Pros" in agent_name else "cons_memory" if "Cons" in agent_name else ""
    return os.path.join(BASE_MEMORY_DIR, sub_dir, filename)

async def write_json_direct(filename: str, content: Any, agent_name: str, round_num: Optional[int] = None) -> None:
    """
    Appends an entry containing the agent's name, content, and optional 
    round number to the specified JSON file.
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
    """
    file_path = get_memory_path(agent_name, filename)
    if not os.path.exists(file_path): return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_memory_tools(agent_name: str):
    """
    Creates a set of memory tools bound to a specific agent name.
    """
    
    @tool
    async def read_json(filename: str) -> Any:
        """
        Reads the content of a JSON memory file. 
        Use 'shared_memory.json' for common debate state.
        Use 'persona.json', 'thinking.json', or 'critique.json' for agent-specific memory.
        """
        return await read_json_direct(filename, agent_name)

    @tool
    async def write_json(filename: str, content: str) -> str:
        """
        Writes or appends content to a JSON memory file.
        Use 'shared_memory.json' to commit final arguments.
        Use 'persona.json', 'thinking.json', or 'critique.json' for internal agent state.
        The 'content' should be a string or a JSON-encoded object.
        """
        # Try to parse as JSON if it's an object/list, otherwise treat as string
        try:
            parsed_content = json.loads(content)
        except (json.JSONDecodeError, TypeError):
            parsed_content = content
            
        await write_json_direct(filename, parsed_content, agent_name)
        return f"Successfully wrote to {filename}"

    return [read_json, write_json]
