# Show HN draft — copy-paste (2026-10-09)

Title:

Show HN: grok-local-agent-kit – local AI agents on Ollama/LM Studio (session pack, no cloud)

Body:

I built an offline-first Python toolkit for local agents. It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, and can fall back across models with a circuit breaker that survives restart.

What is in the box today (v0.48):

- `grok-agent pack demo` runs chat math, a file write, a search fixture, and MCP echo, then writes SESSION.md — no model
- `grok-agent playbook demo` and `grok-agent handoff demo` still run offline; live handoff is opt-in
- CLI: `grok-agent doctor`, chat, tools, model catalog, health-aware router
- MCP over stdio / HTTP / SSE
- Workspace packer + local file RAG (no network)
- Multi-agent team, shared blackboard, handoff queue
- Local approval gate (denied tools never run) and a scriptable TUI
- JSON workflows and a file-backed job ledger that runs them offline
- Optional SQLite memory, eval harness, budgets, JSONL transcripts

No API key is required for local models. Demos that do not chat (`doctor`, `pack demo`, `playbook demo`, `mvp`, `tools demo`) run without a model.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent pack demo
grok-agent mvp
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
