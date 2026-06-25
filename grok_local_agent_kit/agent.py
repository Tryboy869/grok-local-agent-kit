import ollama
from pydantic import BaseModel

class Agent:
    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def run(self, prompt: str) -> str:
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']

if __name__ == "__main__":
    agent = Agent()
    print(agent.run("Hello from local agent!"))
