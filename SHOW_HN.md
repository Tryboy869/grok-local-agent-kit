# Show HN: grok-local-agent-kit 0.14 — local agents with Ollama embeddings and a tighter Python sandbox

I wanted a small Python kit that runs an agent on my laptop against Ollama or LM Studio without wrapping a cloud API.

v0.14 ships:

- ReAct tool loop (files, web, shell, sandboxed python, calculator, MCP)
- Multi-LLM fallback router (Ollama → LM Studio)
- JSONL memory *and* SQLite vector memory
- Optional live embeddings: `GROK_EMBED_BACKEND=ollama` (falls back to hash)
- `on_thought` hook so you can watch the loop think, not only the final answer
- Tighter `execute_python` sandbox (blocked imports, dunders, timeout)
- JSON skill packs under `.grok/skills/`
- MCP over stdio, HTTP, and SSE with retry
- Usage estimator so you can see ~tokens per run
- Tests that do not need a live LLM

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent chat -v --stream --router
python examples/sandbox_agent.py
python examples/embed_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

Happy to hear what you would require before trusting this in a real workflow.
