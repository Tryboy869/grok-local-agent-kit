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

## Shipped (v0.43.0)

- Declarative workflow runner: file ops + injectable web search + MCP echo
- `grok-agent workflow demo|run` and `examples/workflow_agent.py`
- Storyboard for the workflow GIF (`docs/gifs/workflow-demo.md`)

## Shipped (v0.44.0)

- File-backed job ledger: due workflows, injectable clock, `jobs-state.json`
- `grok-agent jobs demo|tick` and `examples/jobs_agent.py`
- Storyboard for the jobs GIF (`docs/gifs/jobs-demo.md`)

## Next (v0.45.x)

- Recorded binary GIFs in docs/gifs/ (storyboards landed in v0.43 and v0.44)
- PyPI / Test PyPI publish
- True vec0 virtual table writes when sqlite-vec is present
- Stronger plugin isolation
- Interactive Rich/prompt toolkit TUI when stdin is a TTY

## v1.0

- Frozen public API + PyPI
- Vision / multimodal models
- Docs site

## Shipped (v0.45.0)

- Offline MVP agent: intent router + file / math / search / system / MCP echo tools
- Provider table + probe for Ollama and LM Studio (demo still runs if both are down)
- `grok-agent mvp`, `examples/mvp_chat.py`, `examples/mvp_automation.py`
- Storyboard `docs/gifs/mvp-demo.md`

## Shipped (v0.46.0)

- Playbook runner sequences chat, math, system, search, and MCP echo without a model
- Optional ReAct handoff descriptor when an injected or live probe is `up` (no chat socket opened)
- `grok-agent playbook demo|run`, `examples/playbook_agent.py`, `examples/playbooks/local_mvp.json`
- Storyboard `docs/gifs/playbook-demo.md`
- HN / Indie Hackers draft `docs/HN_UPDATE_v046.md`

## Shipped (v0.47.0)

- Opt-in ReAct execution: `execute_handoff` runs an injected callable or `Agent.run` when `live=True`
- Scripted path unchanged when no runner is passed (v0.46 tests still pass)
- `grok-agent handoff demo|live`, `examples/handoff_react_agent.py`
- Storyboard `docs/gifs/handoff-demo.md`
- HN / Indie Hackers draft `docs/HN_UPDATE_v047.md`

## Shipped (v0.48.0)

- Session pack batches chat, automation, search, and MCP echo without a model
- `grok-agent pack demo|run`, `examples/session_pack.py`, `examples/packs/local_session.json`
- Brief files: `SESSION.md` and `pack-report.json`
- Storyboard `docs/gifs/pack-demo.md`
- HN / Indie Hackers draft `docs/HN_UPDATE_v048.md`

## Next

- v0.49: record a real VHS GIF from `docs/gifs/pack-demo.md` and publish a 30s demo
- v0.50: MCP stdio attach inside the pack runner (echo stays the default)
- v0.51: stream handoff tokens into the session brief
- PyPI / Test PyPI publish
