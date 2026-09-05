# Public Roadmap — grok-local-agent-kit

## ✅ v0.6–0.15 — foundation through traces

- ReAct agent, multi-LLM router, tools, MCP stdio/HTTP/SSE
- JSONL + SQLite vector memory, optional Ollama embeddings
- Hooks, skills, orchestrator, parallel tools, trace export

## ✅ v0.16.0

- Local HTTP API (`grok-agent serve`)
- Workspace planner tools + CLI
- Tool allow/deny lists and per-tool timeouts
- Interval scheduler for automation examples

## ✅ v0.17.0 (current)

- Optional bearer auth on `grok-agent serve` (`--token` / `GROK_AGENT_SERVE_TOKEN`)
- Trace replay (`grok-agent replay`, `replay_file`, `examples/replay_agent.py`)
- Health endpoint reports whether auth is enabled
- Tests in `tests/test_v017.py` (no live LLM)

## 🚧 v0.18.x

- sqlite-vec optional backend
- Recorded binary GIFs committed to `docs/gifs/`
- PyPI test publish
- Cancellation tokens that actually kill hung subprocesses

## 📋 v1.0 — Production ready

- Stable public API + PyPI release
- Vision / multimodal models
- Official docs site

Want something prioritized? Open an issue or PR.
