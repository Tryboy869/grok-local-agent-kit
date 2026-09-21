"""Scriptable approval TUI.

Interactive when stdin is a TTY. For tests and CI, pass a decision script
(`A003=approved,A004=denied`) or a bulk policy (`approve-all` / `deny-all`).
No live LLM required.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from .approvals import Approval, ApprovalGate, load_approvals, save_approvals

Decision = Tuple[str, str]


def parse_script(script: str) -> List[Decision]:
    """Parse `A003=approved,A004=denied` (spaces and `:` also accepted)."""
    out: List[Decision] = []
    if not script or not script.strip():
        return out
    for chunk in script.replace(";", ",").split(","):
        piece = chunk.strip()
        if not piece:
            continue
        if "=" in piece:
            key, val = piece.split("=", 1)
        elif ":" in piece:
            key, val = piece.split(":", 1)
        else:
            raise ValueError(f"bad script chunk: {piece!r}")
        status = val.strip().lower()
        if status in {"yes", "y", "ok", "allow"}:
            status = "approved"
        if status in {"no", "n", "block", "reject"}:
            status = "denied"
        if status not in ("approved", "denied"):
            raise ValueError(f"bad status: {val!r}")
        out.append((key.strip(), status))
    return out


def format_queue(gate: ApprovalGate) -> str:
    pending = gate.pending()
    if not pending:
        return "(no pending approvals)"
    lines = ["id     kind      subject            actor         reason"]
    lines.append("-" * 68)
    for item in pending:
        lines.append(
            f"{item.id:<6} {item.kind:<9} {item.subject[:16]:<16} "
            f"{item.actor[:12]:<12} {item.reason[:20]}"
        )
    return "\n".join(lines)


def apply_decisions(
    gate: ApprovalGate,
    decisions: Sequence[Decision],
    decided_by: str = "tui",
) -> List[Approval]:
    applied: List[Approval] = []
    for approval_id, status in decisions:
        applied.append(gate.decide(approval_id, status, decided_by=decided_by))
    return applied


def bulk_decide(gate: ApprovalGate, status: str, decided_by: str = "tui") -> List[Approval]:
    if status not in ("approved", "denied"):
        raise ValueError(status)
    applied: List[Approval] = []
    for item in list(gate.pending()):
        applied.append(gate.decide(item.id, status, decided_by=decided_by))
    return applied


def seed_pending_gate() -> ApprovalGate:
    """A gate with two pending items after policy auto-decides calc/shell."""
    gate = ApprovalGate(allow=["calculator"], deny=["run_shell"], default="pending")
    gate.request("tool", "calculator", actor="researcher", reason="21*2")
    gate.request("tool", "run_shell", actor="operator", reason="echo hi")
    gate.request("tool", "web_search", actor="researcher", reason="local agents")
    gate.request("handoff", "T004", actor="operator", reason="claim write-up")
    return gate


def run_scripted(
    gate: ApprovalGate,
    *,
    script: str = "",
    policy: str = "",
    decided_by: str = "tui",
) -> str:
    """Apply a script or bulk policy and return a dump + summary."""
    applied: List[Approval] = []
    if policy in ("approve-all", "yes-all"):
        applied = bulk_decide(gate, "approved", decided_by=decided_by)
    elif policy in ("deny-all", "no-all"):
        applied = bulk_decide(gate, "denied", decided_by=decided_by)
    elif script:
        applied = apply_decisions(gate, parse_script(script), decided_by=decided_by)
    leftover = gate.pending()
    lines = [format_queue(gate) if leftover else "(queue empty)"]
    if applied:
        lines.append("applied:")
        lines.extend(f"  {a.render()}" for a in applied)
    if leftover:
        lines.append(f"still pending: {len(leftover)}")
    else:
        lines.append("still pending: 0")
    return "\n".join(lines)


def demo_tui() -> str:
    gate = seed_pending_gate()
    header = format_queue(gate)
    body = run_scripted(
        gate,
        script="A003=approved,A004=denied",
        decided_by="human",
    )
    return f"{header}\n---\n{body}\n---\n{gate.dump()}"


def persist_scripted(
    path: str,
    *,
    script: str = "",
    policy: str = "",
    seed: bool = False,
) -> str:
    from pathlib import Path

    if seed or not Path(path).exists():
        gate = seed_pending_gate()
    else:
        gate = load_approvals(path)
    text = run_scripted(gate, script=script, policy=policy, decided_by="tui")
    dest = save_approvals(gate, path)
    return f"{text}\nsaved {dest}"
