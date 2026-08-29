"""Grok Local Agent Kit — local-first AI agents with tools & multi-LLM support."""

from .agent import Agent, create_agent
from .llm import LLMClient
from .mcp import MCPManager, StdioMCPClient, load_mcp_config
from .memory import forget, recall, remember
from .orchestrator import Orchestrator
from .router import MultiLLMRouter, format_probe
from .session import list_sessions, load_session, save_session
from .tools import execute_tool, get_default_tools

__version__ = "0.10.0"
__all__ = [
    "Agent",
    "create_agent",
    "LLMClient",
    "MCPManager",
    "StdioMCPClient",
    "load_mcp_config",
    "MultiLLMRouter",
    "Orchestrator",
    "list_sessions",
    "load_session",
    "save_session",
    "remember",
    "recall",
    "forget",
    "format_probe",
    "get_default_tools",
    "execute_tool",
    "__version__",
]
