# Launch update — v0.20.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP — now with **Streamable HTTP session ids, request cancellation, and an offline eval harness**.

**What's new since v0.19**

- `MCPSessionRegistry` + `Mcp-Session-Id` on SSE/HTTP client
- Cancel in-flight MCP requests (JSON-RPC `-32800`)
- `grok-agent eval` / `examples/eval_agent.py` — golden tools + JSON extract, no LLM
- `grok-agent mcp-session` to open / list / cancel / close sessions
- `tests/test_v020.py` (no live LLM)

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent eval
python examples/mcp_session_agent.py
pytest -q
```

**Ask:** Next blocker for 1.0 — sqlite-vec, recorded GIFs, or a frozen PyPI API?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
