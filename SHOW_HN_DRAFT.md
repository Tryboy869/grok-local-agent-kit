# Show HN draft — 2026-10-05

Title (HN limit ~80 chars):

Show HN: grok-local-agent-kit – local agents on Ollama/LM Studio, no API key

Body (copy-paste):

I built an offline-first Python toolkit for local agents. It talks to Ollama and LM Studio (OpenAI-compatible), runs a ReAct tool loop, and can fall back across models with a circuit breaker that survives process restart.

What is in the box today (v0.43):

- CLI `grok-agent`: doctor, chat, tools, model catalog, route, snapshot
- Multi-LLM router that prefers models actually installed on the machine
- MCP over stdio/HTTP/SSE
- Workspace packer + local file RAG (no network)
- Multi-agent team, shared blackboard, roster, handoff queue
- Local approval gate (including a small TUI)
- SQLite memory, optional sqlite-vec, JSONL transcripts, budgets
- Offline eval harness; live-model eval is opt-in
- Drop-in tool plugins; Python plugins are opt-in and sandboxed

Try it:

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent models demo
grok-agent route catalog
```

Chat needs a local model:

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
```

From source: https://github.com/Tryboy869/grok-local-agent-kit

MIT. No cloud account required for the local path. Feedback welcome on the router, the approval gate, and what a minimal MCP recipe should look like.

---

Do not post this more than once. HN buries duplicates.
