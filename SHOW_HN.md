# Show HN: grok-local-agent-kit 0.13 — local agents with vector memory and MCP SSE

I wanted a small Python kit that runs an agent on my laptop against Ollama or LM Studio without wrapping a cloud API.

v0.13 ships:

- ReAct tool loop (files, web, shell, python sandbox, calculator, MCP)
- Multi-LLM fallback router (Ollama → LM Studio)
- JSONL memory *and* SQLite cosine vector memory (no extra deps)
- JSON skill packs under `.grok/skills/`
- Hook bus inside the loop (`before_tool`, `on_token`, `on_final`)
- MCP over stdio, HTTP, and SSE with retry
- MCP prompts/list + prompts/get
- Usage estimator so you can see ~tokens per run
- Tests that do not need a live LLM

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent chat -v --stream --router
python examples/vector_memory_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Happy to hear what you would require before trusting this in a real workflow.
