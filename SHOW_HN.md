# Show HN: grok-local-agent-kit v0.21 — local agents with a tool cache

I keep building a Python kit for **offline-first agents** that talk to Ollama or LM Studio, call real tools, and speak MCP.

v0.21 adds what I actually needed while looping an agent on the same calculator / file-read calls:

- TTL cache so identical tool calls are free
- Offline telemetry (latency, hits, errors) with `grok-agent telemetry`
- Still no cloud, no API keys for local models

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
python examples/cache_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
