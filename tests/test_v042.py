"""Offline scripted agent loop — no live LLM."""

from pathlib import Path

from grok_local_agent_kit.offline import ScriptedLLM, demo_offline, run_offline


def test_scripted_lists_then_answers(tmp_path: Path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    out = run_offline("please list files", tmp_path)
    assert "Done (offline)" in out
    assert "a.txt" in out


def test_scripted_write_creates_file(tmp_path: Path):
    out = run_offline("automation: write a note", tmp_path)
    note = tmp_path / "offline-note.txt"
    assert note.is_file()
    assert "written by the offline agent" in note.read_text(encoding="utf-8")
    assert "Done (offline)" in out


def test_demo_offline_mentions_both_paths():
    text = demo_offline()
    assert "chat:" in text
    assert "automation:" in text
    assert "wrote=True" in text


def test_scripted_llm_close():
    llm = ScriptedLLM()
    llm.close()
    assert llm.calls == 0
