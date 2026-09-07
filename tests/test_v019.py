"""v0.19 tests — watcher, structured JSON, recipes. No live LLM."""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit.recipes import load_recipe, run_recipe
from grok_local_agent_kit.structured import extract_json, extract_json_or_none, require_keys
from grok_local_agent_kit.watch import diff, snapshot


def test_snapshot_and_diff(tmp_path: Path):
    (tmp_path / "a.txt").write_text("one", encoding="utf-8")
    s1 = snapshot(tmp_path)
    (tmp_path / "a.txt").write_text("two two", encoding="utf-8")
    (tmp_path / "b.txt").write_text("new", encoding="utf-8")
    s2 = snapshot(tmp_path)
    events = {e.path: e.kind for e in diff(s1, s2)}
    assert events["a.txt"] == "modified"
    assert events["b.txt"] == "created"


def test_extract_fenced_json():
    text = 'prefix\n```json\n{"ok": true, "n": 3}\n```\nsuffix'
    assert extract_json(text) == {"ok": True, "n": 3}


def test_extract_bare_object():
    assert extract_json('answer is {"x": 1} done') == {"x": 1}


def test_extract_or_none():
    assert extract_json_or_none("not json") is None


def test_require_keys():
    require_keys({"a": 1, "b": 2}, ["a"])
    try:
        require_keys({"a": 1}, ["b"])
        raise AssertionError("expected ValueError")
    except ValueError as exc:
        assert "missing" in str(exc)


def test_recipe_runs_calculator(tmp_path: Path):
    path = tmp_path / "r.toml"
    path.write_text(
        'name = "math"\n\n[[steps]]\ntool = "calculator"\nexpression = "3*7"\n',
        encoding="utf-8",
    )
    recipe = load_recipe(path)
    results = run_recipe(recipe)
    assert results[0]["output"] == "21"
