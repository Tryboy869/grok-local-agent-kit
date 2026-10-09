"""v0.48 — session pack batches offline MVP goals (no network)."""

import json
from pathlib import Path

from grok_local_agent_kit.pack import DEFAULT_GOALS, demo_pack, load_pack, run_pack


def test_pack_routes_chat_automation_search_mcp(tmp_path: Path):
    report = run_pack(DEFAULT_GOALS, tmp_path, search=lambda q: f"hit:{q}")
    intents = [item["intent"] for item in report["results"]]
    assert intents == ["math", "files", "search", "mcp"]
    assert report["ok"] is True
    assert report["goals"] == 4
    assert (tmp_path / "mvp_note.txt").is_file()
    assert "sqrt" in report["results"][0]["answer"] or "22" in report["results"][0]["answer"]
    assert (tmp_path / "pack-report.json").is_file()
    assert "Session pack" in (tmp_path / "SESSION.md").read_text(encoding="utf-8")
    saved = json.loads((tmp_path / "pack-report.json").read_text(encoding="utf-8"))
    assert saved["providers"]["ollama"]["status"] == "not-probed"


def test_load_pack_rejects_empty(tmp_path: Path):
    path = tmp_path / "empty.json"
    path.write_text('{"goals": []}', encoding="utf-8")
    try:
        load_pack(path)
    except ValueError as exc:
        assert "no goals" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_demo_pack_text(tmp_path: Path):
    text = demo_pack(tmp_path)
    assert "chat" in text
    assert "automation" in text
    assert "not-probed" in text
