# Launch update — v0.10.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that actually call tools, speak MCP, remember notes, and fail over from Ollama to LM Studio.

**Why now:** Most local-agent repos are prompt wrappers. This one ships a real tool registry, a stdio MCP client, cwd-safe files, sessions, and a fallback router you can probe with one CLI command.

**Install**

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor && grok-agent route
```

**Proof without a GPU:** `pytest -q` and `python examples/mcp_agent.py --no-llm` / `python examples/memory_agent.py`.

**Ask:** What should block 1.0 — HTTP MCP, vector memory, or a PyPI-stable API?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
