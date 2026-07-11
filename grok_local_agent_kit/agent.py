import ollama
import requests
import json
from typing import List, Dict, Any, Callable, Optional
import os

class Tool:
    def __init__(self, name: str, func: Callable, description: str, parameters: Dict):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = parameters

class Agent:
    def __init__(self, model: str = "llama3.2", provider: str = "ollama", base_url: Optional[str] = None):
        self.model = model
        self.provider = provider
        self.base_url = base_url or ("http://localhost:1234/v1" if provider == "lmstudio" else None)
        self.history = []
        self.tools = []
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register core tools"""
        self.register_tool(
            name="web_search",
            func=self._web_search,
            description="Search the web using DuckDuckGo or similar",
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
            description="Read content from a local file",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file"}
                },
                "required": ["file_path"]
            }
        )
        self.register_tool(
            name="file_write",
            func=self._file_write,
            description="Write content to a local file",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["file_path", "content"]
            }
        )
        # MCP placeholder - can be extended
        self.register_tool(
            name="mcp_context",
            func=self._mcp_context,
            description="Get MCP context or memory",
            parameters={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Context key"}
                },
                "required": ["key"]
            }
        )
    
    def register_tool(self, name: str, func: Callable, description: str, parameters: Dict):
        tool = Tool(name, func, description, parameters)
        self.tools.append(tool)
    
    def _web_search(self, query: str) -> str:
        """Real web search if duckduckgo-search installed, else placeholder"""
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=3)]
                return "\n".join([f"{r['title']}: {r['body'][:200]}" for r in results])
        except ImportError:
            return f"[Web search for '{query}'] Install 'duckduckgo-search' for real results: pip install duckduckgo-search"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def _file_read(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()[:8000]  # Limit for context
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def _file_write(self, file_path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def _mcp_context(self, key: str) -> str:
        """Placeholder for MCP"""
        return f"MCP context for {key}: Local agent memory simulation active."
    
    def _get_tools_for_provider(self):
        if self.provider == "ollama":
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
        else:
            # OpenAI compatible for LM Studio etc.
            return [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters
                    }
                } for tool in self.tools
            ]
    
    def _call_llm(self, messages: List[Dict], tools=None):
        if self.provider == "ollama":
            response = ollama.chat(model=self.model, messages=messages, tools=tools or [])
            return response
        elif self.provider == "lmstudio" or self.base_url:
            # OpenAI compatible API
            payload = {
                "model": self.model,
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto" if tools else None
            }
            try:
                resp = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                # Simulate ollama response format
                class MockResponse:
                    pass
                mock = MockResponse()
                mock.message = type('obj', (object,), {'content': data['choices'][0]['message']['content'], 'tool_calls': data['choices'][0]['message'].get('tool_calls', [])})()
                return mock
            except Exception as e:
                raise Exception(f"LM Studio error: {e}")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def chat(self, prompt: str, max_iterations: int = 5) -> str:
        self.history.append({'role': 'user', 'content': prompt})
        messages = self.history.copy()
        
        for iteration in range(max_iterations):
            try:
                tools = self._get_tools_for_provider()
                response = self._call_llm(messages, tools)
                
                msg = response.message if hasattr(response, 'message') else response['message'] if isinstance(response, dict) else response
                
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_name = tc.function.name
                        args = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments
                        for tool in self.tools:
                            if tool.name == tool_name:
                                result = tool.func(**args)
                                messages.append({'role': 'tool', 'content': str(result), 'tool_call_id': getattr(tc, 'id', '1')})
                                break
                    continue  # Loop for tool results
                else:
                    content = msg.content
                    self.history.append({'role': 'assistant', 'content': content})
                    return content
            except Exception as e:
                err = f'Error: {str(e)}. Ensure Ollama/LM Studio running and model pulled.'
                self.history.append({'role': 'assistant', 'content': err})
                return err
        return "Max iterations reached."

def create_agent(model: str = "llama3.2", provider: str = "ollama", base_url: Optional[str] = None):
    """Factory for agents"""
    return Agent(model, provider, base_url)