# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.16.0] — 2026-09-04

### Added
- Local HTTP API (`grok-agent serve`, GET `/health`, POST `/v1/chat`) bound to 127.0.0.1 by default
- Workspace planner tools + CLI (`plan_add` / `plan_list` / `plan_done`, `grok-agent plan`)
- Tool guardrails: allow-list, deny-list, per-tool wall-clock timeout (`GROK_AGENT_*`)
- Interval `Scheduler` for automation agents
- Examples: `serve_agent.py`, `planner_agent.py`, `guardrails_agent.py`
- Tests in `tests/test_v016.py` (no live LLM)

### Changed
- Version bump to 0.16.0
- README / roadmap / contributing / HN drafts updated

## [0.15.0] — 2026-09-03

### Added
- Real `on_thought` emission when the model writes a thought *and* calls tools
- Parallel tool execution in a single ReAct turn
- Token-level `on_token` events during streamed final answers
- `Agent.export_trace()` + `grok-agent trace`
- Example `examples/parallel_agent.py`

## [0.14.0] — 2026-09-02

- Optional Ollama embeddings, `on_thought`, stronger execute_python sandbox

## [0.13.0] — 2026-09-01

- SQLite vector memory, MCP SSE + prompts, usage tracker

## [0.12.0] — 2026-08-31

- Live ReAct hooks, memory tools, skill packs, last_trace
