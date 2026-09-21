from pathlib import Path

from grok_local_agent_kit.approve_tui import (
    apply_decisions,
    demo_tui,
    format_queue,
    parse_script,
    persist_scripted,
    run_scripted,
    seed_pending_gate,
)
from grok_local_agent_kit.approvals import load_approvals


def test_parse_script_aliases():
    assert parse_script("A003=yes, A004:no") == [
        ("A003", "approved"),
        ("A004", "denied"),
    ]


def test_seed_has_two_pending():
    gate = seed_pending_gate()
    pending = {a.id: a.subject for a in gate.pending()}
    assert pending == {"A003": "web_search", "A004": "T004"}
    table = format_queue(gate)
    assert "A003" in table and "web_search" in table


def test_scripted_drain():
    gate = seed_pending_gate()
    apply_decisions(gate, [("A003", "approved"), ("A004", "denied")], decided_by="test")
    assert gate.pending() == []
    items = {a.id: a.status for a in gate.all_items()}
    assert items["A003"] == "approved"
    assert items["A004"] == "denied"


def test_bulk_and_demo():
    gate = seed_pending_gate()
    text = run_scripted(gate, policy="approve-all")
    assert "still pending: 0" in text
    assert "approved" in demo_tui()


def test_persist_roundtrip(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dest = Path("approvals.json")
    out = persist_scripted(str(dest), script="A003=approved,A004=denied", seed=True)
    assert dest.exists()
    assert "still pending: 0" in out
    loaded = load_approvals(dest)
    assert loaded.pending() == []
    by_id = {a.id: a.status for a in loaded.all_items()}
    assert by_id["A003"] == "approved"
    assert by_id["A004"] == "denied"
