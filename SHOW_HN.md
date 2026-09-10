# Show HN: grok-local-agent-kit v0.22 — local agents with a tool-call budget

I keep building a Python kit for **offline-first agents** that talk to Ollama or LM Studio, call real tools, and speak MCP.

v0.22 adds what I needed after a ReAct loop tried the same tool 200 times:

- Tool-call budget (global + per-tool) via `grok-agent budget`
- Retry helper with backoff for flaky local backends
- Still no cloud, no API keys for local models

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
python examples/budget_agent.py
python examples/retry_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
