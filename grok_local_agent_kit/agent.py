# Core Agent with Ollama and tool calling
import ollama
from typing import List, Callable, Dict, Any
from .tools import web_search, execute_code

class Agent:
    def __init__(self, model: str = 'llama3.2'):
        self.model = model
        self.tools = {'web_search': web_search, 'execute_code': execute_code}

    def run(self, prompt: str) -> str:
        messages = [{'role': 'user', 'content': prompt}]
        # Simple ReAct simulation
        response = ollama.chat(model=self.model, messages=messages)
        return response['message']['content']

def create_agent(model='llama3.2'):
    return Agent(model)

__all__ = ['Agent', 'create_agent']