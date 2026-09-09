# Launch update — v0.21.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP — now with a **TTL tool cache and offline telemetry** so repeated tool calls are free and measurable.

**What's new since v0.20**

- `ToolCache` + `cached_execute` — hash(name, args), TTL, max size, enable/disable
- `Telemetry` + `timed_execute` — per-tool latency, cache hits, errors
- `grok-agent cache` / `grok-agent telemetry`
- Runtime wraps `execute_tool` so existing agents pick this up automatically
- `tests/test_v021.py` (no live LLM)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent eval
python examples/cache_agent.py
python examples/telemetry_agent.py
pytest -q
```

**Ask:** Next blocker for 1.0 — sqlite-vec, recorded GIFs, or a frozen PyPI API?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
