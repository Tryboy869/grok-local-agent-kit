# Launch update — v0.26.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP — now with a cwd-safe workspace packer and file RAG that runs without a network or a live model.

**What's new since v0.25**

- `pack_workspace` summarizes the repo (paths + snippets, skips `.git` / `.venv`)
- `search_workspace` ranks files with local hash embeddings
- `grok-agent workspace pack` / `grok-agent workspace search "query"`
- Example: `python examples/workspace_agent.py`
- Tests: `tests/test_v026.py` (no live LLM)
- File tools still cannot escape the working directory

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/workspace_agent.py
grok-agent workspace pack
grok-agent workspace search "MCP routing"
pytest -q
```

**Ask:** Next blocker for 1.0 — recorded GIFs, PyPI, or subprocess-isolated plugins?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
