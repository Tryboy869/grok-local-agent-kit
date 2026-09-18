from grok_local_agent_kit.handoff import (
    HandoffQueue,
    demo_handoff,
    load_queue,
    save_queue,
)
from grok_local_agent_kit.team import Blackboard


def test_offer_claim_complete(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    board = Blackboard()
    q = HandoffQueue(board=board)
    a = q.offer("write tests", owner="lead")
    q.claim(a.id, "ops")
    q.complete(a.id, note="done")
    assert q.all_tasks()[0].status == "done"
    assert q.all_tasks()[0].assignee == "ops"
    assert len(board) >= 3


def test_queue_json_and_sqlite(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    q = HandoffQueue()
    q.offer("persist me")
    save_queue(q, "handoff.json")
    loaded = load_queue("handoff.json")
    assert loaded.all_tasks()[0].title == "persist me"
    save_queue(q, "handoff.sqlite")
    loaded2 = load_queue("handoff.sqlite")
    assert loaded2.all_tasks()[0].title == "persist me"


def test_demo_handoff_offline():
    out = demo_handoff("no cloud")
    assert "no cloud" in out
    assert "done" in out
    assert "researcher" in out or "T00" in out
