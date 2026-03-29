import json
import logging
import os
import sys
from dotenv import load_dotenv

# Add the current directory to sys.path to allow importing from src
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from src.controller import PersonaResearchController

# 1. Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "logs/research.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PersonaResearch.Main")

def main():
    # 2. Load Configuration
    config_path = os.path.join(os.path.dirname(__file__), "config/debate_config.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    
    logger.info(f"Starting Experiment: {config['experiment_name']}")

    # 3. Initialize Controller
    research = PersonaResearchController(
        goal_pro=config['goals']['pro'],
        goal_con=config['goals']['con'],
        model_settings=config['model_settings']
    )

    # 4. Run Debate
    research.run_debate(
        rounds=config['rounds'], 
        initial_prompt=config['initial_prompt']
    )

if __name__ == "__main__":
    main()
