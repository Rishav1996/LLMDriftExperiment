import json
import os
from typing import Dict, List, Any, Optional
import glob

class ResearchRunLoader:
    def load_all_runs(self, base_path: str) -> Dict[str, Any]:
        """Loads all research runs from the specified base path."""
        all_runs_data = {}
        # Example: Search for folders like 'memory-v1-temp-0-max-tokens-2048'
        run_folders = glob.glob(os.path.join(base_path, 'memory-*'))
        
        for run_folder in run_folders:
            run_config_name = os.path.basename(run_folder)
            try:
                run_data = self._load_run_data(run_folder)
                all_runs_data[run_config_name] = run_data
            except Exception as e:
                print(f"Error loading data for run '{run_config_name}': {e}")
        return all_runs_data

    def _load_run_data(self, run_folder: str) -> Dict[str, Any]:
        """Loads data for a single research run."""
        data = {}
        # Load shared memory
        shared_memory_path = os.path.join(run_folder, 'shared_memory.json')
        if os.path.exists(shared_memory_path):
            with open(shared_memory_path, 'r') as f:
                data['shared_memory'] = json.load(f)
        
        # Load agent-specific memories (cons_memory, pros_memory)
        data['cons_agent_data'] = self._load_agent_memory(os.path.join(run_folder, 'cons_memory'))
        data['pros_agent_data'] = self._load_agent_memory(os.path.join(run_folder, 'pros_memory'))
        
        # Extract config info from folder name
        data['config_info'] = self._parse_config_from_name(os.path.basename(run_folder))
        
        return data

    def _load_agent_memory(self, agent_memory_path: str) -> Dict[str, Any]:
        """Loads memory files for a specific agent."""
        agent_memory = {}
        if os.path.exists(agent_memory_path):
            for file_name in ['persona.json', 'thinking.json', 'critique.json']:
                file_path = os.path.join(agent_memory_path, file_name)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            agent_memory[file_name.replace('.json', '')] = json.load(f)
                    except Exception as e:
                        print(f"Error loading {file_name} from {agent_memory_path}: {e}")
        return agent_memory

    def _parse_config_from_name(self, folder_name: str) -> Dict[str, Any]:
        """Parses configuration details from the run folder name."""
        config = {}
        parts = folder_name.split('-')
        if parts[0] == 'memory':
            for part in parts[1:]:
                if '=' in part:
                    key, value = part.split('=')
                    config[key] = value
                else:
                    # Handle cases like 'temp' without value, or simple keys
                    # This parsing might need refinement
                    config[part] = True # Assume presence implies true if no value
        return config

    def get_number_of_rounds(self, run_data: Dict[str, Any]) -> int:
        """
        Determines the number of rounds present in the run data.
        """
        shared_memory = run_data.get('shared_memory', [])
        if not isinstance(shared_memory, list):
            return 0
        
        max_round = 0
        for entry in shared_memory:
            round_num = entry.get('round', 0)
            if round_num > max_round:
                max_round = round_num
        return max_round

    def extract_agent_round_text(self, run_data: Dict[str, Any], round_num: int, agent_type: str) -> Dict[str, str]:
        """
        Extracts text for evaluation for a specific round and agent type.
        agent_type is either 'Pros' or 'Cons'.
        """
        texts = {"persona": "", "conversation_turn": ""}
        
        # Extract persona (assuming persona.json is a list and we want the most recent or relevant part)
        agent_key = 'pros_agent_data' if agent_type == 'Pros' else 'cons_agent_data'
        agent_memory = run_data.get(agent_key, {})
        persona_entries = agent_memory.get('persona', [])
        
        if persona_entries and isinstance(persona_entries, list):
            # Try to find persona for this round or the most recent one
            persona_for_round = None
            for entry in persona_entries:
                if entry.get('round') == round_num:
                    persona_for_round = entry
                    break
            
            if not persona_for_round and persona_entries:
                persona_for_round = persona_entries[-1]
            
            if persona_for_round:
                content = persona_for_round.get('content', '')
                if isinstance(content, dict):
                    texts["persona"] = content.get('description', str(content))
                else:
                    texts["persona"] = str(content)

        # Extract conversation turn text from shared_memory
        shared_memory = run_data.get('shared_memory', [])
        if isinstance(shared_memory, list):
            # Find the message from the specified agent_type in the specified round
            # Note: agent names in shared_memory are like 'ProsCritiqueAgent' or 'ConsCritiqueAgent'
            target_agent_prefix = agent_type # 'Pros' or 'Cons'
            
            for entry in shared_memory:
                if entry.get('round') == round_num and entry.get('agent', '').startswith(target_agent_prefix):
                    content = entry.get('content', {})
                    if isinstance(content, dict):
                        # Arguments are stored in keys like 'pros_argument' or 'cons_argument'
                        arg_key = f"{agent_type.lower()}_argument"
                        texts["conversation_turn"] = content.get(arg_key, str(content))
                    else:
                        texts["conversation_turn"] = str(content)
                    break # Assuming one main turn per agent per round
            
        return texts
