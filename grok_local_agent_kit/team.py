"""Multi-agent team with a shared blackboard.

Unlike Orchestrator (planner then sequential specialists via full Agent.run),
Team keeps a durable board: members read recent posts and append notes /
claims / artifacts. Handlers can be plain callables (LLM-free tests) or thin
wrappers around Agent.run. v0.29 adds JSONL / SQLite persistence via persist.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Callable, Dict, Iterable, List, Optional, Sequence


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


ALLOWED_KINDS = ("goal", "note", "claim", "question", "answer", "artifact", "system")


@dataclass
class Post:
    author: str
    kind: str
    body: str
    ts: str = field(default_factory=_now)
    tags: List[str] = field(default_factory=list)

    def render(self) -> str:
        tag = f" [{' '.join(self.tags)}]" if self.tags else ""
        return f"[{self.ts}] {self.author}/{self.kind}{tag}: {self.body}"


class Blackboard:
    """Thread-safe shared memory for a team."""

    def __init__(self) -> None:
        self._posts: List[Post] = []
        self._lock = Lock()

    def post(
        self,
        author: str,
        body: str,
        kind: str = "note",
        tags: Optional[Sequence[str]] = None,
    ) -> Post:
        kind = (kind or "note").lower()
        if kind not in ALLOWED_KINDS:
            kind = "note"
        item = Post(author=author, kind=kind, body=str(body), tags=list(tags or []))
        return self.post_raw(item)

    def post_raw(self, item: Post) -> Post:
        with self._lock:
            self._posts.append(item)
        return item

    def recent(self, n: int = 20, kinds: Optional[Iterable[str]] = None) -> List[Post]:
        allow = set(kinds) if kinds else None
        with self._lock:
            items = list(self._posts)
        if allow:
            items = [p for p in items if p.kind in allow]
        return items[-n:]

    def dump(self, n: int = 50) -> str:
        rows = self.recent(n)
        if not rows:
            return "(empty blackboard)"
        return "\n".join(p.render() for p in rows)

    def __len__(self) -> int:
        with self._lock:
            return len(self._posts)


Handler = Callable[[Blackboard, str], str]


@dataclass
class Member:
    name: str
    instruction: str
    handler: Optional[Handler] = None

    def act(self, board: Blackboard, goal: str) -> str:
        if self.handler is None:
            summary = board.dump(12)
            body = f"{self.instruction}\n\nGoal: {goal}\n\nBoard:\n{summary}"
            board.post(self.name, body[:400], kind="note")
            return body[:200]
        result = self.handler(board, goal)
        board.post(self.name, result, kind="note")
        return result


def _echo_handler(label: str) -> Handler:
    def _fn(board: Blackboard, goal: str) -> str:
        last = board.recent(5)
        hint = last[-1].body[:80] if last else goal
        return f"{label} reviewed '{hint}' and is ready."

    return _fn


DEFAULT_MEMBERS: Dict[str, Member] = {
    "coordinator": Member(
        "coordinator",
        "Keep the board tidy. Restate the goal and assign next focus.",
        _echo_handler("coordinator"),
    ),
    "researcher": Member(
        "researcher",
        "Collect facts relevant to the goal. Prefer tools when an Agent is wired.",
        _echo_handler("researcher"),
    ),
    "operator": Member(
        "operator",
        "Apply workspace changes or confirm none were needed.",
        _echo_handler("operator"),
    ),
}


class Team:
    def __init__(
        self,
        members: Optional[Sequence[Member]] = None,
        board: Optional[Blackboard] = None,
    ) -> None:
        self.board = board or Blackboard()
        self.members: List[Member] = list(members) if members else list(DEFAULT_MEMBERS.values())

    def add(self, member: Member) -> None:
        self.members.append(member)

    def run(self, goal: str, rounds: int = 1) -> str:
        goal = (goal or "").strip() or "(empty goal)"
        self.board.post("system", goal, kind="goal", tags=["team"])
        rounds = max(1, int(rounds))
        for i in range(rounds):
            self.board.post("system", f"round {i + 1}/{rounds}", kind="system")
            for member in self.members:
                member.act(self.board, goal)
        self.board.post("system", "team finished", kind="system", tags=["done"])
        return self.board.dump()

    def status(self) -> str:
        names = ", ".join(m.name for m in self.members) or "(none)"
        return f"members={names} posts={len(self.board)}"


def demo_team(goal: str = "List what this kit can do without a cloud API.") -> str:
    """LLM-free team run used by CLI and tests."""
    team = Team()
    return team.run(goal, rounds=1)
