# Launch update — v0.22.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP — now with a **tool-call budget** so a ReAct loop cannot melt your laptop, plus a tiny retry helper for flaky local backends.

**What's new since v0.21**

- `ToolBudget` — global cap + per-tool caps (`GROK_AGENT_MAX_TOOL_CALLS`)
- Runtime consumes budget on cache-miss executions (cached hits stay free)
- `retry_call` — exponential backoff, injectable sleeper (easy to test)
- `grok-agent budget stats|reset|on|off|set --max N`
- Examples: `budget_agent.py`, `retry_agent.py`
- `tests/test_v022.py` (no live LLM)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent eval
python examples/budget_agent.py
python examples/retry_agent.py
pytest -q
```

**Ask:** Next blocker for 1.0 — sqlite-vec, recorded GIFs, or a frozen PyPI API?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
