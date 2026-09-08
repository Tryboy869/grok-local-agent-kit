# Show HN: grok-local-agent-kit 0.20 — MCP session ids + offline eval

I keep shipping a small Python kit for **offline-first agents** on Ollama / LM Studio.

v0.20 adds the MCP glue that was missing:

- Streamable HTTP **session ids** (`Mcp-Session-Id`) on `SSEMCPClient`
- Cancel an in-flight JSON-RPC request (`-32800`)
- `grok-agent eval` — golden calculator / JSON cases with **no GPU**

Still in the box: file watcher, recipes, cancel hung shells, bearer token on `grok-agent serve`, router, planner, guardrails.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent eval
python examples/mcp_session_agent.py
pytest -q
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
