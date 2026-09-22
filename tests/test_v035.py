import json
from pathlib import Path

from grok_local_agent_kit.live_eval import (
    DEFAULT_PROFILE,
    LiveCase,
    LiveProfile,
    format_live_report,
    live_enabled,
    load_profile,
    run_profile,
    stub_complete,
)


def test_stub_scores_default_profile():
    report = run_profile(DEFAULT_PROFILE, live=False)
    assert report["backend"] == "stub"
    assert report["ok"] is True
    assert report["passed"] == 2
    text = format_live_report(report)
    assert "echo-ok" in text and "PASS" in text


def test_live_requires_env_and_flag(monkeypatch):
    monkeypatch.delenv("GROK_LIVE_EVAL", raising=False)
    assert live_enabled(True) is False
    monkeypatch.setenv("GROK_LIVE_EVAL", "1")
    assert live_enabled(False) is False
    assert live_enabled(True) is True


def test_custom_complete_and_fail():
    profile = LiveProfile(
        name="custom",
        cases=[LiveCase(name="need-xyz", prompt="hi", contains="xyz")],
    )
    report = run_profile(profile, complete=lambda _p: "nope")
    assert report["ok"] is False
    assert report["results"][0]["error"]


def test_stub_complete_json():
    case = LiveCase(name="j", prompt="x", json_key="status", contains="ready")
    out = stub_complete("x", case)
    assert json.loads(out)["status"] == "ready"


def test_load_profile_roundtrip(tmp_path: Path):
    dest = tmp_path / "p.json"
    dest.write_text(
        json.dumps(
            {
                "name": "file",
                "cases": [{"name": "a", "prompt": "say OK", "contains": "OK"}],
            }
        ),
        encoding="utf-8",
    )
    profile = load_profile(dest)
    assert profile.name == "file"
    report = run_profile(profile, live=False)
    assert report["ok"] is True
