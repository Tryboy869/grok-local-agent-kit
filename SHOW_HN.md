# Show HN: grok-local-agent-kit — offline-first local agents with MCP, budgets, and retries

Show HN: grok-local-agent-kit – offline-first agents for Ollama / LM Studio

I built a Python toolkit so you can run capable agents on your machine without a cloud API key.

What it does today (v0.22):

- Talks to Ollama or any OpenAI-compatible local server (LM Studio)
- ReAct tool loop: files, shell, calculator, web, Python sandbox, MCP
- Multi-LLM fallback router if one backend is down
- MCP over stdio / HTTP / SSE with session ids and cancel
- Local HTTP API, recipes, workspace watcher, offline eval harness
- Tool-result cache + telemetry (no network)
- Tool-call budget so a ReAct loop cannot spin 200 times
- Retry with backoff for flaky local backends

Install:

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/budget_agent.py
```

Or: `pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git`

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Not affiliated with xAI. Local models only unless you point it at a compatible endpoint.
