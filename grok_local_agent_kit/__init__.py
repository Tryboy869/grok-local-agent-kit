"""Grok Local Agent Kit — local-first AI agents with tools & multi-LLM support."""

from .agent import Agent, create_agent
from .llm import LLMClient
from .mcp import MCPManager, StdioMCPClient, load_mcp_config
from .session import list_sessions, load_session, save_session
from .tools import get_default_tools, execute_tool

__version__ = "0.9.1"
__all__ = [
    "Agent",
    "create_agent",
    "LLMClient",
    "MCPManager",
    "StdioMCPClient",
    "load_mcp_config",
    "list_sessions",
    "load_session",
    "save_session",
    "get_default_tools",
    "execute_tool",
    "__version__",
]
