"""v0.17 tests — no live LLM required."""

from __future__ import annotations

import json
from pathlib import Path

from grok_local_agent_kit.replay import load_trace, replay_tools, summarize_trace
from grok_local_agent_kit.serve import _extract_bearer, make_handler
from grok_local_agent_kit.tools import calculator, search_files


def test_calculator_still_works():
    assert calculator("2 + 2") == "4"


def test_search_files_finds_this_test(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "sample.py").write_text("def hello_v017():\n    return 1\n", encoding="utf-8")
    out = search_files("hello_v017", path=".", pattern="*.py")
    assert "hello_v017" in out


def test_extract_bearer():
    assert _extract_bearer("Bearer secret-token") == "secret-token"
    assert _extract_bearer("secret-token") == "secret-token"


def test_replay_trace_roundtrip(tmp_path):
    trace = [
        {"type": "thought", "text": "I will add 2+2"},
        {"type": "tool", "name": "calculator", "arguments": {"expression": "2+2"}},
    ]
    p = tmp_path / "trace.json"
    p.write_text(json.dumps(trace), encoding="utf-8")
    loaded = load_trace(p)
    assert len(loaded) == 2
    summary = summarize_trace(loaded)
    assert "calculator" in summary
    results = replay_tools(loaded, dry_run=False)
    assert results[0]["ok"] is True
    assert results[0]["output"] == "4"


def test_make_handler_exports():
    Handler = make_handler(lambda: None, token="abc")
    assert Handler is not None
