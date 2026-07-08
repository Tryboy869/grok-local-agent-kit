import ollama
from typing import List, Dict, Any, Callable
import json

class Tool:
    def __init__(self, name: str, func: Callable, description: str, parameters: Dict):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = parameters

class Agent:
    def __init__(self, model: str = "llama3.2", provider: str = "ollama"):
        self.model = model
        self.provider = provider
        self.history = []
        self.tools = []
        self._register_default_tools()
    
    def _register_default_tools(self):
        self.register_tool(
            name="web_search",
            func=self._web_search,
            description="Search the web for information",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        )
        self.register_tool(
            name="file_read",
            func=self._file_read,
            description="Read content from a file",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file"}
                },
                "required": ["file_path"]
            }
        )
    
    def register_tool(self, name: str, func: Callable, description: str, parameters: Dict):
        tool = Tool(name, func, description, parameters)
        self.tools.append(tool)
    
    def _web_search(self, query: str) -> str:
        try:
            return f"[Web search placeholder for '{query}'] - To enable real search: pip install duckduckgo-search"
        except:
            return f"Web search for {query}"
    
    def _file_read(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()[:4000]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _get_ollama_tools(self):
        return [
            {
                'type': 'function',
                'function': {
                    'name': tool.name,
                    'description': tool.description,
                    'parameters': tool.parameters
                }
            } for tool in self.tools
        ]
    
    def chat(self, prompt: str) -> str:
        self.history.append({'role': 'user', 'content': prompt})
        messages = self.history.copy()
        try:
            if self.provider == 'ollama':
                tools = self._get_ollama_tools()
                response = ollama.chat(model=self.model, messages=messages, tools=tools)
                if response.message.tool_calls:
                    for tc in response.message.tool_calls:
                        tool_name = tc.function.name
                        args = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments
                        for tool in self.tools:
                            if tool.name == tool_name:
                                result = tool.func(**args)
                                self.history.append({'role': 'tool', 'content': str(result)})
                                # Re-call for final response
                                response = ollama.chat(model=self.model, messages=self.history, tools=tools)
                                break
                content = response.message.content
                self.history.append({'role': 'assistant', 'content': content})
                return content
            else:
                return f'[{self.provider}] {prompt[:100]}...'
        except Exception as e:
            err = f'Error: {str(e)}. Run ollama serve and ollama pull {self.model}'
            self.history.append({'role': 'assistant', 'content': err})
            return err

def create_agent(model: str = "llama3.2", provider: str = "ollama"):
    return Agent(model, provider)