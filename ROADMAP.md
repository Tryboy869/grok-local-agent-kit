# Roadmap

Public plan for grok-local-agent-kit. Dates slide; the order is the contract.

## Shipped

- v0.16-v0.20: sessions, MCP HTTP/SSE, cancel, eval harness
- v0.21: tool cache + telemetry
- v0.22: tool-call budget + retry helper
- v0.23: optional sqlite-vec + hash fallback
- v0.24: drop-in JSON/Python tool plugins + JSONL transcripts
- v0.25: plugin sandbox
- v0.26: workspace packer + local file RAG
- v0.27: web search HTML fallback
- v0.28: multi-agent Team + shared Blackboard
- v0.29: persist blackboard to JSONL / SQLite
- v0.30: persist team roster + optional per-member LLM bindings
- v0.31: task handoff queue (offer / claim / complete)
- v0.32: local approval gate (HITL for tools + handoff claims)
- v0.33: ApprovalGate wired into the ReAct tool loop (`before_tool` + `gated_execute`)
- v0.34: scriptable approval TUI (`approve tui|queue`)
- v0.35: opt-in live-model eval profile (`eval-demo` / `eval-live`, `GROK_LIVE_EVAL=1`)

## Next (v0.36.x)

- Recorded binary GIFs in docs/gifs/
- PyPI / Test PyPI publish
- True vec0 virtual table writes when sqlite-vec is present
- Stronger plugin isolation
- Interactive Rich/prompt toolkit TUI when stdin is a TTY

## v1.0

- Frozen public API + PyPI
- Vision / multimodal models
- Docs site
