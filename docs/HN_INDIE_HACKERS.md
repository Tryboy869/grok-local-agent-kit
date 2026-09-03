# Launch update — v0.15.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools in parallel, remember notes (JSONL + SQLite cosine, optional Ollama embeddings), load JSON skill packs, fail over from Ollama to LM Studio, speak MCP over stdio/HTTP/SSE, stream thoughts, and dump a JSON trace of every run.

**What's new since v0.14**

- Parallel tool execution in one ReAct turn
- `on_thought` now actually lands in `last_trace` when the model thinks *and* calls tools
- Streamed `on_token` chunks (`kind="stream"`) on the final answer
- `Agent.export_trace()` + `grok-agent trace`
- Ready-to-run `examples/parallel_agent.py` (no live LLM)

**Why now:** Most local-agent repos are prompt wrappers. This one ships a real tool registry, three MCP transports, cwd-safe files, sessions, a fallback router, vector memory that works offline *or* with nomic-embed-text, and an observability hook bus that actually runs.

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
python examples/parallel_agent.py
python examples/sandbox_agent.py
```

**Proof without a GPU:** `pytest -q`, `python examples/hooks_agent.py`, `python examples/skills_agent.py`, `python examples/sandbox_agent.py`, `python examples/embed_agent.py`, `python examples/parallel_agent.py`, `python examples/mcp_agent.py --no-llm`.

**Ask:** What should block 1.0 — sqlite-vec, a PyPI-stable API, or recorded GIFs?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
