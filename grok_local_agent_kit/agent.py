import ollama
from typing import List, Dict, Any
import json

class Agent:
    def __init__(self, model='llama3.2'):
        self.model = model
        self.history = []
    def chat(self, prompt):
        self.history.append({'role': 'user', 'content': prompt})
        response = ollama.chat(model=self.model, messages=self.history)
        content = response['message']['content']
        self.history.append({'role': 'assistant', 'content': content})
        return content

def create_agent():
    return Agent()