# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.38.0] — 2026-09-26

### Added
- Persist routed HealthBoard decisions to the same cwd-safe `health.json` the CLI already uses
- `MultiLLMRouter(persist_path=...)`, `attach_persist()`, `persist()` — every `_mark` writes the file
- A second router can hydrate from that file and skip an already-open breaker
- CLI: `grok-agent route persist` (no live LLM)
- Example: `examples/persist_route_agent.py`
- Tests: `tests/test_v038.py`

## [0.37.0] — 2026-09-25

### Added
- Wire `HealthBoard` into `MultiLLMRouter.pick` / `probe` / `chat`
- Open breakers are skipped (no ping). Failures trip the board; successes close it
- Sticky routes drop an endpoint when its breaker opens
- CLI: `grok-agent route demo` (no live LLM)
- Example: `examples/route_health_agent.py`
- Tests: `tests/test_v037.py`

## [0.36.0] — 2026-09-24

### Added
- Circuit breaker health board for local LLM backends (`HealthBoard`, `BreakerState`)
- States: closed / open / half-open with cwd-safe JSON persistence
- CLI: `grok-agent health demo|show|trip|reset` (no live LLM)
- Example: `examples/health_agent.py`
- Tests: `tests/test_v036.py`

## [0.35.0] — 2026-09-22

### Added
- Opt-in live-model eval profile (`live_eval`): stub by default, real LLM only when `GROK_LIVE_EVAL=1` and `--live`
- CLI: `grok-agent eval-live|eval-demo` (does not replace `grok-agent eval`)
- Example: `examples/live_eval_agent.py` + `examples/live_eval_profile.json`
- Tests: `tests/test_v035.py`
