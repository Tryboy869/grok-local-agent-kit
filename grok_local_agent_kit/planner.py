"""Lightweight workspace planner (JSON todos under .grok/plan.json)."""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


PLAN_PATH = Path(".grok") / "plan.json"
_lock = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load() -> List[Dict[str, Any]]:
    if not PLAN_PATH.exists():
        return []
    try:
        data = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        items = data.get("items", data if isinstance(data, list) else [])
        return items if isinstance(items, list) else []
    except Exception:
        return []


def _save(items: List[Dict[str, Any]]) -> None:
    PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLAN_PATH.write_text(
        json.dumps({"updated": _now(), "items": items}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def plan_add(title: str, notes: str = "") -> str:
    title = (title or "").strip()
    if not title:
        return "Error: title must be non-empty"
    with _lock:
        items = _load()
        item = {
            "id": len(items) + 1,
            "title": title,
            "notes": notes or "",
            "status": "open",
            "created": _now(),
        }
        items.append(item)
        _save(items)
    return f"Added plan item #{item['id']}: {title}"


def plan_list(status: str = "all") -> str:
    items = _load()
    status = (status or "all").lower()
    if status != "all":
        items = [i for i in items if str(i.get("status")) == status]
    if not items:
        return "Plan is empty."
    lines = []
    for i in items:
        lines.append(f"#{i.get('id')} [{i.get('status')}] {i.get('title')} — {i.get('notes', '')}")
    return f"Plan ({len(items)}):\n" + "\n".join(lines)


def plan_done(item_id: int) -> str:
    with _lock:
        items = _load()
        for i in items:
            if int(i.get("id", 0)) == int(item_id):
                i["status"] = "done"
                i["done_at"] = _now()
                _save(items)
                return f"Marked #{item_id} done: {i.get('title')}"
    return f"No plan item #{item_id}"


def plan_clear(done_only: bool = True) -> str:
    with _lock:
        items = _load()
        if done_only:
            kept = [i for i in items if i.get("status") != "done"]
            removed = len(items) - len(kept)
            _save(kept)
            return f"Cleared {removed} done item(s)."
        _save([])
        return "Cleared entire plan."
