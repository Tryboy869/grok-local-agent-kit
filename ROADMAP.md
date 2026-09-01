# Public Roadmap — grok-local-agent-kit

## ✅ v0.6–0.9 — foundation

- ReAct agent, multi-LLM, tools, MCP stdio, sessions

## ✅ v0.10.0

- Multi-LLM fallback router, JSONL memory, orchestrator

## ✅ v0.11.0

- File-based config (`grok-agent.toml`)
- Event hooks on the agent
- MCP HTTP JSON-RPC (minimal POST)

## ✅ v0.12.0

- Hooks actually fire inside the ReAct loop
- Memory tools + skill packs
- `last_trace` for observability
- Fake-LLM loop tests

## ✅ v0.13.0 (current)

- SQLite vector-style memory (hashed bag-of-words + cosine)
- MCP SSE client with reconnect
- MCP prompts/list + prompts/get
- Usage estimator + `on_token` hook

## 🚧 v0.14.x

- Optional real embeddings (ollama `/api/embeddings` or sqlite-vec)
- Token streaming of tool-loop thought tokens, not only the final answer
- Stronger sandboxed `execute_python`
- Recorded README GIFs in `docs/gifs/`

## 📋 v1.0 — Production ready

- Stable public API + PyPI release
- Vision / multimodal models
- Official docs site

Want something prioritized? Open an issue or PR.
