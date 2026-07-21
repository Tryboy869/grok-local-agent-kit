# Basic agent implementation
import ollama
def create_agent(model='llama3.2'):
    class Agent:
        def run(self, prompt):
            response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
            return response['message']['content']
    return Agent()

__all__ = ['create_agent']