# Show HN: grok-local-agent-kit 0.17 — local agents with tool traces you can replay

I keep shipping a small Python kit for **offline-first agents** on Ollama / LM Studio.

v0.17 adds two things people actually asked for after the HTTP API landed:

1. Optional bearer token on `grok-agent serve` (loopback still default; `/health` stays public).
2. Replay of `export_trace()` JSON — summarize or re-run the tool calls **without a live model**. That makes CI and demos cheap.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/replay_agent.py --run
```

Stack: ReAct loop, parallel tools, MCP stdio/HTTP/SSE, SQLite vector memory, planner, guardrails, scheduler.

Repo: https://github.com/Tryboy869/grok-local-agent-kit
