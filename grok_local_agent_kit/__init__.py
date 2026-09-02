"""Grok Local Agent Kit — local-first AI agents with tools & multi-LLM support."""

__version__ = "0.14.0"

from .agent import Agent
from .config import KitConfig, load_config, write_example_config
from .factory import create_agent
from .hooks import HookBus, default_verbose_hooks
from .llm import LLMClient
from .mcp import MCPManager, StdioMCPClient, load_mcp_config
from . import mcp_ext as _mcp_ext  # noqa: F401  — patches prompts onto MCP classes
from .mcp_http import HTTPMCPClient, probe_http_mcp
from .mcp_sse import SSEMCPClient, probe_sse_mcp
from .memory import forget, recall, remember
from .orchestrator import Orchestrator
from .router import MultiLLMRouter, format_probe
from .session import list_sessions, load_session, save_session
from .skills import load_skills
from .tools import execute_tool, get_default_tools
from .usage import UsageStats, estimate_tokens
from .embeddings import embed, hash_embed, ollama_embed
from .vector_memory import vforget, vrecall, vremember
from . import cli as _cli_mod
from .cli_ext import register as _register_cli_ext

_register_cli_ext(_cli_mod.cli)

__all__ = [
    "Agent",
    "create_agent",
    "KitConfig",
    "load_config",
    "write_example_config",
    "HookBus",
    "default_verbose_hooks",
    "LLMClient",
    "MCPManager",
    "StdioMCPClient",
    "HTTPMCPClient",
    "SSEMCPClient",
    "probe_http_mcp",
    "probe_sse_mcp",
    "load_mcp_config",
    "MultiLLMRouter",
    "Orchestrator",
    "UsageStats",
    "estimate_tokens",
    "list_sessions",
    "load_session",
    "save_session",
    "remember",
    "recall",
    "forget",
    "vremember",
    "vrecall",
    "embed",
    "hash_embed",
    "ollama_embed",
    "vforget",
    "load_skills",
    "format_probe",
    "get_default_tools",
    "execute_tool",
    "__version__",
]
