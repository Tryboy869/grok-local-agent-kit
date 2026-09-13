# Show HN: grok-local-agent-kit — offline-first local agents (Ollama + MCP + workspace RAG)

I built a small Python toolkit so you can run capable agents on your machine with no cloud and no API keys for local models.

**What it does**

- Talks to Ollama or LM Studio (OpenAI-compat) with a multi-LLM fallback router
- ReAct tool loop: files, web, shell, calculator, Python sandbox, MCP (stdio / HTTP / SSE)
- Workspace packer + local file RAG (`pack_workspace`, `search_workspace`) — no network
- Drop-in plugins: JSON tools always load; Python plugins are opt-in only
- Local HTTP API, SQLite memory (optional sqlite-vec), transcripts, eval harness, telemetry + budgets

**Why I made it**

Most agent frameworks assume the cloud. I wanted something you can `pip install`, point at a local model, and use the same day — including MCP tools and a workspace search that works offline.

**Try it**

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent workspace pack
grok-agent chat -v --stream --router
```

Or:

```
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
ollama pull llama3.2
pytest -q
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Happy to hear what breaks first.
