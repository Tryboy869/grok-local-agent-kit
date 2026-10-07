"""v0.46 playbook — sequenced MVP goals, handoff stays offline unless probe is up."""

import json
from pathlib import Path

import pytest

from grok_local_agent_kit.playbook import (
    builtin_playbook,
    demo_playbook,
    handoff_plan,
    load_playbook,
    run_playbook,
)


def test_playbook_runs_every_intent(tmp_path: Path):
    report = run_playbook(
        builtin_playbook(),
        tmp_path,
        probes={"ollama": {"status": "down"}, "lmstudio": {"status": "down"}},
    )
    intents = [step["intent"] for step in report["steps"]]
    assert intents == ["files", "math", "system", "search", "mcp"]
    assert report["ok"] is True
    assert report["handoff_mode"] == "scripted"
    assert (tmp_path / "mvp_note.txt").exists()
    saved = json.loads((tmp_path / "playbook-report.json").read_text(encoding="utf-8"))
    assert saved["name"] == "local-mvp"
    assert "22" in saved["steps"][1]["answer"]


def test_handoff_when_provider_up():
    plan = handoff_plan(
        "compute sqrt(144) + 10",
        {"ollama": {"status": "up", "model": "llama3.2"}, "lmstudio": {"status": "down"}},
    )
    assert plan["mode"] == "react"
    assert plan["provider"] == "ollama"
    assert plan["base_url"].startswith("http://127.0.0.1:11434")
    assert plan["model"] == "llama3.2"


def test_lmstudio_handoff_if_ollama_down():
    plan = handoff_plan(
        "search local agents",
        {"ollama": {"status": "down"}, "lmstudio": {"status": "up"}},
    )
    assert plan["provider"] == "lmstudio"
    assert "1234" in plan["base_url"]


def test_load_playbook_rejects_empty(tmp_path: Path):
    path = tmp_path / "bad.json"
    path.write_text('{"name": "x", "steps": []}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_playbook(path)


def test_demo_mentions_chat_and_mcp(tmp_path: Path):
    text = demo_playbook(
        tmp_path,
        probes={"ollama": {"status": "down"}, "lmstudio": {"status": "down"}},
    )
    assert "intent=math" in text
    assert "intent=mcp" in text
    assert "handoff=scripted" in text
