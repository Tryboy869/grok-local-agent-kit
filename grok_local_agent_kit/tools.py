"""Built-in tools: web search, file ops (cwd-safe), shell, execute_python, calculator, http_get, system info, search_files, MCP stdio client."""

from __future__ import annotations

import ast
import json
import math
import os
import platform
import shutil
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
    if DDGS is None:
        return "Error: duckduckgo-search package not installed. Run: pip install duckduckgo-search"
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
    url = (url or "").strip()
    if not url.startswith(("http://", "https://")):
        return "Error: url must start with http:// or https://"
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            r = client.get(url, headers={"User-Agent": "grok-local-agent-kit/0.9.0"})
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


def search_files(query: str, path: str = ".", pattern: str = "*.py", max_matches: int = 20, max_chars_per_file: int = 400) -> str:
    query = (query or "").strip()
    if not query:
        return "Error: query must be non-empty"
    try:
        root = _safe_path(path)
        if not root.exists():
            return f"Path does not exist: {root}"
        matches: List[str] = []
        count = 0
        glob_pat = pattern if "**" in pattern else f"**/{pattern}"
        for p in sorted(root.glob(glob_pat)):
            if not p.is_file():
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if query.lower() not in text.lower():
                continue
            lower = text.lower()
            idx = lower.find(query.lower())
            start = max(0, idx - 80)
            end = min(len(text), idx + len(query) + 80)
            snippet = text[start:end].replace("\n", " ").strip()
            if len(snippet) > max_chars_per_file:
                snippet = snippet[:max_chars_per_file] + "..."
            rel = p.relative_to(Path.cwd()) if p.is_relative_to(Path.cwd()) else p
            matches.append(f"{rel}: ...{snippet}...")
            count += 1
            if count >= max_matches:
                break
        if not matches:
            return f"No matches for '{query}' under {root} (pattern={pattern})"
        return f"Found {len(matches)} match(es) for '{query}':\n" + "\n".join(matches)
    except Exception as e:
        return f"search_files error: {e}"


def read_file(path: str, max_chars: int = 12000) -> str:
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
    try:
        p = _safe_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} chars to {p}"
    except Exception as e:
        return f"write_file error: {e}"


def append_file(path: str, content: str) -> str:
    try:
        p = _safe_path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully appended {len(content)} chars to {p}"
    except Exception as e:
        return f"append_file error: {e}"


def mkdir(path: str) -> str:
    try:
        p = _safe_path(path)
        p.mkdir(parents=True, exist_ok=True)
        return f"Successfully created directory {p}"
    except Exception as e:
        return f"mkdir error: {e}"


def file_stat(path: str) -> str:
    try:
        p = _safe_path(path)
        if not p.exists():
            return f"Path does not exist: {p}"
        st = p.stat()
        kind = "DIR" if p.is_dir() else "FILE"
        return (
            f"{kind} {p}\n"
            f"size: {st.st_size} B\n"
            f"mtime: {datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat()}\n"
            f"mode: {oct(st.st_mode)}"
        )
    except Exception as e:
        return f"file_stat error: {e}"


def copy_file(src: str, dest: str) -> str:
    try:
        s = _safe_path(src)
        d = _safe_path(dest)
        if not s.exists() or not s.is_file():
            return f"Source is not a file: {s}"
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        return f"Successfully copied {s} → {d}"
    except Exception as e:
        return f"copy_file error: {e}"


def delete_file(path: str) -> str:
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
    blocked = ["rm -rf", "rm -r", "mkfs", "dd if=", ":(){", "shutdown", "reboot", "passwd", "chmod 777", "chown", "> /dev/", "curl | sh", "wget | sh", "| bash", "| sh"]
    lower = command.lower()
    for b in blocked:
        if b in lower:
            return f"Blocked potentially dangerous command containing '{b}'."
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout, cwd=str(Path.cwd()))
        out = (result.stdout or "") + (result.stderr or "")
        if result.returncode != 0:
            out = f"[exit {result.returncode}]\n{out}"
        return out[:8000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout}s"
    except Exception as e:
        return f"run_shell error: {e}"


def execute_python(code: str) -> str:
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
            allowed = {"math", "json", "re", "datetime", "collections", "itertools", "functools", "statistics"}
            for n in names:
                if n not in allowed:
                    return f"Blocked import of '{n}'. Allowed: {sorted(allowed)}"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "open", "__import__"}:
                return f"Blocked call to {node.func.id}"
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"system", "popen", "remove", "rmdir"}:
                return f"Blocked attribute call .{node.func.attr}"
    import contextlib, io
    buf = io.StringIO()
    local_ns: Dict[str, Any] = {}
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(tree, "<agent>", "exec"), {"__builtins__": {"print": print, "len": len, "range": range, "str": str, "int": int, "float": float, "list": list, "dict": dict, "set": set, "tuple": tuple, "True": True, "False": False, "None": None, "abs": abs, "min": min, "max": max, "sum": sum, "sorted": sorted, "enumerate": enumerate, "zip": zip, "map": map, "filter": filter, "round": round}}, local_ns)
        out = buf.getvalue()
        return out if out else "(executed, no stdout)"
    except Exception as e:
        return f"execute_python error: {type(e).__name__}: {e}"


def calculator(expression: str) -> str:
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed_names.update({"pi": math.pi, "e": math.e})
    try:
        tree = ast.parse(expression, mode="eval")
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id not in allowed_names and node.id not in {"True", "False"}:
                return f"Blocked name: {node.id}"
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Subscript)):
                return "Blocked construct in calculator"
        result = eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"


def get_datetime(timezone_name: str = "UTC") -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S UTC") + f" (requested: {timezone_name})"


def get_system_info() -> str:
    try:
        lines = [f"OS: {platform.system()} {platform.release()} ({platform.machine()})", f"Python: {sys.version.split()[0]} ({platform.python_implementation()})", f"CWD: {Path.cwd()}", f"Platform: {platform.platform()}", f"CPU count: {os.cpu_count() or '?'}"]
        return "\n".join(lines)
    except Exception as e:
        return f"get_system_info error: {e}"


def list_tools() -> str:
    lines = []
    for schema in TOOL_SPECS:
        fn = schema.get("function", {})
        name = fn.get("name", "?")
        desc = (fn.get("description") or "").strip()
        lines.append(f"- {name}: {desc}")
    return f"Available tools ({len(lines)}):\n" + "\n".join(lines)


def mcp_list_resources() -> str:
    from .mcp import get_manager
    return get_manager().list_resources()


def mcp_list_tools() -> str:
    from .mcp import get_manager
    return get_manager().list_tools()


def mcp_call_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
    from .mcp import get_manager
    return get_manager().call_tool(name, arguments)


TOOL_SPECS: List[Dict[str, Any]] = [
    {"type": "function", "function": {"name": "web_search", "description": "Search the web for up-to-date information.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "max_results": {"type": "integer"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "http_get", "description": "Fetch a URL with a simple GET request and return text content.", "parameters": {"type": "object", "properties": {"url": {"type": "string"}, "max_chars": {"type": "integer"}, "timeout": {"type": "number"}}, "required": ["url"]}}},
    {"type": "function", "function": {"name": "list_files", "description": "List files and directories in a path (restricted to workspace).", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "pattern": {"type": "string"}}, "required": []}}},
    {"type": "function", "function": {"name": "search_files", "description": "Search file contents under a path for a text query (cwd-safe).", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "path": {"type": "string"}, "pattern": {"type": "string"}, "max_matches": {"type": "integer"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a text file (cwd-safe).", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "max_chars": {"type": "integer"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Write text to a file (cwd-safe).", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "append_file", "description": "Append text to a file (cwd-safe).", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "delete_file", "description": "Delete a single file (cwd-safe). Refuses directories.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "mkdir", "description": "Create a directory (cwd-safe, parents allowed).", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "file_stat", "description": "Get size, mtime and type of a path (cwd-safe).", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "copy_file", "description": "Copy a file within the workspace (cwd-safe).", "parameters": {"type": "object", "properties": {"src": {"type": "string"}, "dest": {"type": "string"}}, "required": ["src", "dest"]}}},
    {"type": "function", "function": {"name": "run_shell", "description": "Run a shell command with safety restrictions.", "parameters": {"type": "object", "properties": {"command": {"type": "string"}, "timeout": {"type": "integer"}}, "required": ["command"]}}},
    {"type": "function", "function": {"name": "execute_python", "description": "Execute a short Python snippet safely.", "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}},
    {"type": "function", "function": {"name": "calculator", "description": "Safely evaluate a mathematical expression.", "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "get_datetime", "description": "Get the current date and time (UTC).", "parameters": {"type": "object", "properties": {"timezone_name": {"type": "string"}}, "required": []}}},
    {"type": "function", "function": {"name": "get_system_info", "description": "Get basic system information (OS, Python version, cwd, CPU count).", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "list_tools", "description": "List all currently registered tools and their short descriptions.", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "mcp_list_resources", "description": "List MCP resources and configured servers (live stdio client).", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "mcp_list_tools", "description": "Discover tools from configured MCP stdio servers.", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "mcp_call_tool", "description": "Call a tool on a configured MCP stdio server.", "parameters": {"type": "object", "properties": {"name": {"type": "string"}, "arguments": {"type": "object"}}, "required": ["name"]}}},
]

TOOL_FUNCS: Dict[str, Callable[..., str]] = {
    "web_search": web_search, "http_get": http_get, "list_files": list_files, "search_files": search_files,
    "read_file": read_file, "write_file": write_file, "append_file": append_file, "delete_file": delete_file,
    "mkdir": mkdir, "file_stat": file_stat, "copy_file": copy_file,
    "run_shell": run_shell, "execute_python": execute_python, "calculator": calculator, "get_datetime": get_datetime,
    "get_system_info": get_system_info, "list_tools": list_tools, "mcp_list_resources": mcp_list_resources,
    "mcp_list_tools": mcp_list_tools, "mcp_call_tool": mcp_call_tool,
}


def get_default_tools() -> tuple[List[Dict[str, Any]], Dict[str, Callable[..., str]]]:
    return TOOL_SPECS, dict(TOOL_FUNCS)


def execute_tool(name: str, arguments: Dict[str, Any], registry: Dict[str, Callable[..., str]]) -> str:
    if name not in registry:
        return f"Unknown tool: {name}"
    try:
        return registry[name](**arguments)
    except TypeError as e:
        return f"Invalid arguments for {name}: {e}"
    except Exception as e:
        return f"Tool {name} failed: {e}"
