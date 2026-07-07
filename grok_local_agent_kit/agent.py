from typing import List, Dict

class Agent:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.history = []
    
    def chat(self, prompt: str) -> str:
        # Placeholder for Ollama integration
        self.history.append({"role": "user", "content": prompt})
        response = f"[Agent response with {self.model}]: {prompt[:100]}..."
        self.history.append({"role": "assistant", "content": response})
        return response

# More advanced agent logic coming soon