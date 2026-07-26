"""
Built-in tools for the agent.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., str]
    parameters: Optional[Dict[str, Any]] = None


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo."""
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"- {r.get('title', '')}: {r.get('href', '')}\n  {r.get('body', '')[:200]}")
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search failed: {e}"


def execute_python(code: str) -> str:
    """Execute a short Python snippet safely in a subprocess (timeout 10s)."""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            path = f.name
        result = subprocess.run(
            ["python", path],
            capture_output=True,
            text=True,
            timeout=10,
        )
        os.unlink(path)
        output = result.stdout + result.stderr
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return "Execution timed out (10s limit)."
    except Exception as e:
        return f"Execution error: {e}"


def list_directory(path: str = ".") -> str:
    """List files and folders in a directory."""
    try:
        entries = os.listdir(path)
        return "\n".join(sorted(entries)) if entries else "(empty)"
    except Exception as e:
        return str(e)


def read_file(path: str, max_chars: int = 4000) -> str:
    """Read a text file (truncated)."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(max_chars)
        return content
    except Exception as e:
        return str(e)


# Default tool registry
DEFAULT_TOOLS: List[Tool] = [
    Tool(
        name="web_search",
        description="Search the web for up-to-date information",
        func=web_search,
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "default": 5},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="execute_python",
        description="Execute a short Python code snippet and return stdout/stderr",
        func=execute_python,
        parameters={
            "type": "object",
            "properties": {"code": {"type": "string", "description": "Python code to run"}},
            "required": ["code"],
        },
    ),
    Tool(
        name="list_directory",
        description="List files in a directory",
        func=list_directory,
        parameters={
            "type": "object",
            "properties": {"path": {"type": "string", "default": "."}},
            "required": [],
        },
    ),
    Tool(
        name="read_file",
        description="Read the content of a text file",
        func=read_file,
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "max_chars": {"type": "integer", "default": 4000},
            },
            "required": ["path"],
        },
    ),
]


def add_custom_tools(agent: Any) -> None:
    """Helper used by examples to register extra tools."""
    # Already registered by default; this function stays for compatibility
    pass
