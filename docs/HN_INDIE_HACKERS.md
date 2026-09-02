# Launch update — v0.14.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, remember notes (JSONL + SQLite cosine, optional Ollama embeddings), load JSON skill packs, fail over from Ollama to LM Studio, speak MCP over stdio/HTTP/SSE, stream loop thoughts, and run Python in a tighter sandbox.

**What's new since v0.13**

- Optional real embeddings via Ollama `/api/embeddings` (`GROK_EMBED_BACKEND=ollama`) with automatic hash fallback
- `on_thought` hook + thought spans in `last_trace`
- Stronger `execute_python` sandbox (blocked dunders/imports, SIGALRM timeout)
- Ready-to-run `examples/sandbox_agent.py` and `examples/embed_agent.py`
- Demo storyboard at `docs/gifs/README.md`

**Why now:** Most local-agent repos are prompt wrappers. This one ships a real tool registry, three MCP transports, cwd-safe files, sessions, a fallback router, vector memory that works offline *or* with nomic-embed-text, and an observability hook bus that actually runs.

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
python examples/sandbox_agent.py
python examples/embed_agent.py
```

**Proof without a GPU:** `pytest -q`, `python examples/hooks_agent.py`, `python examples/skills_agent.py`, `python examples/sandbox_agent.py`, `python examples/embed_agent.py`, `python examples/mcp_agent.py --no-llm`.

**Ask:** What should block 1.0 — sqlite-vec, a PyPI-stable API, or recorded GIFs?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
