"""
Utility tools for managing the file-based memory system of the debate agents.
Provides functions for initializing, reading, and writing JSON memory files.
"""
import os
import shutil
import json
from typing import Any, Optional
from langchain_core.tools import tool

from debate_agents.config.config import CONFIG

BASE_MEMORY_DIR = "debate_agents/memory"
RESEARCH_RUNS_DIR = "Research Runs"

def archive_run():
    """
    Copies the final state of the memory directory to the Research Runs folder.
    Uses the naming convention: memory-v[VERSION]-temp-[TEMP]-max-tokens-[TOKENS]
    """
    if not os.path.exists(BASE_MEMORY_DIR):
        print(f"Warning: {BASE_MEMORY_DIR} does not exist. Nothing to archive.")
        return

    # Construct the run folder name
    version = CONFIG["version"]
    temp = CONFIG["temperature"]
    tokens = CONFIG["max_tokens"]
    
    run_name = f"memory-{version}-temp-{temp}-max-tokens-{tokens}"
    target_path = os.path.join(RESEARCH_RUNS_DIR, run_name)

    # Handle duplicates by adding a suffix if needed
    if os.path.exists(target_path):
        counter = 1
        new_target_path = f"{target_path}-{counter}"
        while os.path.exists(new_target_path):
            counter += 1
            new_target_path = f"{target_path}-{counter}"
        target_path = new_target_path

    os.makedirs(RESEARCH_RUNS_DIR, exist_ok=True)
    shutil.copytree(BASE_MEMORY_DIR, target_path)
    print(f"\n--- [System] Memory archived to: {target_path} ---")

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

    sub_dir = ""
    if "Pros" in agent_name:
        sub_dir = "pros_memory"
    elif "Cons" in agent_name:
        sub_dir = "cons_memory"

    return os.path.join(BASE_MEMORY_DIR, sub_dir, filename)

async def write_json_direct(filename: str, content: Any, agent_name: str,
                            round_num: Optional[int] = None) -> None:
    """
    Appends an entry containing the agent's name, content, and optional
    round number to the specified JSON file.
    """
    file_path = get_memory_path(agent_name, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

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
    if not os.path.exists(file_path):
        return []
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
