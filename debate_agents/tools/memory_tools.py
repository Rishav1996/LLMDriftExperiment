import os
import shutil
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
        os.path.join(BASE_MEMORY_DIR, "shared_memory.md"),
        os.path.join(pros_dir, "persona.md"),
        os.path.join(pros_dir, "thinking.md"),
        os.path.join(pros_dir, "critique.md"),
        os.path.join(cons_dir, "persona.md"),
        os.path.join(cons_dir, "thinking.md"),
        os.path.join(cons_dir, "critique.md"),
    ]
    
    for file_path in files_to_init:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("") # Initialize with empty content
            
    print("Memory refreshed: Structure initialized with required markdown files.")

def get_memory_path(agent_name: str, filename: str) -> str:
    """
    Constructs the file path based on agent role.
    """
    if "Pros" in agent_name: # Broadened match
        sub_dir = "pros_memory"
    elif "Cons" in agent_name: # Broadened match
        sub_dir = "cons_memory"
    else:
        # Default for shared or other agents
        sub_dir = ""

    if filename == "shared_memory.md":
        path = os.path.join(BASE_MEMORY_DIR, "shared_memory.md")
    else:
        path = os.path.join(BASE_MEMORY_DIR, sub_dir, filename)
    
    return path

async def write_markdown(
    filename: str,
    content: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Writes content to a markdown file in the agent's private or shared memory.
    
    Args:
        filename: The name of the file (e.g., 'thinking.md', 'persona.md', 'critique.md', or 'shared_memory.md').
        content: The text content to write or append.
    """
    agent_name = tool_context.agent_name
    file_path = get_memory_path(agent_name, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    mode = 'a' if filename == "shared_memory.md" else 'w'
    
    with open(file_path, mode, encoding='utf-8') as f:
        if mode == 'a':
            # Use a slightly different header for the topic initialization vs arguments
            if "TopicExtractAgent" in agent_name:
                f.write(f"# Debate Topic: {content}\n\n")
            else:
                f.write(f"\n\n### Entry by {agent_name}\n{content}")
        else:
            f.write(content)
            
    return {"status": "success", "path": file_path}

async def read_markdown(
    filename: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Reads content from a markdown file in the agent's private or shared memory.
    
    Args:
        filename: The name of the file to read.
    """
    agent_name = tool_context.agent_name
    file_path = get_memory_path(agent_name, filename)
    
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File {filename} not found in memory."}
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    return {"status": "success", "content": content}

def get_read_markdown_tool():
    return FunctionTool(func=read_markdown)

def get_write_markdown_tool():
    return FunctionTool(func=write_markdown)
