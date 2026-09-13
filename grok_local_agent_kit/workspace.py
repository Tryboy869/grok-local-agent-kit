"""Workspace packer + lightweight file RAG (cwd-safe, no live LLM)."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

from .embeddings import embed
from .tools import _safe_path

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "dist",
    "build",
}

TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".toml",
    ".json",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".rst",
    ".csv",
}


def _iter_files(root: Path, suffixes: Iterable[str], max_files: int) -> List[Path]:
    out: List[Path] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in suffixes:
            continue
        out.append(p)
        if len(out) >= max_files:
            break
    return out


def pack_workspace(
    path: str = ".",
    max_files: int = 40,
    max_chars_per_file: int = 400,
    max_total_chars: int = 8000,
) -> str:
    """Summarize a workspace: relative paths + head snippets."""
    try:
        root = _safe_path(path)
    except Exception as e:
        return f"pack_workspace error: {e}"
    if not root.exists():
        return f"Path does not exist: {root}"
    files = _iter_files(root, TEXT_SUFFIXES, max_files)
    if not files:
        return f"No text files under {root}"
    lines = [f"Workspace pack of {root} ({len(files)} file(s)):"]
    used = 0
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        snippet = text[:max_chars_per_file].replace("\n", " ").strip()
        try:
            rel = p.relative_to(Path.cwd())
        except ValueError:
            rel = p
        block = f"- {rel} ({p.stat().st_size} B): {snippet}"
        if used + len(block) > max_total_chars:
            lines.append("... truncated")
            break
        lines.append(block)
        used += len(block)
    return "\n".join(lines)


def _cosine(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    num = sum(x * y for x, y in zip(a, b))
    da = sum(x * x for x in a) ** 0.5
    db = sum(y * y for y in b) ** 0.5
    if da == 0 or db == 0:
        return 0.0
    return num / (da * db)


def search_workspace(
    query: str,
    path: str = ".",
    top_k: int = 5,
    max_files: int = 80,
    chunk_chars: int = 500,
) -> str:
    """Rank workspace text files against a query using local hash embeddings."""
    query = (query or "").strip()
    if not query:
        return "Error: query must be non-empty"
    try:
        root = _safe_path(path)
    except Exception as e:
        return f"search_workspace error: {e}"
    if not root.exists():
        return f"Path does not exist: {root}"
    qv = embed(query)
    scored: List[Tuple[float, str, str]] = []
    for p in _iter_files(root, TEXT_SUFFIXES, max_files):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        chunk = text[:chunk_chars]
        score = _cosine(qv, embed(chunk))
        try:
            rel = str(p.relative_to(Path.cwd()))
        except ValueError:
            rel = str(p)
        snippet = chunk.replace("\n", " ").strip()[:240]
        scored.append((score, rel, snippet))
    scored.sort(key=lambda t: t[0], reverse=True)
    top = scored[: max(1, int(top_k))]
    if not top:
        return f"No files to search under {root}"
    lines = [f"Top {len(top)} hit(s) for {query!r}:"]
    for score, rel, snippet in top:
        lines.append(f"- {rel} (score={score:.3f}): {snippet}")
    return "\n".join(lines)


def register_tools() -> None:
    """Attach pack_workspace / search_workspace to the default tool registry."""
    from . import tools as t

    if any(s.get("function", {}).get("name") == "pack_workspace" for s in t.TOOL_SPECS):
        return
    t.TOOL_SPECS.extend(
        [
            {
                "type": "function",
                "function": {
                    "name": "pack_workspace",
                    "description": "Summarize the workspace: file list plus short snippets (cwd-safe).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "max_files": {"type": "integer"},
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_workspace",
                    "description": "Rank workspace files against a query using local embeddings (cwd-safe).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "path": {"type": "string"},
                            "top_k": {"type": "integer"},
                        },
                        "required": ["query"],
                    },
                },
            },
        ]
    )
    t.TOOL_FUNCS["pack_workspace"] = pack_workspace
    t.TOOL_FUNCS["search_workspace"] = search_workspace
