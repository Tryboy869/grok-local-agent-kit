# Show HN: grok-local-agent-kit — offline-first local agents (Ollama + MCP + HITL tools)

I built a small Python toolkit so you can run capable agents on your machine with no cloud and no API keys for local models.

**What it does**

- Talks to Ollama or LM Studio (OpenAI-compat) with a multi-LLM fallback router
- ReAct tool loop: files, web, shell, calculator, Python sandbox, MCP (stdio / HTTP / SSE)
- A local approval gate now sits on that loop: denied or pending tools never execute
- Web search that still works if the DDG Python package flakes (HTML fallback)
- Workspace packer + local file RAG — no network
- Multi-agent `Team` with a shared blackboard, persisted roster, handoff queue
- Drop-in plugins: JSON tools always load; Python plugins are opt-in only
- Local HTTP API, SQLite memory (optional sqlite-vec), eval harness, budgets, transcripts
- Demos (`tools`, `team`, `roster`, `handoff`, `approve demo|react`) run with **zero** live model

**Try it**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent tools demo
grok-agent approve react
```

Chat needs Ollama or LM Studio:

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
