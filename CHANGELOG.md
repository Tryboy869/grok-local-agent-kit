# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.21.0] — 2026-09-09

### Added
- In-process TTL tool cache (`ToolCache`, `cached_execute`, `grok-agent cache`)
- Tool telemetry (`Telemetry`, `timed_execute`, `grok-agent telemetry`)
- Runtime wrapper patches `execute_tool` with cache + timing
- Examples: `cache_agent.py`, `telemetry_agent.py`
- Tests in `tests/test_v021.py` (no live LLM)

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

## [0.18.0]
- Cancellation tokens that kill hung `run_shell` process groups

## [0.17.0]
- Bearer auth on `grok-agent serve`, trace replay

## [0.16.0]
- Local HTTP API, planner, guardrails, scheduler
