# Launch update — v0.16.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools in parallel, remember notes, load JSON skill packs, fail over from Ollama to LM Studio, speak MCP over stdio/HTTP/SSE, stream thoughts, dump a JSON trace, keep a workspace plan, enforce tool allow/deny + timeouts, and expose a loopback HTTP API.

**What's new since v0.15**

- `grok-agent serve` — GET `/health`, POST `/v1/chat` on 127.0.0.1
- Planner tools + `grok-agent plan` writing `.grok/plan.json`
- Guardrails: `GROK_AGENT_ALLOW_TOOLS`, `GROK_AGENT_DENY_TOOLS`, `GROK_AGENT_TOOL_TIMEOUT`
- Interval `Scheduler` for automation examples
- Ready-to-run `examples/serve_agent.py`, `planner_agent.py`, `guardrails_agent.py` (no live LLM)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
python examples/serve_agent.py
python examples/planner_agent.py
```

**Proof without a GPU:** `pytest -q` plus the examples above.

**Ask:** What should block 1.0 — sqlite-vec, bearer auth on serve, a PyPI-stable API, or recorded GIFs?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
