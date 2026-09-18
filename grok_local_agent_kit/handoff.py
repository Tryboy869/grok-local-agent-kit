"""Task handoff queue on top of the team blackboard.

Members post work items, claim them, and mark them done. Persistence is the
same cwd-safe JSONL/SQLite path used by the board. Demos need no live LLM.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import List, Optional, Sequence, Union

from .persist import _safe_path
from .team import Blackboard

PathLike = Union[str, Path]
ALLOWED_STATUS = ("open", "claimed", "done", "dropped")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Task:
    id: str
    title: str
    owner: str = "system"
    assignee: str = ""
    status: str = "open"
    note: str = ""
    ts: str = field(default_factory=_now)
    tags: List[str] = field(default_factory=list)

    def render(self) -> str:
        who = self.assignee or "-"
        return f"[{self.status}] {self.id} {self.title} owner={self.owner} assignee={who}"


class HandoffQueue:
    """In-memory queue; optional mirror onto a Blackboard."""

    def __init__(self, board: Optional[Blackboard] = None) -> None:
        self._tasks: List[Task] = []
        self._lock = Lock()
        self._seq = 0
        self.board = board

    def _next_id(self) -> str:
        self._seq += 1
        return f"T{self._seq:03d}"

    def offer(
        self,
        title: str,
        owner: str = "system",
        tags: Optional[Sequence[str]] = None,
        note: str = "",
    ) -> Task:
        with self._lock:
            task = Task(
                id=self._next_id(),
                title=title.strip() or "(untitled)",
                owner=owner,
                note=note,
                tags=list(tags or []),
            )
            self._tasks.append(task)
        self._mirror(task, f"offered {task.id}")
        return task

    def claim(self, task_id: str, assignee: str) -> Task:
        task = self._get(task_id)
        if task.status == "done":
            raise ValueError(f"{task_id} already done")
        task.assignee = assignee
        task.status = "claimed"
        task.ts = _now()
        self._mirror(task, f"claimed by {assignee}")
        return task

    def complete(self, task_id: str, note: str = "") -> Task:
        task = self._get(task_id)
        task.status = "done"
        if note:
            task.note = note
        task.ts = _now()
        self._mirror(task, f"done {task.id}")
        return task

    def drop(self, task_id: str) -> Task:
        task = self._get(task_id)
        task.status = "dropped"
        task.ts = _now()
        self._mirror(task, f"dropped {task.id}")
        return task

    def open_tasks(self) -> List[Task]:
        with self._lock:
            return [t for t in self._tasks if t.status in ("open", "claimed")]

    def all_tasks(self) -> List[Task]:
        with self._lock:
            return list(self._tasks)

    def dump(self) -> str:
        rows = self.all_tasks()
        if not rows:
            return "(empty handoff queue)"
        return "\n".join(t.render() for t in rows)

    def _get(self, task_id: str) -> Task:
        with self._lock:
            for t in self._tasks:
                if t.id == task_id:
                    return t
        raise KeyError(task_id)

    def _mirror(self, task: Task, event: str) -> None:
        if self.board is None:
            return
        self.board.post(
            task.assignee or task.owner or "system",
            f"{event}: {task.title}",
            kind="claim",
            tags=[task.id, task.status],
        )

    def load_tasks(self, tasks: Sequence[Task]) -> None:
        with self._lock:
            self._tasks = list(tasks)
            self._seq = 0
            for t in self._tasks:
                try:
                    n = int(t.id.lstrip("Tt"))
                except ValueError:
                    n = 0
                if n > self._seq:
                    self._seq = n


def save_queue(queue: HandoffQueue, path: PathLike) -> Path:
    dest = _safe_path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(t) for t in queue.all_tasks()]
    suffix = dest.suffix.lower()
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        conn = sqlite3.connect(str(dest))
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS handoff (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    owner TEXT,
                    assignee TEXT,
                    status TEXT,
                    note TEXT,
                    ts TEXT,
                    tags TEXT
                )
                """
            )
            conn.execute("DELETE FROM handoff")
            conn.executemany(
                "INSERT INTO handoff (id, title, owner, assignee, status, note, ts, tags) VALUES (?,?,?,?,?,?,?,?)",
                [
                    (r["id"], r["title"], r["owner"], r["assignee"], r["status"], r["note"], r["ts"], ",".join(r.get("tags") or []))
                    for r in rows
                ],
            )
            conn.commit()
        finally:
            conn.close()
        return dest
    dest.write_text(json.dumps({"version": 1, "tasks": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return dest


def load_queue(path: PathLike, board: Optional[Blackboard] = None) -> HandoffQueue:
    src = _safe_path(path)
    queue = HandoffQueue(board=board)
    if not src.exists():
        return queue
    suffix = src.suffix.lower()
    tasks: List[Task] = []
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        conn = sqlite3.connect(str(src))
        try:
            try:
                rows = conn.execute(
                    "SELECT id, title, owner, assignee, status, note, ts, tags FROM handoff"
                ).fetchall()
            except sqlite3.OperationalError:
                return queue
        finally:
            conn.close()
        for row in rows:
            tasks.append(
                Task(
                    id=row[0],
                    title=row[1],
                    owner=row[2] or "system",
                    assignee=row[3] or "",
                    status=row[4] or "open",
                    note=row[5] or "",
                    ts=row[6] or _now(),
                    tags=[t for t in (row[7] or "").split(",") if t],
                )
            )
    else:
        data = json.loads(src.read_text(encoding="utf-8"))
        raw = data.get("tasks") if isinstance(data, dict) else data
        for row in raw or []:
            tasks.append(
                Task(
                    id=str(row.get("id") or "T000"),
                    title=str(row.get("title") or ""),
                    owner=str(row.get("owner") or "system"),
                    assignee=str(row.get("assignee") or ""),
                    status=str(row.get("status") or "open"),
                    note=str(row.get("note") or ""),
                    ts=str(row.get("ts") or _now()),
                    tags=list(row.get("tags") or []),
                )
            )
    queue.load_tasks(tasks)
    return queue


def demo_handoff(goal: str = "Ship a local handoff without a cloud queue.") -> str:
    board = Blackboard()
    q = HandoffQueue(board=board)
    q.offer(goal, owner="coordinator", tags=["goal"])
    research = q.offer("Collect offline facts about the kit", owner="coordinator")
    ops = q.offer("Write a one-line status note", owner="coordinator")
    q.claim(research.id, "researcher")
    q.complete(research.id, note="facts on the board")
    q.claim(ops.id, "operator")
    q.complete(ops.id, note="status written")
    return q.dump() + "\n---\n" + board.dump()
