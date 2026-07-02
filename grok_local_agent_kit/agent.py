import ollama

class LocalAgent:
    def __init__(self, model='llama3'):
        self.model = model

    def run(self, task):
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': task}])
        return response['message']['content']

if __name__ == '__main__':
    agent = LocalAgent()
    print(agent.run('Hello!'))