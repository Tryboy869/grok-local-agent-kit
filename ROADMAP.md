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
- v0.36: circuit breaker health board for Ollama / LM Studio (`health demo|show|trip|reset`)
- v0.37: HealthBoard wired into MultiLLMRouter.pick / probe / chat (`route demo`)
- v0.38: persist routed health decisions onto `health.json` (`route persist`)
- v0.39: portable kit snapshot (`snapshot demo|show|write`)
- v0.40: local model catalog (`models demo|list|refresh`, `catalog.json`)
- v0.41: wire catalog.pick into MultiLLMRouter defaults (`route catalog`)
- v0.42: offline scripted agent loop (`offline demo`, chat + automation examples)
- v0.43: declarative workflow runner (files + search + MCP, no daemon)
- v0.58: enhanced core agent example with polished routing & multi-tool chain, docs & HN update
- v0.60: refined math routing extraction + docs/HN sync
- v0.61: improved math routing (** power, better extraction) + docs/HN sync
- v0.62: compound intent routing (math + save to file) + ready_compound_agent example + docs/HN sync

## Next

- Record real VHS GIFs for core / chat / automation / multi-tool / compound demos
- MCP stdio attach inside the pack runner
- Stream handoff tokens into the session brief
- PyPI / Test PyPI publish
- Stronger plugin isolation and optional interactive TUI
- Community recipes and skill packs
- Better multi-step chaining and natural-language plan extraction in the offline core
