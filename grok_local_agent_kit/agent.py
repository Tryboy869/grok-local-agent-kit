import ollama

class LocalAgent:
    def __init__(self, model='llama3'):
        self.model = model

    def run(self, prompt: str) -> str:
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']

    def mcp_support(self):
        return 'MCP (Multi-Context Protocol) integration ready for local agents.'

if __name__ == '__main__':
    agent = LocalAgent()
    print(agent.run('Hello from local agent!'))
