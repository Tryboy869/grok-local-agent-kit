"""Helpers that wire ApprovalGate into the ReAct tool loop."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .approvals import ApprovalDenied, ApprovalGate
from .hooks import HookBus


def check_tool(gate: ApprovalGate, name: str, actor: str = "agent", reason: str = "") -> str:
    """Require approval for a tool. Returns empty string if allowed.

    Denied / still-pending tools raise ApprovalDenied (caller turns that
    into a tool-result string so the ReAct loop can continue).
    """
    gate.require("tool", name, actor=actor, reason=reason)
    return ""


def tool_block_message(exc: BaseException) -> str:
    return f"blocked by approval gate: {exc}"


def attach_approval_gate(
    hooks: HookBus,
    gate: ApprovalGate,
    *,
    actor: str = "agent",
) -> HookBus:
    """Register a before_tool listener that enforces the gate."""

    def _before_tool(*, name: str, args: Dict[str, Any], **_: Any) -> None:
        reason = ""
        if isinstance(args, dict) and args:
            reason = ",".join(f"{k}={v}" for k, v in list(args.items())[:4])
        check_tool(gate, name, actor=actor, reason=reason)

    hooks.on("before_tool", _before_tool)
    return hooks


def gated_execute(
    gate: Optional[ApprovalGate],
    name: str,
    runner,
    *args: Any,
    **kwargs: Any,
) -> str:
    """Run ``runner`` only if the gate allows ``name``. Offline-friendly."""
    if gate is not None:
        try:
            check_tool(gate, name)
        except ApprovalDenied as exc:
            return tool_block_message(exc)
    return runner(*args, **kwargs)
