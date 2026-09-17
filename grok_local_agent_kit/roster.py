"""Persist a Team roster and optionally bind members to a local LLM.

The roster is JSON (or a SQLite table next to a board). Bindings are opt-in:
without --llm / bind_roster(), handlers stay the LLM-free echo defaults so
tests and `grok-agent roster demo` never need Ollama.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Union

from .persist import _safe_path
from .team import DEFAULT_MEMBERS, Blackboard, Handler, Member, Team

PathLike = Union[str, Path]


@dataclass
class MemberSpec:
    """Serializable member description. Handler callables are never stored."""

    name: str
    instruction: str
    provider: str = ""
    model: str = ""
    role: str = ""
    tags: List[str] = field(default_factory=list)

    def to_member(self, handler: Optional[Handler] = None) -> Member:
        return Member(
            name=self.name,
            instruction=self.instruction,
            handler=handler,
            provider=self.provider,
            model=self.model,
            role=self.role or self.name,
        )


def specs_from_team(team: Team) -> List[MemberSpec]:
    return [
        MemberSpec(
            name=m.name,
            instruction=m.instruction,
            provider=getattr(m, "provider", "") or "",
            model=getattr(m, "model", "") or "",
            role=getattr(m, "role", "") or m.name,
        )
        for m in team.members
    ]


def default_specs() -> List[MemberSpec]:
    return [
        MemberSpec(name=m.name, instruction=m.instruction, role=m.name)
        for m in DEFAULT_MEMBERS.values()
    ]


def save_roster(specs: Sequence[MemberSpec], path: PathLike) -> Path:
    dest = _safe_path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "members": [asdict(s) for s in specs]}
    suffix = dest.suffix.lower()
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        conn = sqlite3.connect(str(dest))
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS roster (
                    name TEXT PRIMARY KEY,
                    instruction TEXT NOT NULL,
                    provider TEXT,
                    model TEXT,
                    role TEXT,
                    tags TEXT
                )
                """
            )
            conn.execute("DELETE FROM roster")
            conn.executemany(
                "INSERT INTO roster (name, instruction, provider, model, role, tags) VALUES (?, ?, ?, ?, ?, ?)",
                [(s.name, s.instruction, s.provider, s.model, s.role, ",".join(s.tags)) for s in specs],
            )
            conn.commit()
        finally:
            conn.close()
        return dest
    dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return dest


def load_roster(path: PathLike) -> List[MemberSpec]:
    src = _safe_path(path)
    if not src.exists():
        return default_specs()
    suffix = src.suffix.lower()
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        conn = sqlite3.connect(str(src))
        try:
            try:
                rows = conn.execute(
                    "SELECT name, instruction, provider, model, role, tags FROM roster"
                ).fetchall()
            except sqlite3.OperationalError:
                return default_specs()
        finally:
            conn.close()
        specs = []
        for name, instruction, provider, model, role, tags in rows:
            specs.append(
                MemberSpec(
                    name=name,
                    instruction=instruction,
                    provider=provider or "",
                    model=model or "",
                    role=role or name,
                    tags=[t for t in (tags or "").split(",") if t],
                )
            )
        return specs or default_specs()
    data = json.loads(src.read_text(encoding="utf-8"))
    members = data.get("members") if isinstance(data, dict) else data
    specs = []
    for row in members or []:
        specs.append(
            MemberSpec(
                name=str(row.get("name") or "member"),
                instruction=str(row.get("instruction") or ""),
                provider=str(row.get("provider") or ""),
                model=str(row.get("model") or ""),
                role=str(row.get("role") or row.get("name") or ""),
                tags=list(row.get("tags") or []),
            )
        )
    return specs or default_specs()


def team_from_roster(
    path: PathLike | None = None,
    board: Optional[Blackboard] = None,
    specs: Optional[Sequence[MemberSpec]] = None,
) -> Team:
    if specs is None:
        specs = load_roster(path) if path else default_specs()
    members = [s.to_member() for s in specs]
    return Team(members=members, board=board)


LLMFactory = Callable[[MemberSpec], object]


def _default_llm_handler(spec: MemberSpec, factory: Optional[LLMFactory]) -> Handler:
    def _fn(board: Blackboard, goal: str) -> str:
        context = board.dump(12)
        prompt = (
            f"You are {spec.name} ({spec.role or spec.name}).\n"
            f"{spec.instruction}\n\nGoal: {goal}\n\nBoard:\n{context}\n\n"
            "Reply in one short paragraph. Do not invent tools that are not on the board."
        )
        if factory is None:
            return f"{spec.name} would call {spec.provider or 'local'}/{spec.model or 'default'}: {goal[:80]}"
        agent = factory(spec)
        run = getattr(agent, "run", None)
        if callable(run):
            return str(run(prompt))
        return str(agent)

    return _fn


def bind_roster(
    specs: Sequence[MemberSpec],
    factory: Optional[LLMFactory] = None,
    live: bool = False,
) -> List[Member]:
    """Attach handlers. If live is False, keep echo-style stubs (tests)."""
    members: List[Member] = []
    for spec in specs:
        if live and (spec.provider or spec.model or factory):
            handler = _default_llm_handler(spec, factory)
        else:
            handler = None
        members.append(spec.to_member(handler=handler))
    return members


def format_roster(specs: Sequence[MemberSpec]) -> str:
    if not specs:
        return "(empty roster)"
    lines = []
    for s in specs:
        bind = f" provider={s.provider}" if s.provider else ""
        model = f" model={s.model}" if s.model else ""
        lines.append(f"- {s.name} [{s.role or s.name}]{bind}{model}: {s.instruction[:80]}")
    return "\n".join(lines)
