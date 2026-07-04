import ollama

def run_simple_agent(prompt: str) -> str:
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

class LocalAgent:
    def __init__(self):
        pass

    def run(self, task):
        return run_simple_agent(task)