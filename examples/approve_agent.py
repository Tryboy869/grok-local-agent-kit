#!/usr/bin/env python3
"""Offline demo: approval gate for tools + handoff claims."""

from grok_local_agent_kit.approvals import (
    ApprovalDenied,
    ApprovalGate,
    save_approvals,
)
from grok_local_agent_kit.handoff import HandoffQueue


def main() -> None:
    gate = ApprovalGate(allow=["calculator"], deny=["shell"], default="pending")
    q = HandoffQueue()
    task = q.offer("summarize workspace", owner="coordinator")

    calc = gate.require("tool", "calculator", actor="researcher")
    print("allowed:", calc.render())

    try:
        gate.require("tool", "shell", actor="operator")
    except ApprovalDenied as exc:
        print("blocked:", exc)

    req = gate.request("handoff", task.id, actor="researcher", reason="claim")
    print("pending claim:", req.render())
    gate.decide(req.id, "approved", decided_by="human")
    gate.require("handoff", task.id, actor="researcher")
    q.claim(task.id, "researcher")
    print(q.dump())
    print("---")
    print(gate.dump())
    save_approvals(gate, "approvals.json")
    print("saved approvals.json")


if __name__ == "__main__":
    main()
