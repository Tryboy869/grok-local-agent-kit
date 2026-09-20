"""Process-wide ApprovalGate used by the execute_tool runtime wrap."""

from __future__ import annotations

from typing import Optional

from .approvals import ApprovalGate

_GATE: Optional[ApprovalGate] = None


def get_gate() -> Optional[ApprovalGate]:
    return _GATE


def set_gate(gate: Optional[ApprovalGate]) -> Optional[ApprovalGate]:
    global _GATE
    _GATE = gate
    return _GATE


def reset_gate() -> None:
    global _GATE
    _GATE = None
