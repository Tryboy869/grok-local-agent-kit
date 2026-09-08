# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.20.0] — 2026-09-08

### Added
- MCP Streamable HTTP session registry (`Mcp-Session-Id`, in-flight request cancel, JSON-RPC -32800)
- `SSEMCPClient` now opens a session, echoes server session headers, and honors cancel
- Offline eval harness (`evalkit`, `grok-agent eval`, `examples/eval_agent.py`)
- CLI: `grok-agent mcp-session open|list|cancel|close`
- Examples: `mcp_session_agent.py`, `eval_cases.json`
- Tests: `tests/test_v020.py` (no live LLM)

### Changed
- Version bump to 0.20.0

## [0.19.0] — 2026-09-07

### Added
- Workspace file watcher (`grok_local_agent_kit.watch`, `grok-agent watch`)
- Structured JSON extract (`extract_json`, `grok-agent json-extract`)
- TOML/JSON recipe runner (`load_recipe` / `run_recipe`, `grok-agent recipe`)
- Examples: `watch_agent.py`, `structured_agent.py`, `recipe_agent.py`
- Tests: `tests/test_v019.py`

### Changed
- Version bump to 0.19.0

## [0.18.0] — 2026-09-06

### Added
- `CancelToken` + `ProcessRegistry` (`grok_local_agent_kit.cancel`)
- `run_shell` now uses `Popen` + process groups and **kills children** on timeout or cancel
- Guard timeout signals tracked subprocesses (`cancel_all`)
- CLI: `grok-agent cancel [reason]`
- Example: `examples/cancel_agent.py`
- Tests: `tests/test_v018.py`

### Changed
- Version bump to 0.18.0

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
