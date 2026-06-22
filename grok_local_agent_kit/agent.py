import ollama

class LocalAgent:
    def __init__(self, model='llama3.1'):
        self.model = model
    def run(self, task):
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': task}])
        return response['message']['content']
