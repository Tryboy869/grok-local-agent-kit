"""v0.45 offline MVP — routing + tools, no network required for the plan."""

from pathlib import Path

from grok_local_agent_kit.mvp import demo_mvp, plan_for, probe_providers, route_intent, run_mvp


def test_intent_routing():
    assert route_intent("compute sqrt(144) + 10") == "math"
    assert route_intent("search local AI agents") == "search"
    assert route_intent("write a note") == "files"
    assert route_intent("call mcp ping") == "mcp"
    assert route_intent("what is the python version") == "system"


def test_run_mvp_writes_file(tmp_path: Path):
    result = run_mvp("write a note for the kit", tmp_path, search=lambda q: "hit")
    assert result["intent"] == "files"
    assert result["ok"] is True
    assert (tmp_path / "mvp_note.txt").read_text(encoding="utf-8").startswith("write a note")
    assert any(step["tool"] == "list_files" for step in result["steps"])


def test_math_and_search_are_injectable(tmp_path: Path):
    math = run_mvp("compute sqrt(144) + 10", tmp_path)
    assert math["intent"] == "math"
    assert "22" in math["answer"]
    web = run_mvp("search local agents", tmp_path, search=lambda q: f"top:{q}")
    assert web["answer"] == "top:search local agents"
    assert plan_for("mcp echo")[0]["tool"] == "mcp_echo"


def test_demo_and_provider_probe(tmp_path: Path):
    text = demo_mvp(tmp_path)
    assert "MVP demo" in text
    assert "ollama" in text and "lmstudio" in text
    report = probe_providers(timeout=0.2)
    assert set(report) == {"ollama", "lmstudio"}
    assert report["ollama"]["status"] in {"up", "down"}
