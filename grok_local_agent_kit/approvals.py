"""Local human-in-the-loop approval gate.

Agents can request permission before a tool runs or a handoff is claimed.
Decisions persist as JSON under the workspace. Demos need no live LLM.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Callable, Dict, List, Optional, Sequence, Union

from .persist import _safe_path

PathLike = Union[str, Path]
ALLOWED_STATUS = ("pending", "approved", "denied")
Decider = Callable[["Approval"], str]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Approval:
    id: str
    kind: str  # tool | handoff | other
    subject: str
    actor: str = "system"
    reason: str = ""
    status: str = "pending"
    decided_by: str = ""
    ts: str = field(default_factory=_now)
    tags: List[str] = field(default_factory=list)

    def render(self) -> str:
        return f"[{self.status}] {self.id} {self.kind}:{self.subject} actor={self.actor}"


class ApprovalDenied(RuntimeError):
    """Raised when a required approval is denied."""


class ApprovalGate:
    """In-memory gate with optional persist path and auto-allow / deny lists."""

    def __init__(
        self,
        *,
        allow: Optional[Sequence[str]] = None,
        deny: Optional[Sequence[str]] = None,
        default: str = "pending",
        decider: Optional[Decider] = None,
    ) -> None:
        if default not in ("pending", "approved", "denied"):
            raise ValueError(f"bad default: {default}")
        self.allow = {a.strip() for a in (allow or []) if a.strip()}
        self.deny = {a.strip() for a in (deny or []) if a.strip()}
        self.default = default
        self.decider = decider
        self._items: Dict[str, Approval] = {}
        self._lock = Lock()
        self._seq = 0

    def _next_id(self) -> str:
        self._seq += 1
        return f"A{self._seq:03d}"

    def request(
        self,
        kind: str,
        subject: str,
        actor: str = "system",
        reason: str = "",
        tags: Optional[Sequence[str]] = None,
    ) -> Approval:
        subject = subject.strip()
        status = self.default
        if subject in self.deny or f"{kind}:{subject}" in self.deny:
            status = "denied"
        elif subject in self.allow or f"{kind}:{subject}" in self.allow:
            status = "approved"
        with self._lock:
            item = Approval(
                id=self._next_id(),
                kind=kind.strip() or "other",
                subject=subject or "(untitled)",
                actor=actor,
                reason=reason,
                status=status,
                decided_by="policy" if status != "pending" else "",
                tags=list(tags or []),
            )
            self._items[item.id] = item
        if item.status == "pending" and self.decider is not None:
            decision = self.decider(item)
            if decision not in ("approved", "denied"):
                raise ValueError(f"decider returned {decision!r}")
            self.decide(item.id, decision, decided_by="decider")
        return self._items[item.id]

    def require(self, kind: str, subject: str, **kwargs) -> Approval:
        item = self.request(kind, subject, **kwargs)
        if item.status == "denied":
            raise ApprovalDenied(item.render())
        if item.status == "pending":
            raise ApprovalDenied(f"pending approval required: {item.render()}")
        return item

    def decide(self, approval_id: str, status: str, decided_by: str = "human") -> Approval:
        if status not in ("approved", "denied"):
            raise ValueError(status)
        with self._lock:
            item = self._items.get(approval_id)
            if item is None:
                raise KeyError(approval_id)
            item.status = status
            item.decided_by = decided_by
            item.ts = _now()
            return item

    def pending(self) -> List[Approval]:
        with self._lock:
            return [a for a in self._items.values() if a.status == "pending"]

    def all_items(self) -> List[Approval]:
        with self._lock:
            return list(self._items.values())

    def dump(self) -> str:
        rows = self.all_items()
        if not rows:
            return "(empty approval gate)"
        return "\n".join(a.render() for a in rows)

    def load_items(self, items: Sequence[Approval]) -> None:
        with self._lock:
            self._items = {a.id: a for a in items}
            self._seq = 0
            for a in items:
                try:
                    n = int(a.id.lstrip("Aa"))
                except ValueError:
                    n = 0
                if n > self._seq:
                    self._seq = n


def save_approvals(gate: ApprovalGate, path: PathLike) -> Path:
    dest = _safe_path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "allow": sorted(gate.allow),
        "deny": sorted(gate.deny),
        "default": gate.default,
        "items": [asdict(a) for a in gate.all_items()],
    }
    dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return dest


def load_approvals(path: PathLike) -> ApprovalGate:
    src = _safe_path(path)
    if not src.exists():
        return ApprovalGate()
    data = json.loads(src.read_text(encoding="utf-8"))
    gate = ApprovalGate(
        allow=data.get("allow") or [],
        deny=data.get("deny") or [],
        default=data.get("default") or "pending",
    )
    items = []
    for row in data.get("items") or []:
        items.append(
            Approval(
                id=str(row.get("id") or "A000"),
                kind=str(row.get("kind") or "other"),
                subject=str(row.get("subject") or ""),
                actor=str(row.get("actor") or "system"),
                reason=str(row.get("reason") or ""),
                status=str(row.get("status") or "pending"),
                decided_by=str(row.get("decided_by") or ""),
                ts=str(row.get("ts") or _now()),
                tags=list(row.get("tags") or []),
            )
        )
    gate.load_items(items)
    return gate


def demo_approvals() -> str:
    gate = ApprovalGate(allow=["calculator", "list_files"], deny=["shell"], default="pending")
    gate.request("tool", "calculator", actor="researcher", reason="21*2")
    gate.request("tool", "shell", actor="operator", reason="rm -rf /")
    pending = gate.request("handoff", "T002", actor="researcher", reason="claim research")
    gate.decide(pending.id, "approved", decided_by="human")
    return gate.dump()
