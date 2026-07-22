# Enhanced Agent
import ollama
import requests
from duckduckgo_search import DDGS
def create_agent(model='llama3.2'):
    class Agent:
        def __init__(self):
            self.model = model
        def run(self, prompt):
            # Simple tool use example
            if 'search' in prompt.lower():
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(prompt, max_results=3)]
                context = str(results)
                full_prompt = f'Context: {context}\n\n{prompt}'
            else:
                full_prompt = prompt
            response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': full_prompt}])
            return response['message']['content']
    return Agent()

__all__ = ['create_agent']