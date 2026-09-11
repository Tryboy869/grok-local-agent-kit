# Launch update — v0.23.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP — now with an **optional sqlite-vec** memory backend that falls back to hashed cosine so a laptop without extra wheels still works.

**What's new since v0.22**

- `GROK_VEC_BACKEND=auto|hash|sqlite-vec`
- `sqlite_vec_store.knn` / `describe` + hash fallback
- `grok-agent vec info|search|remember`
- Example: `examples/sqlite_vec_agent.py`
- Tests: `tests/test_v023.py` (no live LLM)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
pip install -e ".[vec]"   # optional
grok-agent doctor && grok-agent vec info
python examples/sqlite_vec_agent.py
pytest -q
```

**Ask:** Next blocker for 1.0 — recorded GIFs, a frozen PyPI API, or live-model evals?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
