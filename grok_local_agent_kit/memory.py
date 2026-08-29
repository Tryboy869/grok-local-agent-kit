"""Tiny local memory: JSONL notes under .grok/memory/."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

MEMORY_DIR = Path(".grok") / "memory"
MEMORY_FILE = MEMORY_DIR / "notes.jsonl"


def _ensure_dir() -> Path:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    return MEMORY_FILE


def remember(text: str, tags: str = "") -> str:
    text = (text or "").strip()
    if not text:
        return "remember error: empty note"
    path = _ensure_dir()
    note = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "text": text,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(note, ensure_ascii=False) + "\n")
    return f"Remembered ({len(text)} chars)."


def recall(query: str = "", limit: int = 8) -> str:
    path = MEMORY_FILE
    if not path.exists():
        return "No memory notes yet."
    notes: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            notes.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    query = (query or "").strip().lower()
    if query:
        tokens = [t for t in re.split(r"\s+", query) if t]
        scored = []
        for n in notes:
            blob = (n.get("text") or "") + " " + " ".join(n.get("tags") or [])
            blob_l = blob.lower()
            score = sum(1 for t in tokens if t in blob_l)
            if score:
                scored.append((score, n))
        scored.sort(key=lambda x: x[0], reverse=True)
        picked = [n for _, n in scored[: max(1, limit)]]
    else:
        picked = notes[-max(1, limit) :]
    if not picked:
        return f"No memory matches for {query!r}."
    lines = []
    for n in picked:
        tags = ",".join(n.get("tags") or [])
        tag_s = f" [{tags}]" if tags else ""
        lines.append(f"- {n.get('ts', '?')}{tag_s}: {n.get('text', '')}")
    return "Memory:\n" + "\n".join(lines)


def forget(query: str) -> str:
    query = (query or "").strip().lower()
    if not query:
        return "forget error: query required"
    path = MEMORY_FILE
    if not path.exists():
        return "No memory notes yet."
    kept: List[str] = []
    removed = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw:
            continue
        try:
            n = json.loads(raw)
        except json.JSONDecodeError:
            kept.append(raw)
            continue
        blob = ((n.get("text") or "") + " " + " ".join(n.get("tags") or [])).lower()
        if query in blob:
            removed += 1
            continue
        kept.append(raw)
    path.write_text(("\n".join(kept) + ("\n" if kept else "")), encoding="utf-8")
    return f"Forgot {removed} note(s) matching {query!r}."


def memory_stats() -> str:
    if not MEMORY_FILE.exists():
        return "memory: 0 notes"
    n = sum(1 for line in MEMORY_FILE.read_text(encoding="utf-8").splitlines() if line.strip())
    return f"memory: {n} notes in {MEMORY_FILE}"
