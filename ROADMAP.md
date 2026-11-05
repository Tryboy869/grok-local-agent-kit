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
- v0.33: ApprovalGate wired into the ReAct tool loop
- v0.34: scriptable approval TUI
- v0.35: opt-in live-model eval profile
- v0.36: circuit breaker health board
- v0.37: HealthBoard wired into MultiLLMRouter
- v0.38: persist routed health
- v0.39: portable kit snapshot
- v0.40: local model catalog
- v0.41: catalog.pick into router defaults
- v0.42: offline scripted agent loop
- v0.43: declarative workflow runner
- v0.58–v0.62: enhanced core, refined math routing, compound intent routing + ready examples
- v0.63: polished offline MVP example (chat + automation), clearer README demos
- v0.64: refined offline core + polished chat/automation examples + docs refresh

## Next

- Record real VHS GIFs for MVP / chat / automation / multi-tool / compound demos
- MCP stdio attach inside the pack runner
- Stream handoff tokens into the session brief
- PyPI / Test PyPI publish
- Stronger plugin isolation and optional interactive TUI
- Community recipes and skill packs
- Better multi-step chaining and natural-language plan extraction in the offline core
