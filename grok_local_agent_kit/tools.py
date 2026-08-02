"""Built-in tools: web search, file ops (cwd-safe), shell, execute_python, calculator, MCP stub."""

from __future__ import annotations

import ast
import math
import os
import subprocess
import tempfile
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
    except PermissionError as e:
        return str(e)
    except Exception as e:
        return f"Error listing files: {e}"


def read_file(path: str, max_chars: int = 8000) -> str:
    """Read a text file (truncated for safety, cwd-restricted)."""
    try:
        p = _safe_path(path)
        if not p.is_file():
            return f"Not a file: {p}"
        text = p.read_text(encoding="utf-8", errors="replace")
        if len(text) > max_chars:
            return text[:max_chars] + f"\n\n... [truncated, total {len(text)} chars]"
        return text
    except PermissionError as e:
        return str(e)
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file (creates parent dirs, cwd-restricted)."""
    try:
        p = _safe_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} chars to {p}"
    except PermissionError as e:
        return str(e)
    except Exception as e:
        return f"Error writing file: {e}"


def run_shell(command: str, timeout: int = 30) -> str:
    """Run a shell command (basic safety + timeout)."""
    blocked = [
        "rm -rf /",
        "rm -rf /*",
        "mkfs",
        ":(){:|:&};:",
        "dd if=/dev/zero",
        "chmod -R 777 /",
        "> /dev/sda",
        "shutdown",
        "reboot",
        "poweroff",
        "halt",
        "init 0",
        "init 6",
        "fork bomb",
        "curl | bash",
        "wget | sh",
    ]
    lower = command.lower()
    for b in blocked:
        if b in lower:
            return f"Blocked potentially dangerous command containing: {b}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd(),
        )
        out = result.stdout.strip()
        err = result.stderr.strip()
        if result.returncode != 0:
            return f"Exit {result.returncode}\nSTDOUT:\n{out}\nSTDERR:\n{err}"
        return out or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout}s"
    except Exception as e:
        return f"Shell error: {e}"


def execute_python(code: str, timeout: int = 15) -> str:
    """Execute a short Python snippet in a temporary file (sandbox-ish)."""
    forbidden = [
        "os.system",
        "subprocess",
        "__import__",
        "open(",
        "eval(",
        "exec(",
        "compile(",
        "getattr(",
        "setattr(",
        "globals(",
        "locals(",
        "breakpoint(",
        "input(",
        "importlib",
        "ctypes",
        "socket",
        "urllib",
        "requests",
    ]
    for f in forbidden:
        if f in code:
            return f"Blocked code containing potentially unsafe construct: {f}"

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        result = subprocess.run(
            ["python", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd(),
        )
        Path(tmp_path).unlink(missing_ok=True)

        out = result.stdout.strip()
        err = result.stderr.strip()
        if result.returncode != 0:
            return f"Exit {result.returncode}\nSTDOUT:\n{out}\nSTDERR:\n{err}"
        return out or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Python execution timed out after {timeout}s"
    except Exception as e:
        return f"execute_python error: {e}"


def calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression (no side effects)."""
    try:
        tree = ast.parse(expression, mode="eval")
        allowed_names = {
            "abs",
            "round",
            "min",
            "max",
            "sum",
            "pow",
            "sqrt",
            "sin",
            "cos",
            "tan",
            "log",
            "log10",
            "exp",
            "pi",
            "e",
            "True",
            "False",
        }
        allowed_funcs = {
            "abs",
            "round",
            "min",
            "max",
            "sum",
            "pow",
            "sqrt",
            "sin",
            "cos",
            "tan",
            "log",
            "log10",
            "exp",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id not in allowed_names:
                return f"Blocked name in expression: {node.id}"
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name) or node.func.id not in allowed_funcs:
                    return "Blocked complex call"
            if isinstance(node, (ast.Attribute, ast.Subscript, ast.Import, ast.ImportFrom)):
                return "Blocked node type in expression"

        safe_globals = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
        }
        result = eval(compile(tree, "<calculator>", "eval"), safe_globals, {})
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"


def mcp_list_resources() -> str:
    """List available MCP resources (enhanced stub — real client in next release)."""
    return (
        "MCP client status: stub (v0.6.0)\n"
        "Planned for next minor: real stdio + SSE MCP client.\n"
        "Current registered resources: none.\n"
        "You can still call mcp_call_tool for testing the interface."
    )


def mcp_call_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
    """Call an MCP tool by name (stub until full MCP client)."""
    return (
        f"MCP tool call stub → name={name}, args={arguments or {}}.\n"
        "Not connected to a live MCP server yet. "
        "Wire a real server in v0.6.x / v0.7."
    )


def mcp_list_tools() -> str:
    """List tools that would be available from connected MCP servers (stub)."""
    return (
        "MCP tools discovery stub.\n"
        "When a real MCP client is connected you will see external tools here.\n"
        "Local tools remain available via the standard registry."
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
            "description": "List files and directories in a path (workspace-restricted).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path (default '.')"},
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
            "description": "Read the content of a text file (workspace-restricted).",
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
            "description": "Write text content to a file (workspace-restricted).",
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
            "description": "Execute a shell command and return stdout/stderr (with safety filters).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to run"},
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
            "description": "Execute a short Python code snippet and return its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python source code"},
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds (default 15)",
                    },
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
