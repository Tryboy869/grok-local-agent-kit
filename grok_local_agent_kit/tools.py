"""Built-in tools: web search, file ops (cwd-safe), shell, execute_python, calculator, MCP stub."""

from __future__ import annotations

import ast
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

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


def list_tools() -> str:
    """Return the list of currently registered tools and short descriptions."""
    lines = []
    for schema in TOOL_SPECS:
        fn = schema.get("function", {})
        name = fn.get("name", "?")
        desc = (fn.get("description") or "").strip()
        lines.append(f"- {name}: {desc}")
    return f"Available tools ({len(lines)}):\n" + "\n".join(lines)


def mcp_list_resources() -> str:
    """List available MCP resources (enhanced stub — real client planned for v0.8)."""
    return (
        "MCP client status: enhanced stub (v0.7.1)\n"
        "Planned for v0.8: real stdio + SSE/HTTP MCP client.\n"
        "Current registered resources: none (no live server connected).\n"
        "Interface preview:\n"
        "  mcp_list_resources() → list resources\n"
        "  mcp_list_tools()     → discover external tools\n"
        "  mcp_call_tool(name, arguments) → invoke a remote tool\n"
        "You can still call these tools to exercise the agent loop."
    )


def mcp_call_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
    """Call an MCP tool by name (stub until full MCP client)."""
    return (
        f"MCP tool call stub → name={name}, args={arguments or {}}.\n"
        "Not connected to a live MCP server yet. "
        "Full client lands in v0.8 (stdio + SSE)."
    )


def mcp_list_tools() -> str:
    """List tools that would be available from connected MCP servers (stub)."""
    return (
        "MCP tools discovery stub (v0.7.1).\n"
        "When a real MCP client is connected you will see external tools here.\n"
        "Local tools remain available via the standard registry (see list_tools)."
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
            "name": "list_tools",
            "description": "List all currently registered tools and their short descriptions.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mcp_list_resources",
            "description": "List available MCP resources (stub until full MCP client).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mcp_list_tools",
            "description": "List tools exposed by connected MCP servers (stub).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mcp_call_tool",
            "description": "Call an MCP tool by name (stub until full MCP client).",
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
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_shell": run_shell,
    "execute_python": execute_python,
    "calculator": calculator,
    "get_datetime": get_datetime,
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
