# Launch update — v0.19.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP, cancel hung shells — and now **watch your workspace, parse JSON out of messy model text, and run TOML recipes with zero LLM**.

**What's new since v0.18**

- `grok-agent watch` — polling file watcher (created / modified / deleted)
- `extract_json()` — first JSON object from fenced or bare model output
- `grok-agent recipe path.toml` — multi-step built-in tools, no GPU
- Examples: `watch_agent.py`, `structured_agent.py`, `recipe_agent.py`
- `tests/test_v019.py` (no live LLM)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
python examples/watch_agent.py
python examples/recipe_agent.py
pytest -q
```

**Ask:** Next blocker for 1.0 — sqlite-vec, recorded GIFs, or a frozen PyPI API?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
