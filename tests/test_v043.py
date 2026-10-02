"""Declarative workflow runner — no live LLM, no network."""

from pathlib import Path

from grok_local_agent_kit.workflow import demo_workflow, load_workflow, run_workflow


def test_workflow_files_search_and_mcp(tmp_path: Path):
    (tmp_path / "seed.txt").write_text("seed", encoding="utf-8")
    spec = {
        "name": "unit",
        "steps": [
            {"tool": "list_files", "arguments": {"path": "."}, "save_as": "listing"},
            {"tool": "write_file", "arguments": {"path": "out.txt", "content": "from {{listing}}\n"}},
            {"tool": "web_search", "arguments": {"query": "local"}},
            {"tool": "mcp_call", "arguments": {"name": "echo", "arguments": {"q": "ping"}}},
            {"tool": "read_file", "arguments": {"path": "out.txt"}},
        ],
    }
    result = run_workflow(spec, tmp_path, search=lambda q: f"hit:{q}")
    assert result["ok"] is True
    assert result["steps"] == 5
    assert "seed.txt" in (tmp_path / "out.txt").read_text(encoding="utf-8")
    assert any(item["tool"] == "web_search" and "hit:local" in item["output"] for item in result["trace"])
    assert any('"tool": "echo"' in item["output"] for item in result["trace"])


def test_workflow_blocks_path_escape(tmp_path: Path):
    spec = {"name": "escape", "steps": [{"tool": "read_file", "arguments": {"path": "../secret"}}]}
    result = run_workflow(spec, tmp_path)
    assert result["ok"] is False
    assert "escapes" in (result["trace"][0]["error"] or "")


def test_load_and_demo(tmp_path: Path):
    spec = tmp_path / "flow.json"
    spec.write_text(
        '{"name":"disk","steps":[{"tool":"note","arguments":{"text":"hi"}}]}',
        encoding="utf-8",
    )
    loaded = load_workflow(spec)
    result = run_workflow(loaded, tmp_path)
    assert result["ok"] is True
    text = demo_workflow(tmp_path / "demo")
    assert "workflow=mvp-routing-tools" in text
    assert "wrote=True" in text
    assert (tmp_path / "demo" / "automation-note.txt").is_file()
