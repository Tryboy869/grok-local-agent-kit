"""Grok Local Agent Kit — local-first AI agents with tools & multi-LLM support."""

__version__ = "0.61.0"

from .agent import Agent
from .config import KitConfig, load_config, write_example_config
from .factory import create_agent
from .hooks import HookBus, default_verbose_hooks
from .llm import LLMClient
from .mcp import MCPManager, StdioMCPClient, load_mcp_config
from . import mcp_ext as _mcp_ext  # noqa: F401
from .mcp_http import HTTPMCPClient, probe_http_mcp
from .mcp_sse import SSEMCPClient, probe_sse_mcp
from .memory import forget, recall, remember
from .orchestrator import Orchestrator
from .router import MultiLLMRouter, format_probe, demo_routed_health, demo_persisted_route
from .session import list_sessions, load_session, save_session
from .skills import load_skills
from .tools import execute_tool, get_default_tools
from .usage import UsageStats, estimate_tokens
