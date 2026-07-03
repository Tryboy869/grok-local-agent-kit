import ollama
from typing import List, Dict

class LocalAgent:
    def __init__(self, model: str = 'llama3.2'):
        self.model = model

    def run(self, task: str, tools: List = None) -> str:
        # Basic agent loop simulation
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': task}])
        return response['message']['content']

print('LocalAgent ready for Ollama/MCP!')