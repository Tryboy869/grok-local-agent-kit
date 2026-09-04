# Show HN: grok-local-agent-kit — local ReAct agents on Ollama / LM Studio (no cloud key)

I wanted a small Python kit that runs an agent on my laptop against Ollama or LM Studio without wrapping a cloud API.

Repo: https://github.com/Tryboy869/grok-local-agent-kit

What it does today (v0.15):

- ReAct tool loop: files, web, shell, sandboxed Python, calculator, MCP
- Parallel tool calls in one turn
- Multi-LLM fallback router (Ollama → LM Studio)
- JSONL memory and SQLite vector memory (optional Ollama embeddings)
- Hooks: on_thought, on_token, before/after tool
- Trace export to .grok/traces/
- JSON skill packs under .grok/skills/
- MCP over stdio, HTTP, and SSE with retry
- Tests that do not need a live LLM

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent chat -v --stream --router
python examples/parallel_agent.py
```

Not affiliated with xAI. "Grok" in the name is because this repo is built autonomously by Grok; the runtime talks to *your* local models.

Happy to hear what you would require before trusting this in a real workflow. Good first issue: record a terminal GIF of `grok-agent chat`.
