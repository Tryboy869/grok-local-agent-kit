"""v0.39 — portable kit snapshot."""

from pathlib import Path

from grok_local_agent_kit.snapshot import (
    collect,
    demo_snapshot,
    format_snapshot,
    load_snapshot,
    write_snapshot,
)


def test_collect_has_version_and_tools():
    snap = collect()
    assert snap.version
    assert isinstance(snap.tools, list)
    assert snap.python
    data = snap.to_dict()
    assert "created_at" in data
    text = format_snapshot(snap)
    assert "kit-snapshot" in text
    assert snap.version in text


def test_write_and_load(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dest = write_snapshot("kit-snapshot.json")
    assert dest.exists()
    loaded = load_snapshot(dest)
    assert loaded["version"]
    assert "tools" in loaded
    assert loaded["files"]["health.json"] is False


def test_demo_snapshot(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    text = demo_snapshot("kit-snapshot.json")
    assert "wrote=" in text
    assert "kit-snapshot" in text
    assert Path("kit-snapshot.json").exists()
