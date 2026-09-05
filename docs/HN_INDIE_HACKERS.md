# Launch update — v0.17.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools in parallel, remember notes, load JSON skill packs, fail over from Ollama to LM Studio, speak MCP over stdio/HTTP/SSE, stream thoughts, dump a JSON trace, **replay that trace without a model**, keep a workspace plan, enforce tool allow/deny + timeouts, and expose a loopback HTTP API **with optional bearer auth**.

**What's new since v0.16**

- `GROK_AGENT_SERVE_TOKEN` / `grok-agent serve --token` — 401 on `/v1/chat` if missing, `/health` stays public
- `grok-agent replay` + `examples/replay_agent.py` — summarize or re-run tool calls from `export_trace()`
- `tests/test_v017.py` — calculator, file search, bearer parse, replay round-trip (no GPU)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
python examples/replay_agent.py --run
python examples/serve_agent.py
```

**Proof without a GPU:** `pytest -q` plus the examples above.

**Ask:** What should block 1.0 — sqlite-vec, a PyPI-stable API, recorded GIFs, or killing hung `run_shell` processes?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
