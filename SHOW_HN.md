# Show HN: grok-local-agent-kit — offline-first local agents (Ollama + MCP + team handoff)

I built a small Python toolkit so you can run capable agents on your machine with no cloud and no API keys for local models.

**What it does**

- Talks to Ollama or LM Studio (OpenAI-compat) with a multi-LLM fallback router
- ReAct tool loop: files, web, shell, calculator, Python sandbox, MCP (stdio / HTTP / SSE)
- Web search that still works if the DDG Python package flakes (HTML fallback)
- Workspace packer + local file RAG — no network
- Multi-agent `Team` with a shared blackboard
- Persist the board **and** the roster (who is on the team, optional model bindings)
- Local handoff queue: offer / claim / complete tasks without a hosted job system
- Drop-in plugins: JSON tools always load; Python plugins are opt-in only
- Local HTTP API, SQLite memory (optional sqlite-vec), eval harness, budgets, transcripts
- `grok-agent tools demo` / `team demo` / `roster demo` / `handoff demo` run with **zero** live model

**Try it**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent team demo
grok-agent roster demo
grok-agent handoff demo
```

Chat needs Ollama or LM Studio:

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
