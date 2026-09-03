# Show HN: grok-local-agent-kit 0.15 — local agents with parallel tools and traces

I wanted a small Python kit that runs an agent on my laptop against Ollama or LM Studio without wrapping a cloud API.

v0.15 ships:

- ReAct tool loop (files, web, shell, sandboxed python, calculator, MCP)
- Parallel tool calls in a single turn (`parallel_tools=True`)
- Multi-LLM fallback router (Ollama → LM Studio)
- JSONL memory *and* SQLite vector memory (optional Ollama embeddings)
- `on_thought` + streamed `on_token` hooks
- Trace export to `.grok/traces/`
- JSON skill packs under `.grok/skills/`
- MCP over stdio, HTTP, and SSE with retry
- Tests that do not need a live LLM

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent chat -v --stream --router
python examples/parallel_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Happy to hear what you would require before trusting this in a real workflow.
