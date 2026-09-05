# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.17.0] — 2026-09-05

### Added
- Optional bearer token for `grok-agent serve` (`--token` / `GROK_AGENT_SERVE_TOKEN`)
- Health JSON now includes `"auth": true|false`; `/health` stays public
- Trace replay module + CLI: `grok-agent replay`, `replay_file()`, `examples/replay_agent.py`
- Tests in `tests/test_v017.py` (no live LLM)

### Changed
- Version bump to 0.17.0
- README / roadmap / contributing / HN drafts updated

## [0.16.0] — 2026-09-04

### Added
- Local HTTP API (`grok-agent serve`, GET `/health`, POST `/v1/chat`) bound to 127.0.0.1 by default
- Workspace planner tools + CLI
- Tool guardrails: allow-list, deny-list, per-tool wall-clock timeout
- Interval `Scheduler` for automation agents
- Examples: `serve_agent.py`, `planner_agent.py`, `guardrails_agent.py`
- Tests in `tests/test_v016.py` (no live LLM)

## [0.15.0] — 2026-09-03

- Parallel tools, `on_thought`, `export_trace()`

## [0.14.0] — 2026-09-02

- Optional Ollama embeddings, stronger execute_python sandbox
