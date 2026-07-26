"""
Grok Local Agent Kit
--------------------
Open-source toolkit for local AI agents powered by Ollama + tools + MCP.
"""

__version__ = "0.4.0"

from .agent import Agent, create_agent
from .tools import web_search, execute_python, list_directory

__all__ = [
    "Agent",
    "create_agent",
    "web_search",
    "execute_python",
    "list_directory",
    "__version__",
]
