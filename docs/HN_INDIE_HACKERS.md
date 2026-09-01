# Launch update — v0.13.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, remember notes (JSONL + SQLite cosine), load JSON skill packs, fail over from Ollama to LM Studio, speak MCP over stdio/HTTP/SSE, and emit real hooks from inside the ReAct loop.

**What's new since v0.12**

- Vector-style memory with hashed bag-of-words embeddings in SQLite — `vremember` / `vrecall`, no extra package
- MCP SSE client with exponential backoff (`SSEMCPClient`, `grok-agent mcp-sse URL`)
- MCP prompts (`prompts/list`, `prompts/get`)
- `agent.usage.summary()` token/call estimator
- `on_token` hook for the final answer

**Why now:** Most local-agent repos are prompt wrappers. This one ships a real tool registry, three MCP transports, cwd-safe files, sessions, a fallback router, vector-ish memory that works offline, and an observability hook bus that actually runs.

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
python examples/vector_memory_agent.py
```

**Proof without a GPU:** `pytest -q`, `python examples/hooks_agent.py`, `python examples/skills_agent.py`, `python examples/vector_memory_agent.py`, `python examples/mcp_agent.py --no-llm`.

**Ask:** What should block 1.0 — real embeddings, a PyPI-stable API, or a tighter sandbox?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
