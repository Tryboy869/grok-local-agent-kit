# Launch update — v0.12.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, remember notes, load JSON skill packs, fail over from Ollama to LM Studio, and emit real hooks from inside the ReAct loop.

**What's new since v0.11**

- Hooks no longer sit on the sideline — `before_tool` / `after_tool` / `on_final` fire during `agent.run()`
- `Agent.last_trace` for cheap observability
- `remember` / `recall` / `forget` are tools the model can call
- Skill packs: drop `*.json` in `.grok/skills/` and `agent.load_skills()`
- Loop tests that do not need a GPU

**Why now:** Most local-agent repos are prompt wrappers. This one ships a real tool registry, two MCP transports, cwd-safe files, sessions, a fallback router, and an observability hook bus that actually runs.

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
```

**Proof without a GPU:** `pytest -q`, `python examples/hooks_agent.py`, `python examples/skills_agent.py`, `python examples/mcp_agent.py --no-llm`.

**Ask:** What should block 1.0 — full SSE MCP, vector memory, or a PyPI-stable API?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
