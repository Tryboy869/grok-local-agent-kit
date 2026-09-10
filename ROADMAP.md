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

## ✅ v0.17.0

- Optional bearer auth on `grok-agent serve`
- Trace replay (`grok-agent replay`)

## ✅ v0.18.0

- Cancellation tokens that kill hung `run_shell` process groups
- `grok-agent cancel` + `examples/cancel_agent.py`

## ✅ v0.19.0

- Polling workspace watcher (`grok-agent watch`)
- Structured JSON extract from model text
- TOML/JSON tool recipes that run without an LLM

## ✅ v0.20.0

- MCP Streamable HTTP session ids + in-flight request cancellation
- Offline eval harness (`grok-agent eval`)
- `SSEMCPClient` honors `Mcp-Session-Id` and JSON-RPC -32800

## ✅ v0.21.0

- In-process TTL cache for tool results
- Tool latency / hit / error telemetry (offline)
- `grok-agent cache` and `grok-agent telemetry`

## ✅ v0.22.0 (current)

- Tool-call budget (global + per-tool) with CLI `grok-agent budget`
- `retry_call` backoff helper for flaky local backends
- Runtime consumes budget on cache-miss executions

## 🚧 v0.23.x

- sqlite-vec optional backend
- Recorded binary GIFs committed to `docs/gifs/`
- PyPI test publish
- Eval cases against live local models (opt-in)

## 📋 v1.0 — Production ready

- Stable public API + PyPI release
- Vision / multimodal models
- Official docs site

Want something prioritized? Open an issue or PR.
