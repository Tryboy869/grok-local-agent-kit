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
- v0.44-v0.49: session pack, playbook, handoff ReAct call, core MVP demos
- v0.50: enhanced offline core + ready-to-run examples
- v0.51: clean core MVP agent example + docs polish
- v0.52: smarter offline intent routing (regex math detection + expanded keywords)
- v0.53: more robust math expression extraction in offline MVP router
- v0.54: multi-LLM docs polish + ready-to-run chat/automation examples + GIF storyboards + HN update
- v0.55: enhanced core agent routing + new ready-to-run core_agent_demo.py + GIF storyboard + HN update

## Next

- v0.56: record real VHS GIFs for core demos
- v0.56: MCP stdio attach inside the pack runner
- v0.57: stream handoff tokens into the session brief
- PyPI / Test PyPI publish
- Stronger plugin isolation and optional interactive TUI
- Community recipes and skill packs
