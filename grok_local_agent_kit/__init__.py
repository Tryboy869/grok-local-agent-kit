"""Grok Local Agent Kit — local-first AI agents with tools & multi-LLM support."""

__version__ = "0.24.0"

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
from .router import MultiLLMRouter, format_probe
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
from .recipes import Recipe, load_recipe, run_recipe
from .cancel import (
    CancelToken,
    CancelledError,
    ProcessRegistry,
    cancel_all,
    get_registry,
    get_token,
    set_token,
)
from .mcp_session import (
    MCPSession,
    MCPSessionRegistry,
    get_registry as get_mcp_registry,
    reset_registry as reset_mcp_registry,
    run_cancellable,
)
from .evalkit import EvalCase, load_cases, run_suite, format_report
from .cache import ToolCache, cache_key, cached_execute, get_cache, reset_cache
from .telemetry import Telemetry, ToolEvent, get_telemetry, reset_telemetry, timed_execute
from .budget import ToolBudget, get_budget, set_budget, reset_budget, BudgetExceeded
from .retry import retry_call
from .plugins import apply_plugins, discover_plugins
from .transcripts import append_turn, list_transcripts, new_path as new_transcript, read_transcript
from .shell import patch_tools as _patch_tools
from .runtime import patch as _patch_runtime
from . import cli as _cli_mod
from .cli_ext import register as _register_cli_ext
from .cli_v021 import register as _register_cli_v021
from .cli_v022 import register as _register_cli_v022
from .cli_v023 import register as _register_cli_v023
from .cli_v024 import register as _register_cli_v024

_register_cli_ext(_cli_mod.cli)
_register_cli_v021(_cli_mod.cli)
_register_cli_v022(_cli_mod.cli)
_register_cli_v023(_cli_mod.cli)
_register_cli_v024(_cli_mod.cli)
_patch_tools()
_patch_runtime()

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
    "active_backend",
    "vec_describe",
    "vec_knn",
    "embed",
    "hash_embed",
    "ollama_embed",
    "vforget",
    "load_skills",
    "format_probe",
    "get_default_tools",
    "execute_tool",
    "ToolGuard",
    "get_guard",
    "set_guard",
    "plan_add",
    "plan_list",
    "plan_done",
    "Scheduler",
    "serve",
    "run_forever",
    "load_trace",
    "replay_file",
    "replay_tools",
    "summarize_trace",
    "CancelToken",
    "CancelledError",
    "ProcessRegistry",
    "cancel_all",
    "get_registry",
    "get_token",
    "set_token",
    "FileEvent",
    "watch",
    "watch_diff",
    "watch_snapshot",
    "extract_json",
    "extract_json_or_none",
    "require_keys",
    "Recipe",
    "load_recipe",
    "run_recipe",
    "MCPSession",
    "MCPSessionRegistry",
    "get_mcp_registry",
    "reset_mcp_registry",
    "run_cancellable",
    "EvalCase",
    "load_cases",
    "run_suite",
    "format_report",
    "ToolCache",
    "cache_key",
    "cached_execute",
    "get_cache",
    "reset_cache",
    "Telemetry",
    "ToolEvent",
    "get_telemetry",
    "reset_telemetry",
    "timed_execute",
    "ToolBudget",
    "get_budget",
    "set_budget",
    "reset_budget",
    "BudgetExceeded",
    "retry_call",
    "apply_plugins",
    "discover_plugins",
    "append_turn",
    "list_transcripts",
    "new_transcript",
    "read_transcript",
    "__version__",
]
