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

## ✅ v0.13.0

- SQLite vector-style memory (hashed bag-of-words + cosine)
- MCP SSE client with reconnect
- MCP prompts/list + prompts/get
- Usage estimator + `on_token` hook

## ✅ v0.14.0 (current)

- Optional real embeddings via Ollama `/api/embeddings` (hash fallback)
- `on_thought` during the tool loop (not only the final answer)
- Stronger sandboxed `execute_python` (timeout + dunder/import guard)
- Demo storyboard in `docs/gifs/`

## 🚧 v0.15.x

- sqlite-vec optional backend
- Token-by-token streaming while tools are still in play
- Recorded binary GIFs committed to `docs/gifs/`
- PyPI test publish

## 📋 v1.0 — Production ready

- Stable public API + PyPI release
- Vision / multimodal models
- Official docs site

Want something prioritized? Open an issue or PR.
