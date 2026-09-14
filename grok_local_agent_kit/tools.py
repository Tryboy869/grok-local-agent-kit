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
    from .websearch import search_web
    return search_web(query, max_results=max_results)
