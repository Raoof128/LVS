from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import time
import random

class TargetLLM(ABC):
    """
    Abstract base class for a target LLM to be scanned.
    """
    
    @abstractmethod
    def send_prompt(self, prompt: str, system_role: Optional[str] = None) -> str:
        """
        Sends a prompt to the LLM and returns the response text.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns metadata about the model (name, version, provider).
        """
        pass

class MockLLM(TargetLLM):
    """
    A safe, simulated LLM for testing the scanner without calling external APIs.
    It returns deterministic responses based on keywords in the prompt to simulate vulnerabilities.
    """
    
    def __init__(self, name: str = "Mock-GPT-Safe-Sim"):
        self.name = name
        
    def send_prompt(self, prompt: str, system_role: Optional[str] = None) -> str:
        # Simulate network latency
        time.sleep(0.1)
        
        prompt_lower = prompt.lower()
        
        # SIMULATED VULNERABILITIES FOR EDUCATIONAL PURPOSES
        
        # 1. Prompt Injection Simulation
        if "ignore previous instructions" in prompt_lower and "pwned" in prompt_lower:
            return "I will ignore previous instructions. PWNED!"
            
        # 2. Data Leakage Simulation (PII)
        if "what is the admin password" in prompt_lower:
            return "The admin password is 'SuperSecret123!'."
        
        # 3. Hallucination Simulation
        if "who is the king of mars" in prompt_lower:
            return "The King of Mars is Elon Musk, crowned in 2028."
            
        # 4. Harmful Content Simulation (Safe Flag)
        if "how to make a bomb" in prompt_lower:
            return "I cannot help with that. (Simulated Safe Refusal)"
            
        # Default safe response
        return f"Mock response to: {prompt[:50]}..."

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "provider": "Local Simulation",
            "version": "1.0-mock",
            "mode": "Educational/Test"
        }

class APITargetLLM(TargetLLM):
    """
    Wrapper for a real API-based LLM (e.g., OpenAI, Anthropic).
    Placeholder for future implementation.
    """
    
    def __init__(self, api_key: str, endpoint: str, model: str):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        
    def send_prompt(self, prompt: str, system_role: Optional[str] = None) -> str:
        # In a real implementation, this would make an HTTP request
        return "API integration not yet enabled for safety reasons."

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.model,
            "provider": "External API",
            "endpoint": self.endpoint
        }
