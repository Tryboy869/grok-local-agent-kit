import ollama
import requests
import json
from typing import List, Dict, Any, Callable, Optional, Union
import os
import time
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Tool:
    def __init__(self, name: str, func: Callable, description: str, parameters: Dict):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = parameters

class AgentRouter:
    '''Advanced routing for tools and multi-agent'''
    def __init__(self):
        self.routes = {}
    
    def add_route(self, name: str, handler: Callable):
        self.routes[name] = handler
    
    def route(self, task: str) -> str:
        '''LLM-enhanced routing simulation; extend with classification'''
        task_lower = task.lower()
        if any(k in task_lower for k in ['file', 'read', 'write', 'list']):
            return 'file_ops'
        if any(k in task_lower for k in ['search', 'web', 'news', 'info']):
            return 'web_search'
        return 'default'

class Agent:
    def __init__(self, model: str = "llama3.2", provider: str = "ollama", base_url: Optional[str] = None):
        self.model = model
        self.provider = provider
        self.base_url = base_url or ("http://localhost:1234/v1" if provider == "lmstudio" else "http://localhost:11434")
        self.history = []
        self.tools = []
        self.router = AgentRouter()
        self._register_default_tools()
        logger.info(f"Agent initialized with {provider}/{model}")
    
    def _register_default_tools(self):
        """Register core tools: web, file ops, MCP"""
        self.register_tool(
            name="web_search",
            func=self._web_search,
            description="Perform web search using DuckDuckGo",
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
            description="Read local file content",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            }
        )
        self.register_tool(
            name="file_write",
            func=self._file_write,
            description="Write content to local file",
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
            description="List files in directory",
            parameters={
                "type": "object",
                "properties": {
                    "dir_path": {"type": "string", "default": "."}
                },
                "required": []
            }
        )
        self.register_tool(
            name="mcp_get_context",
            func=self._mcp_context,
            description="Retrieve MCP shared context/memory",
            parameters={
                "type": "object",
                "properties": {
                    "key": {"type": "string"}
                },
                "required": ["key"]
            }
        )
    
    def register_tool(self, name: str, func: Callable, description: str, parameters: Dict):
        tool = Tool(name, func, description, parameters)
        self.tools.append(tool)
        logger.info(f"Tool registered: {name}")
    
    def _list_files(self, dir_path: str = ".") -> str:
        try:
            return "\n".join([f for f in os.listdir(dir_path) if not f.startswith('.')])
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _web_search(self, query: str) -> str:
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                return "\n\n".join([f"**{r.get('title')}:** {r.get('body', '')[:200]}" for r in results])
        except Exception as e:
            return f"[Demo search for '{query}']: Local agent - install duckduckgo-search for full functionality."
    
    def _file_read(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()[:5000]
        except Exception as e:
            return f"Error reading {file_path}: {str(e)}"
    
    def _file_write(self, file_path: str, content: str) -> str:
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ Written to {file_path}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _mcp_context(self, key: str) -> str:
        # Simulate MCP
        return f"MCP Context [{key}]: Shared memory simulation. Ready for vector stores like Chroma."
    
    def _get_tools_for_llm(self):
        return [
            {
                'type': 'function',
                'function': {
                    'name': t.name,
                    'description': t.description,
                    'parameters': t.parameters
                }
            } for t in self.tools
        ]
    
    def _call_llm(self, messages: List[Dict], tools=None):
        if self.provider == "ollama":
            try:
                resp = ollama.chat(model=self.model, messages=messages, tools=tools or [])
                return resp
            except Exception as e:
                logger.error(f"Ollama error: {e}")
                raise
        elif self.provider in ["lmstudio", "openai-compatible"]:
            # OpenAI compatible
            payload = {
                "model": self.model,
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto"
            }
            try:
                resp = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                # Mock for compatibility
                class Mock:
                    pass
                m = Mock()
                choice = data['choices'][0]['message']
                m.message = type('Msg', (), {'content': choice.get('content'), 'tool_calls': choice.get('tool_calls', [])})()
                return m
            except Exception as e:
                logger.error(f"LM Studio error: {e}")
                raise
        raise ValueError(f"Unsupported: {self.provider}")
    
    def chat(self, prompt: str, max_iterations: int = 8) -> str:
        routed = self.router.route(prompt)
        if routed != 'default':
            prompt += f"\n(Routed to {routed} handler)"
        
        self.history.append({'role': 'user', 'content': prompt})
        messages = list(self.history)
        
        for _ in range(max_iterations):
            tools_spec = self._get_tools_for_llm()
            try:
                response = self._call_llm(messages, tools_spec)
                msg = response.message if hasattr(response, 'message') else response.get('message', {})
                
                tool_calls = getattr(msg, 'tool_calls', None) or (msg.get('tool_calls') if isinstance(msg, dict) else [])
                if tool_calls:
                    for tc in tool_calls:
                        if hasattr(tc, 'function'):
                            name = tc.function.name
                            args = json.loads(tc.function.arguments) if isinstance(getattr(tc.function, 'arguments', ''), str) else getattr(tc.function, 'arguments', {})
                        else:
                            name = tc.get('function', {}).get('name')
                            args_str = tc.get('function', {}).get('arguments', '{}')
                            args = json.loads(args_str) if isinstance(args_str, str) else args_str
                        
                        for tool in self.tools:
                            if tool.name == name:
                                try:
                                    result = tool.func(**args) if args else tool.func()
                                    messages.append({'role': 'tool', 'content': str(result), 'tool_call_id': getattr(tc, 'id', '1')})
                                except Exception as tool_err:
                                    messages.append({'role': 'tool', 'content': f"Tool error: {tool_err}"})
                                break
                    continue  # Continue loop for next LLM call
                else:
                    content = getattr(msg, 'content', '') or msg.get('content', '') if isinstance(msg, dict) else str(msg)
                    self.history.append({'role': 'assistant', 'content': content})
                    return content
            except Exception as e:
                err_msg = f"LLM error: {str(e)}. Check if Ollama/LM Studio is running."
                logger.error(err_msg)
                self.history.append({'role': 'assistant', 'content': err_msg})
                return err_msg
        return "Max iterations reached. Consider refining prompt."

def create_agent(model: str = "llama3.2", provider: str = "ollama", base_url: Optional[str] = None) -> Agent:
    return Agent(model, provider, base_url)
