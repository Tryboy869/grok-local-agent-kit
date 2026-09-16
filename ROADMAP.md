# Roadmap

Public plan for grok-local-agent-kit. Dates slide; the order is the contract.

## Shipped

- v0.16-v0.20: sessions, MCP HTTP/SSE, cancel, eval harness
- v0.21: tool cache + telemetry
- v0.22: tool-call budget + retry helper
- v0.23: optional sqlite-vec + hash fallback
- v0.24: drop-in JSON/Python tool plugins + JSONL transcripts
- v0.25: plugin sandbox — Python plugins opt-in / allowlist only
- v0.26: workspace packer + local file RAG (`pack_workspace`, `search_workspace`)
- v0.27: web search HTML fallback + LLM-free `grok-agent tools demo`
- v0.28: multi-agent `Team` + shared `Blackboard` (`grok-agent team demo`)
- v0.29: persist blackboard to JSONL / SQLite (`grok-agent board demo`)

## Next (v0.30.x)

- Recorded binary GIFs in `docs/gifs/`
- PyPI test publish
- Opt-in live-model eval profile
- True vec0 virtual table writes when sqlite-vec is present
- Stronger plugin isolation (subprocess / restricted builtins)
- Optional per-member LLM binding on a persisted board

## v1.0

- Frozen public API + PyPI
- Vision / multimodal models
- Docs site

Want something moved up? Open an issue.
