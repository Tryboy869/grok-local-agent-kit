"""Grok Local Agent Kit — local-first AI agents with tools & multi-LLM support."""

__version__ = "0.52.0"

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
from .embeddings import embed, hash_embed, ollama_embed
from .vector_memory import vforget, vrecall, vremember
from .sqlite_vec_store import active_backend, describe as vec_describe, knn as vec_knn
from .guardrails import ToolGuard, get_guard, set_guard
from .planner import plan_add, plan_done, plan_list
from .scheduler import Scheduler
from .serve import serve, run_forever
from .replay import load_trace, replay_file, replay_tools, summarize_trace
from .watch import FileEvent, diff as watch_diff, snapshot as watch_snapshot, watch
from .structured import extract_json, extract_json_or_none, require_keys
from .mvp import demo_mvp, probe_providers, run_mvp, route_intent
from .pack import demo_pack, load_pack, run_pack
from .playbook import demo_playbook, demo_react, execute_handoff, handoff_plan, load_playbook, run_playbook, scripted_react
