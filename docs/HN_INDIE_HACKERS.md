# Launch update — v0.11.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, speak MCP (stdio + HTTP), remember notes, fail over from Ollama to LM Studio, and expose hooks you can log or audit.

**What's new since v0.10**

- `grok-agent.toml` / JSON config (`grok-agent init`)
- Event hooks: `before_tool`, `after_tool`, `on_final`
- `HTTPMCPClient` + `grok-agent mcp-http <url>`
- One-line install script

**Why now:** Most local-agent repos are prompt wrappers. This one ships a real tool registry, two MCP transports, cwd-safe files, sessions, a fallback router, and an observability hook bus.

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
```

**Proof without a GPU:** `pytest -q`, `python examples/hooks_agent.py`, `python examples/mcp_agent.py --no-llm`.

**Ask:** What should block 1.0 — full SSE MCP, vector memory, or a PyPI-stable API?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
