"""v0.47 — call the ReAct handoff when mode is react (injected, no network)."""

from pathlib import Path

from grok_local_agent_kit.playbook import (
    builtin_playbook,
    demo_react,
    execute_handoff,
    run_playbook,
    scripted_react,
)


def test_scripted_mode_does_not_call_react(tmp_path: Path):
    seen = []

    def react(plan):
        seen.append(plan)
        return "should-not-run"

    report = run_playbook(
        builtin_playbook(),
        tmp_path,
        probes={"ollama": {"status": "down"}, "lmstudio": {"status": "down"}},
        react=react,
    )
    assert report["react_called"] == 0
    assert seen == []
    assert all(step["react"]["executed"] is False for step in report["steps"])


def test_react_callable_runs_when_provider_up(tmp_path: Path):
    report = run_playbook(
        builtin_playbook(),
        tmp_path,
        probes={"ollama": {"status": "up", "model": "llama3.2"}, "lmstudio": {"status": "down"}},
        react=scripted_react,
    )
    assert report["handoff_mode"] == "react"
    assert report["react_called"] == 5
    assert report["steps"][1]["react"]["answer"].startswith("[react-scripted] ollama")
    assert "sqrt" in report["steps"][1]["react"]["answer"]


def test_descriptor_only_when_no_runner():
    plan = {"mode": "react", "provider": "ollama", "prompt": "hi", "reason": "provider probe is up"}
    result = execute_handoff(plan)
    assert result["executed"] is False
    assert "descriptor only" in result["reason"]


def test_injected_failure_is_reported():
    def boom(_plan):
        raise RuntimeError("model busy")

    result = execute_handoff(
        {"mode": "react", "provider": "ollama", "prompt": "hi"},
        react=boom,
    )
    assert result["executed"] is False
    assert "model busy" in result["error"]


def test_demo_react_mentions_called(tmp_path: Path):
    text = demo_react(tmp_path)
    assert "react=called" in text
    assert "handoff=react" in text
