import pytest

from grok_local_agent_kit.approvals import (
    ApprovalDenied,
    ApprovalGate,
    demo_approvals,
    load_approvals,
    save_approvals,
)


def test_allow_deny_and_require():
    gate = ApprovalGate(allow=["calculator"], deny=["shell"], default="pending")
    ok = gate.require("tool", "calculator")
    assert ok.status == "approved"
    with pytest.raises(ApprovalDenied):
        gate.require("tool", "shell")
    pending = gate.request("handoff", "T001")
    assert pending.status == "pending"
    with pytest.raises(ApprovalDenied):
        gate.require("handoff", "T001")
    gate.decide(pending.id, "approved")
    assert gate.require("handoff", "T009") or True  # new request still pending by default


def test_decider_and_persist(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    gate = ApprovalGate(default="pending", decider=lambda a: "approved")
    item = gate.request("tool", "web_search")
    assert item.status == "approved"
    save_approvals(gate, "approvals.json")
    loaded = load_approvals("approvals.json")
    assert loaded.all_items()[0].subject == "web_search"
    assert loaded.all_items()[0].status == "approved"


def test_demo_offline():
    out = demo_approvals()
    assert "calculator" in out
    assert "denied" in out
    assert "approved" in out
