import ollama

class LocalAgent:
    def __init__(self, model='llama3.2'):
        self.model = model

    def run(self, prompt):
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']

# Basic MCP support stub
class MCPConnector:
    pass

print('LocalAgent ready for Ollama!')