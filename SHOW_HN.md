# Show HN: grok-local-agent-kit 0.16 — local agents with a loopback HTTP API

I wanted a small Python kit that runs an agent on my laptop against Ollama or LM Studio without wrapping a cloud API.

v0.16 ships:

- ReAct tool loop (files, web, shell, sandboxed python, calculator, MCP)
- Parallel tool calls in a single turn
- Multi-LLM fallback router (Ollama → LM Studio)
- JSONL memory *and* SQLite vector memory (optional Ollama embeddings)
- `on_thought` + streamed `on_token` hooks + JSON traces
- JSON skill packs under `.grok/skills/`
- MCP over stdio, HTTP, and SSE with retry
- Local HTTP API: `grok-agent serve` then `POST /v1/chat`
- Workspace planner (`plan_add` / `plan_list` / `plan_done`)
- Tool allow/deny lists and per-tool timeouts
- Tests that do not need a live LLM

```bash
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
grok-agent doctor
grok-agent serve --port 8765
curl -s -X POST http://127.0.0.1:8765/v1/chat -H 'content-type: application/json' -d '{"prompt":"What files are here?"}'
python examples/planner_agent.py
python examples/serve_agent.py
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
