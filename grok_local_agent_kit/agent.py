import ollama
import requests
import json
from typing import List, Dict, Any, Callable, Optional, Union
import os
import time
from pathlib import Path

class Tool:
    def __init__(self, name: str, func: Callable, description: str, parameters: Dict):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = parameters

class AgentRouter:
    '''Simple routing for tools and multi-agent coordination'''
    def __init__(self):
        self.routes = {}
    
    def add_route(self, name: str, handler: Callable):
        self.routes[name] = handler
    
    def route(self, task: str) -> str:
        '''Basic keyword-based routing; extend with LLM for better classification'''
        for keyword, handler in self.routes.items():
            if keyword.lower() in task.lower():
                return handler(task)
        return "No specific route matched. Using default agent."

class Agent:
    def __init__(self, model: str = "llama3.2", provider: str = "ollama", base_url: Optional[str] = None):
        self.model = model
        self.provider = provider
        self.base_url = base_url or ("http://localhost:1234/v1" if provider == "lmstudio" else None)
        self.history = []
        self.tools = []
        self.router = AgentRouter()
        self._register_default_tools()
        self._setup_router()
    
    def _setup_router(self):
        self.router.add_route("file", self._handle_file_task)
        self.router.add_route("web", self._handle_web_task)
        self.router.add_route("search", self._handle_web_task)
    
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
        self.register_tool(
            name="list_files",
            func=self._list_files,
            description="List files in a directory",
            parameters={
                "type": "object",
                "properties": {
                    "dir_path": {"type": "string", "description": "Directory path", "default": "."}
                },
                "required": []
            }
        )
        # MCP placeholder
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
    
    def _list_files(self, dir_path: str = ".") -> str:
        try:
            return "\n".join(os.listdir(dir_path))
        except Exception as e:
            return f"Error listing files: {str(e)}"
    
    def _web_search(self, query: str) -> str:
        """Real web search"""
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=5)]
                return "\n".join([f"{r.get('title', '')}: {r.get('body', '')[:300]}" for r in results])
        except ImportError:
            return f"[Simulated search for '{query}'] (pip install duckduckgo-search for real)",
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def _file_read(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()[:10000]
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
        return f"MCP context for {key}: Local memory simulation. Extend with vector DB for RAG."
    
    def _handle_file_task(self, task: str) -> str:
        return f"File task routed: {task[:100]}..."
    
    def _handle_web_task(self, task: str) -> str:
        return self._web_search(task)
    
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
            try:
                response = ollama.chat(model=self.model, messages=messages, tools=tools or [])
                return response
            except Exception as e:
                raise Exception(f"Ollama error: {e}")
        elif self.provider == "lmstudio" or self.base_url:
            payload = {
                "model": self.model,
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto" if tools else None
            }
            try:
                resp = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=90)
                resp.raise_for_status()
                data = resp.json()
                class MockResponse: pass
                mock = MockResponse()
                choice = data.get('choices', [{}])[0].get('message', {})
                mock.message = type('obj', (object,), {'content': choice.get('content'), 'tool_calls': choice.get('tool_calls', [])})()
                return mock
            except Exception as e:
                raise Exception(f"LM Studio/OpenAI compatible error: {e}")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def chat(self, prompt: str, max_iterations: int = 5) -> str:
        """Core chat with tool calling and routing"""
        # Routing
        routed_response = self.router.route(prompt)
        if "No specific route" not in routed_response:
            prompt += f"\n\nRouted insight: {routed_response}"
        
        self.history.append({'role': 'user', 'content': prompt})
        messages = self.history.copy()
        
        for iteration in range(max_iterations):
            try:
                tools = self._get_tools_for_provider()
                response = self._call_llm(messages, tools)
                
                msg = getattr(response, 'message', None) or (response.get('message') if isinstance(response, dict) else response)
                
                tool_calls = getattr(msg, 'tool_calls', None) or msg.get('tool_calls', []) if isinstance(msg, dict) else []
                if tool_calls:
                    for tc in tool_calls:
                        if hasattr(tc, 'function'):
                            tool_name = tc.function.name
                            args_str = tc.function.arguments
                        else:
                            tool_name = tc.get('function', {}).get('name')
                            args_str = tc.get('function', {}).get('arguments', '{}')
                        try:
                            args = json.loads(args_str) if isinstance(args_str, str) else args_str or {}
                        except:
                            args = {}
                        for tool in self.tools:
                            if tool.name == tool_name:
                                result = tool.func(**{k: v for k, v in args.items() if k in [p for p in tool.parameters.get('properties', {})]}) if args else tool.func()
                                tool_id = getattr(tc, 'id', '1') if hasattr(tc, 'id') else tc.get('id', '1')
                                messages.append({'role': 'tool', 'content': str(result), 'tool_call_id': tool_id})
                                break
                    continue
                else:
                    content = getattr(msg, 'content', '') or (msg.get('content', '') if isinstance(msg, dict) else str(msg))
                    self.history.append({'role': 'assistant', 'content': content})
                    return content
            except Exception as e:
                err = f'Error: {str(e)}. Ensure server running (ollama serve or LM Studio).'
                self.history.append({'role': 'assistant', 'content': err})
                return err
        return "Max iterations reached."

def create_agent(model: str = "llama3.2", provider: str = "ollama", base_url: Optional[str] = None):
    """Factory"""
    return Agent(model, provider, base_url)
