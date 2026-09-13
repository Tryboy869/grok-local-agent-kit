"""v0.26 workspace packer + file RAG — no live LLM."""

from __future__ import annotations

from grok_local_agent_kit.workspace import pack_workspace, search_workspace


def test_pack_workspace_lists_this_tree(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Hello kit\nlocal agents")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("def main():\n    return 42\n")
    out = pack_workspace(".")
    assert "README.md" in out
    assert "app.py" in out
    assert "Hello kit" in out


def test_search_workspace_ranks_relevant_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "notes.md").write_text("Ollama local LLM routing and MCP tools")
    (tmp_path / "unrelated.txt").write_text("bananas and grocery lists")
    out = search_workspace("ollama mcp routing", path=".", top_k=2)
    assert "notes.md" in out
    assert "score=" in out


def test_refuses_path_outside_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    out = pack_workspace("/tmp")
    assert "error" in out.lower() or "outside" in out.lower()
