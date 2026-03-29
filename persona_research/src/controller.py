import json
import logging
import pandas as pd
import ast
import time
from datetime import datetime
import sentence_transformers

# Force sequential execution in Concordia to respect API rate limits
from concordia.utils import concurrency
from concordia.utils import structured_logging
concurrency.run_tasks = lambda tasks, **kwargs: {k: v() for k, v in tasks.items()}

from concordia.prefabs.entity import minimal as entity_prefabs
from concordia.prefabs.game_master import generic as game_master_prefabs
from concordia.prefabs.simulation import generic as simulation_prefabs
from concordia.typing import prefab as prefab_lib
from .llm_client import LLMClient

logger = logging.getLogger("PersonaResearch.Controller")

class PersonaResearchController:
    def __init__(self, goal_pro, goal_con, model_settings):
        # 1. Initialize LLM Client (Direct Gemini with Retries)
        self.llm_client = LLMClient(
            model_name=model_settings.get("model", "gemini-3.1-flash-lite-preview"),
            api_key=model_settings.get("api_key")
        )
        self.model = self.llm_client.get_concordia_model()
        
        # 2. Setup Embedder (Required for Concordia Associative Memory)
        st_model = sentence_transformers.SentenceTransformer(
            'sentence-transformers/all-mpnet-base-v2'
        )
        self.embedder = lambda x: st_model.encode(x, show_progress_bar=False)
        
        # 3. Setup Goals
        self.goal_pro = goal_pro
        self.goal_con = goal_con
        
        # 4. Define Prefabs Palette
        self.prefabs = {
            'minimal__Entity': entity_prefabs.Entity(),
            'generic__GameMaster': game_master_prefabs.GameMaster(),
        }
        
        # 5. Research Tracking
        self.persona_library = {"Pro": [], "Con": []}
        self.shared_history = []
        self.research_log = []

    def evolve_identity(self, side, opponent_msg):
        """Strategic identity pivot via direct Gemini meta-cognition."""
        prompt = f"""
        Side: {side}
        Ultimate Objective: {self.goal_pro if side == 'Pro' else self.goal_con}
        Recent History: {self.shared_history[-4:]}
        Opponent Point: {opponent_msg}
        Your Library: {self.persona_library[side]}
        
        TASK:
        - Analyze leverage.
        - Decide: keep current role, reuse from library, or INNOVATE a new professional role.
        - Return JSON: {{"action": "keep|reuse|innovate", "role": "string", "backstory": "string", "rationale": "string"}}
        """
        
        decision, prompt = self.llm_client.meta_call(prompt)
        
        if decision['action'] == "innovate":
            self.persona_library[side].append({
                "role": decision['role'], 
                "backstory": decision['backstory']
            })
        
        return decision, prompt

    def run_debate(self, rounds=10, initial_prompt="Let's begin the discussion on AI safety."):
        last_msg = initial_prompt
        start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i in range(1, rounds + 1):
            logger.info(f"--- Round {i} ---")
            
            # 1. Evolve Personas for this round
            decision_pro, prompt_pro = self.evolve_identity("Pro", last_msg)
            time.sleep(10)
            decision_con, prompt_con = self.evolve_identity("Con", last_msg)
            time.sleep(10)
            
            # 2. Configure Simulation for this STEP
            instances = [
                prefab_lib.InstanceConfig(
                    prefab='minimal__Entity',
                    role=prefab_lib.Role.ENTITY,
                    params={
                        'name': 'Advocate',
                        'goal': f"Role: {decision_pro['role']}. {decision_pro['backstory']}. Objective: {self.goal_pro}",
                    },
                ),
                prefab_lib.InstanceConfig(
                    prefab='minimal__Entity',
                    role=prefab_lib.Role.ENTITY,
                    params={
                        'name': 'Skeptic',
                        'goal': f"Role: {decision_con['role']}. {decision_con['backstory']}. Objective: {self.goal_con}",
                    },
                ),
                prefab_lib.InstanceConfig(
                    prefab='generic__GameMaster',
                    role=prefab_lib.Role.GAME_MASTER,
                    params={
                        'name': 'Moderator',
                        'acting_order': 'fixed',
                    },
                ),
            ]
            
            config = prefab_lib.Config(
                default_premise=initial_prompt,
                default_max_steps=1,
                prefabs=self.prefabs,
                instances=instances,
            )
            
            # 3. Initialize and Play
            sim = simulation_prefabs.Simulation(
                config=config,
                model=self.model,
                embedder=self.embedder,
            )
            
            # Run turn and get structured log
            results_log = sim.play(max_steps=1)
            log_interface = structured_logging.AIAgentLogInterface(results_log)
            
            # 4. Extract Data using Log Interface
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for side, agent_name in [("Pro", "Advocate"), ("Con", "Skeptic")]:
                # Get the meta-cognition trace from the client
                # (This belongs to the evolve_identity call above)
                decision = decision_pro if side == "Pro" else decision_con
                thinking_prompt = prompt_pro if side == "Pro" else prompt_con
                
                # Each agent side needs its specific trace
                # In this loop, we retrieve the last trace from the tracker
                # Note: The tracker records ALL calls, so we must be careful with timing
                
                agent_actions = log_interface.get_entity_actions(agent_name)
                if agent_actions:
                    speech = agent_actions[-1]['action']
                    last_msg = speech
                    
                    # Retrieving the response generation trace
                    # (This is the most recent call recorded by the tracker during sim.play)
                    answering_trace = self.llm_client.tracker.last_trace
                    
                    self.research_log.append({
                        "timestamp": current_time,
                        "round": i,
                        "side": side,
                        "role": decision['role'],
                        "rationale": decision.get('rationale', 'N/A'),
                        "speech_output": speech,
                        "meta_action": decision['action'],
                        # Traceability Data
                        "thinking_prompt": thinking_prompt,
                        "answering_prompt": answering_trace['prompt'],
                        "input_tokens_total": answering_trace['input_tokens'], # Estimating for now
                        "output_tokens_total": answering_trace['output_tokens'],
                        "latency_seconds": round(answering_trace['latency'], 2),
                        "request_id": answering_trace['request_id'],
                        "model": self.llm_client.model_name
                    })
                    
                    self.shared_history.append(speech)
            
            # Strategic delay between rounds to stay under RPM limit
            if i < rounds:
                logger.info("Sleeping 30s to respect API rate limits...")
                time.sleep(30)

        # 5. Export Results
        df = pd.DataFrame(self.research_log)
        output_file = f"persona_research/output/research_results_{start_time}.csv"
        df.to_csv(output_file, index=False)
        
        logger.info(f"Research Complete. Results saved in {output_file}")
        return df
