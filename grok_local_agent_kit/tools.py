"""Built-in tools: web search, file ops (cwd-safe), shell, execute_python, calculator, http_get, system info, MCP foundation."""

from __future__ import annotations

import ast
import json
import math
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import httpx

try:
    from duckduckgo_search import DDGS
except ImportError:  # pragma: no cover
    DDGS = None  # type: ignore


def _safe_path(path: str, must_be_under_cwd: bool = True) -> Path:
    """Resolve path and optionally enforce it stays under current working directory."""
    p = Path(path).expanduser().resolve()
    if must_be_under_cwd:
        cwd = Path.cwd().resolve()
        try:
            p.relative_to(cwd)
        except ValueError:
            raise PermissionError(
                f"Path '{p}' is outside the working directory '{cwd}'. "
                "For safety, file tools are restricted to the current workspace."
            )
    return p


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web (DuckDuckGo). Returns a concise summary of results."""
    if DDGS is None:
        return (
            "Error: duckduckgo-search package not installed. "
            "Run: pip install duckduckgo-search"
        )
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "No results found."
        lines = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            href = r.get("href", "")
            body = (r.get("body") or "")[:250]
            lines.append(f"{i}. {title}\n   URL: {href}\n   {body}")
        return "\n\n".join(lines)
    except Exception as e:
        return f"Search error: {e}"


def http_get(url: str, max_chars: int = 8000, timeout: float = 15.0) -> str:
    """Fetch a URL with a simple GET request (text content only)."""
    url = (url or "").strip()
    if not url.startswith(("http://", "https://")):
        return "Error: url must start with http:// or https://"
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            r = client.get(url, headers={"User-Agent": "grok-local-agent-kit/0.8.5"})
            r.raise_for_status()
            text = r.text or ""
            if len(text) > max_chars:
                return text[:max_chars] + f"\n\n... [truncated, {len(text) - max_chars} more chars]"
            return text if text else "(empty response)"
    except httpx.TimeoutException:
        return f"http_get timed out after {timeout}s"
    except Exception as e:
        return f"http_get error: {e}"


def list_files(path: str = ".", pattern: str = "*") -> str:
    """List files and directories in the given path (restricted to workspace)."""
    try:
        p = _safe_path(path)
        if not p.exists():
            return f"Path does not exist: {p}"
        items = sorted(p.glob(pattern))
        if not items:
            return f"No items matching '{pattern}' in {p}"
        lines = []
        for item in items[:150]:
            kind = "DIR " if item.is_dir() else "FILE"
            size = f" ({item.stat().st_size} B)" if item.is_file() else ""
            lines.append(f"{kind}  {item.name}{size}")
        if len(items) > 150:
            lines.append(f"... and {len(items) - 150} more")
        return "\n".join(lines)
    except Exception as e:
        return f"list_files error: {e}"


def read_file(path: str, max_chars: int = 12000) -> str:
    """Read a text file (cwd-safe)."""
    try:
        p = _safe_path(path)
        if not p.exists():
            return f"File not found: {p}"
        if not p.is_file():
            return f"Not a file: {p}"
        text = p.read_text(encoding="utf-8", errors="replace")
        if len(text) > max_chars:
            return text[:max_chars] + f"\n\n... [truncated, {len(text) - max_chars} more chars]"
        return text
    except Exception as e:
        return f"read_file error: {e}"


def write_file(path: str, content: str) -> str:
    """Write text to a file (cwd-safe). Creates parent dirs if needed."""
    try:
        p = _safe_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} chars to {p}"
    except Exception as e:
        return f"write_file error: {e}"


def append_file(path: str, content: str) -> str:
    """Append text to a file (cwd-safe). Creates the file if missing."""
    try:
        p = _safe_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully appended {len(content)} chars to {p}"
    except Exception as e:
        return f"append_file error: {e}"


def delete_file(path: str) -> str:
    """Delete a single file (cwd-safe). Directories are refused."""
    try:
        p = _safe_path(path)
        if not p.exists():
            return f"File not found: {p}"
        if not p.is_file():
            return f"Refused: '{p}' is not a regular file (directories are not deleted)."
        p.unlink()
        return f"Successfully deleted {p}"
    except Exception as e:
        return f"delete_file error: {e}"


def run_shell(command: str, timeout: int = 30) -> str:
    """Run a shell command with basic safety restrictions."""
    blocked = ["rm -rf", "mkfs", "dd if=", ":(){", "shutdown", "reboot", "passwd"]
    lower = command.lower()
    for b in blocked:
        if b in lower:
            return f"Blocked potentially dangerous command containing '{b}'."
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(Path.cwd()),
        )
        out = (result.stdout or "") + (result.stderr or "")
        if result.returncode != 0:
            out = f"[exit {result.returncode}]\n{out}"
        return out[:8000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout}s"
    except Exception as e:
        return f"run_shell error: {e}"


def execute_python(code: str) -> str:
    """Execute a short Python snippet in a restricted environment."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Syntax error: {e}"

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            else:
                names = [node.module.split(".")[0]] if node.module else []
            allowed = {
                "math",
                "json",
                "re",
                "datetime",
                "collections",
                "itertools",
                "functools",
                "statistics",
            }
            for n in names:
                if n not in allowed:
                    return f"Blocked import of '{n}'. Allowed: {sorted(allowed)}"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {
                "eval",
                "exec",
                "compile",
                "open",
                "__import__",
            }:
                return f"Blocked call to {node.func.id}"
            if isinstance(node.func, ast.Attribute) and node.func.attr in {
                "system",
                "popen",
                "remove",
                "rmdir",
            }:
                return f"Blocked attribute call .{node.func.attr}"

    import contextlib
    import io

    buf = io.StringIO()
    local_ns: Dict[str, Any] = {}
    try:
        with contextlib.redirect_stdout(buf):
            exec(
                compile(tree, "<agent>", "exec"),
                {
                    "__builtins__": {
                        "print": print,
                        "len": len,
                        "range": range,
                        "str": str,
                        "int": int,
                        "float": float,
                        "list": list,
                        "dict": dict,
                        "set": set,
                        "tuple": tuple,
                        "True": True,
                        "False": False,
                        "None": None,
                        "abs": abs,
                        "min": min,
                        "max": max,
                        "sum": sum,
                        "sorted": sorted,
                        "enumerate": enumerate,
                        "zip": zip,
                        "map": map,
                        "filter": filter,
                        "round": round,
                    }
                },
                local_ns,
            )
        out = buf.getvalue()
        return out if out else "(executed, no stdout)"
    except Exception as e:
        return f"execute_python error: {type(e).__name__}: {e}"


def calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed_names.update({"pi": math.pi, "e": math.e})
    try:
        tree = ast.parse(expression, mode="eval")
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id not in allowed_names and node.id not in {
                "True",
                "False",
            }:
                return f"Blocked name: {node.id}"
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Subscript)):
                return "Blocked construct in calculator"
        result = eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"


def get_datetime(timezone_name: str = "UTC") -> str:
    """Return current date and time (UTC). timezone_name is informational."""
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S UTC") + f" (requested: {timezone_name})"


def get_system_info() -> str:
    """Return basic system information useful for local agents (OS, Python, cwd)."""
    try:
        lines = [
            f"OS: {platform.system()} {platform.release()} ({platform.machine()})",
            f"Python: {sys.version.split()[0]} ({platform.python_implementation()})",
            f"CWD: {Path.cwd()}",
            f"Platform: {platform.platform()}",
            f"CPU count: {os.cpu_count() or '?'}",
        ]
        return "\n".join(lines)
    except Exception as e:
        return f"get_system_info error: {e}"


def list_tools() -> str:
    """Return the list of currently registered tools and short descriptions."""
    lines = []
    for schema in TOOL_SPECS:
        fn = schema.get("function", {})
        name = fn.get("name", "?")
        desc = (fn.get("description") or "").strip()
        lines.append(f"- {name}: {desc}")
    return f"Available tools ({len(lines)}):\n" + "\n".join(lines)


def _load_mcp_config() -> Dict[str, Any]:
    """Load optional MCP server list from env or local config file (foundation for v0.8+)."""
    raw = os.environ.get("GROK_MCP_SERVERS", "").strip()
    if raw:
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return {"servers": data}
            if isinstance(data, dict) and "servers" in data:
                return data
        except json.JSONDecodeError as e:
            return {"servers": [], "error": f"Invalid GROK_MCP_SERVERS JSON: {e}"}
    for candidate in (".mcp_servers.json", "mcp_servers.json", ".grok/mcp.json"):
        p = Path(candidate)
        if p.is_file():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data, dict) and "servers" in data:
                    return data
                if isinstance(data, list):
                    return {"servers": data}
            except Exception as e:
                return {"servers": [], "error": f"Failed to parse {candidate}: {e}"}
    return {"servers": []}


def mcp_list_resources() -> str:
    """List available MCP resources (foundation — real stdio/SSE client in progress)."""
    cfg = _load_mcp_config()
    servers = cfg.get("servers") or []
    err = cfg.get("error")
    lines = [
        "MCP client status: foundation (v0.8.x) — full stdio + SSE client is next",
        f"Configured servers: {len(servers)}",
    ]
    if err:
        lines.append(f"Config note: {err}")
    for i, s in enumerate(servers[:10], 1):
        if not isinstance(s, dict):
            lines.append(f"  {i}. (invalid entry: {type(s).__name__})")
            continue
        name = s.get("name") or s.get("command") or f"server_{i}"
        transport = s.get("transport") or ("stdio" if s.get("command") else "unknown")
        lines.append(f"  {i}. {name} ({transport})")
    if not servers:
        lines.append("No servers configured. Set GROK_MCP_SERVERS or create .mcp_servers.json.")
        lines.append(
            'Example: [{"name":"fs","command":"npx","args":["-y","@modelcontextprotocol/server-filesystem","."]}]'
        )
    lines.append("Interface: mcp_list_resources / mcp_list_tools / mcp_call_tool")
    return "\n".join(lines)


def mcp_list_tools() -> str:
    """List tools that would be available from connected MCP servers (foundation)."""
    cfg = _load_mcp_config()
    servers = cfg.get("servers") or []
    if not servers:
        return (
            "MCP tools discovery (v0.8.x foundation).\n"
            "No MCP servers configured yet.\n"
            "When the full client is connected, external tools appear here.\n"
            "Local tools remain available via list_tools."
        )
    names = []
    for s in servers:
        if isinstance(s, dict):
            names.append(s.get("name") or s.get("command") or "?")
        else:
            names.append("?")
    return (
        f"MCP tools discovery (v0.8.x foundation) — {len(servers)} server(s) configured: "
        + ", ".join(names)
        + ".\nFull discovery lands with the real stdio/SSE client."
    )


def mcp_call_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
    """Call an MCP tool by name (foundation until full MCP client)."""
    cfg = _load_mcp_config()
    servers = cfg.get("servers") or []
    return (
        f"MCP tool call foundation → name={name}, args={arguments or {}}.\n"
        f"Configured servers: {len(servers)}. "
        "Not yet connected to a live MCP process. Full client continues in 0.8.x."
    )


# Tool registry with OpenAI/Ollama-compatible schemas
TOOL_SPECS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for up-to-date information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {
                        "type": "integer",
                        "description": "Max results (default 5)",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "http_get",
            "description": "Fetch a URL with a simple GET request and return text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Full URL (http/https)"},
                    "max_chars": {
                        "type": "integer",
                        "description": "Max characters to return (default 8000)",
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Timeout in seconds (default 15)",
                    },
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories in a path (restricted to workspace).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path (default '.')",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern (default '*')",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file (cwd-safe).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "max_chars": {
                        "type": "integer",
                        "description": "Max characters to return",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a file (cwd-safe).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "append_file",
            "description": "Append text to a file (cwd-safe). Creates the file if it does not exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to append"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a single file (cwd-safe). Refuses directories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to delete"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Run a shell command with safety restrictions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command"},
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds",
                    },
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Execute a short Python snippet safely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to run"},
                },
                "required": ["code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Safely evaluate a mathematical expression (e.g. '2+2', 'sqrt(16)+pi').",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate",
                    },
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_datetime",
            "description": "Get the current date and time (UTC).",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone_name": {
                        "type": "string",
                        "description": "Requested timezone name (informational; result is always UTC)",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_info",
            "description": "Get basic system information (OS, Python version, cwd, CPU count).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tools",
            "description": "List all currently registered tools and their short descriptions.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mcp_list_resources",
            "description": "List available MCP resources / configured servers (MCP foundation).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mcp_list_tools",
            "description": "List tools exposed by configured MCP servers (foundation).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mcp_call_tool",
            "description": "Call an MCP tool by name (foundation until full MCP client).",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "arguments": {"type": "object"},
                },
                "required": ["name"],
            },
        },
    },
]

TOOL_FUNCS: Dict[str, Callable[..., str]] = {
    "web_search": web_search,
    "http_get": http_get,
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "append_file": append_file,
    "delete_file": delete_file,
    "run_shell": run_shell,
    "execute_python": execute_python,
    "calculator": calculator,
    "get_datetime": get_datetime,
    "get_system_info": get_system_info,
    "list_tools": list_tools,
    "mcp_list_resources": mcp_list_resources,
    "mcp_list_tools": mcp_list_tools,
    "mcp_call_tool": mcp_call_tool,
}


def get_default_tools() -> tuple[List[Dict[str, Any]], Dict[str, Callable[..., str]]]:
    """Return (tool schemas, name→function map)."""
    return TOOL_SPECS, dict(TOOL_FUNCS)


def execute_tool(
    name: str, arguments: Dict[str, Any], registry: Dict[str, Callable[..., str]]
) -> str:
    """Execute a tool by name with given arguments."""
    if name not in registry:
        return f"Unknown tool: {name}"
    try:
        return registry[name](**arguments)
    except TypeError as e:
        return f"Invalid arguments for {name}: {e}"
    except Exception as e:
        return f"Tool {name} failed: {e}"
