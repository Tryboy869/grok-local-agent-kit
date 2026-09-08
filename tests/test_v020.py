"""v0.20 tests — MCP sessions + offline eval. No live LLM."""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit.evalkit import EvalCase, load_cases, run_suite
from grok_local_agent_kit.mcp_session import reset_registry, run_cancellable


def test_session_open_and_header():
    reg = reset_registry()
    sess = reg.open(session_id="abc", server="local")
    assert sess.session_id == "abc"
    assert sess.header()["Mcp-Session-Id"] == "abc"
    assert reg.get("abc") is sess


def test_cancel_inflight():
    reg = reset_registry()
    sess = reg.open()
    reg.begin_request(sess.session_id, "9", "tools/call")
    assert "9" in sess.inflight
    assert reg.cancel_request(sess.session_id, "9") is True
    assert "9" not in sess.inflight
    assert reg.is_cancelled(sess.session_id, "9")


def test_run_cancellable_short_circuits():
    reg = reset_registry()
    sess = reg.open()
    reg.cancel_request(sess.session_id, "1")
    called = {"n": 0}

    def boom() -> str:
        called["n"] += 1
        return "nope"

    out = run_cancellable(sess.session_id, "1", "x", boom)
    assert called["n"] == 0
    assert out["error"]["code"] == -32800


def test_eval_calculator_and_json(tmp_path: Path):
    path = tmp_path / "cases.json"
    path.write_text(
        '{"cases":[{"name":"c","kind":"tool","tool":"calculator",'
        '"args":{"expression":"2+2"},"expect":"4"},'
        '{"name":"j","kind":"json","text":"{\\"a\\":1}","expect":{"a":1}}]}',
        encoding="utf-8",
    )
    report = run_suite(load_cases(path))
    assert report["ok"] is True
    assert report["passed"] == 2


def test_eval_failure():
    report = run_suite([EvalCase(name="bad", kind="equals", input=1, expect=2)])
    assert report["ok"] is False
    assert report["failed"] == 1
