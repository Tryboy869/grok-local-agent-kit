"""Grok Local Agent Kit — local-first AI agents with tools & multi-LLM support."""

from .agent import Agent, create_agent
from .llm import LLMClient
from .tools import get_default_tools, execute_tool

__version__ = "0.7.4"
__all__ = [
    "Agent",
    "create_agent",
    "LLMClient",
    "get_default_tools",
    "execute_tool",
    "__version__",
]
