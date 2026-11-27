# Status — grok-local-agent-kit

Current version: **0.85.0** (2026-11-27)

## What works today

- Offline-first MVP with real intent routing (`route_intent` + `run_mvp`) and real tools (no LLM required for demos).
- Compound multi-step plans with result injection: math→file, code→file, search→file, datetime→file, system→file, http_get→file, list_files→file, search_files→file, shell→file, mkdir→file, copy→list, move_file.
- Multi-LLM router with health-aware fallback (Ollama native + OpenAI-compatible / LM Studio).
- MCP (stdio / HTTP / SSE).
- Ready-to-run examples: `mvp_chat_automation.py`, `ready_local_agent_v085.py`, `chat_agent.py`, `automation_agent.py`.
- CLI: `grok-agent doctor`, `grok-agent chat`.
- Tests that run offline.

## Quick verification

```bash
python examples/ready_local_agent_v085.py
python examples/mvp_chat_automation.py
pytest -q
```

All offline demos succeed without network or local model.
