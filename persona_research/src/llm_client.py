import os
import json
import logging
import time
import uuid
from concordia.contrib.language_models.google import gemini_model
from concordia.language_model import retry_wrapper

logger = logging.getLogger("PersonaResearch.LLM")

class TraceabilityTracker:
    """Wrapper to capture prompts, tokens, and latency for traceability."""
    def __init__(self, model):
        self.model = model
        self.last_trace = {
            "prompt": "N/A",
            "input_tokens": 0,
            "output_tokens": 0,
            "latency": 0.0,
            "request_id": "N/A"
        }

    def sample_text(self, prompt, **kwargs):
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Access the underlying GeminiModel to get usage data
        # Note: GeminiModel uses google-genai which returns usage in response
        # However, Concordia's sample_text abstracts this away. 
        # We'll use the model's internal client if possible or estimate.
        
        response_text = self.model.sample_text(prompt, **kwargs)
        latency = time.time() - start_time
        
        # In this specific Concordia contrib model, we don't have direct access 
        # to the raw response object via sample_text. 
        # We will log the request and estimate tokens (or use a dedicated counter if available)
        
        self.last_trace = {
            "prompt": prompt,
            "input_tokens": len(prompt) // 4, # Heuristic for Gemini
            "output_tokens": len(response_text) // 4,
            "latency": latency,
            "request_id": request_id
        }
        return response_text
    
    def __getattr__(self, name):
        return getattr(self.model, name)

class LLMClient:
    def __init__(self, model_name="gemini-3.1-flash-lite-preview", api_key=None):
        if "/" in model_name:
            self.model_name = model_name.split("/")[-1]
        else:
            self.model_name = model_name
            
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or arguments.")

        # Concordia native Gemini wrapper
        base_model = gemini_model.GeminiModel(
            model_name=self.model_name,
            api_key=self.api_key
        )
        
        # Add retries
        retrying_model = retry_wrapper.RetryLanguageModel(
            base_model,
            retry_tries=5,
            retry_delay=5.0,
            exponential_backoff=True
        )
        
        # Wrap for traceability
        self.tracker = TraceabilityTracker(retrying_model)

    def meta_call(self, prompt):
        """Direct JSON-based meta-cognition call with traceability."""
        try:
            json_prompt = f"{prompt}\n\nIMPORTANT: Return ONLY a raw JSON object. Do not include markdown code blocks."
            response_text = self.tracker.sample_text(
                json_prompt,
                max_tokens=1024,
                temperature=0.0
            )
            
            trace = self.tracker.last_trace
            
            clean_json = response_text.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0].strip()

            return json.loads(clean_json), trace
        except Exception as e:
            logger.error(f"Gemini Meta-Call Failed: {e}")
            return {"action": "keep", "role": "Strategic Expert", "backstory": "A resilient analyst.", "rationale": "Error."}, self.tracker.last_trace

    def get_concordia_model(self):
        """Returns the traceable Concordia-compatible model."""
        return self.tracker
