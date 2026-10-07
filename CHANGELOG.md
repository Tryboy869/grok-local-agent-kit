## [0.46.0] - 2026-10-07

### Added
- Playbook runner (`run_playbook`, `load_playbook`) sequences the offline MVP: files, math, system, search, MCP echo.
- Handoff descriptor: `mode=react` when Ollama or LM Studio probe is up; `mode=scripted` otherwise. No chat socket is opened.
- CLI: `grok-agent playbook demo` and `grok-agent playbook run PATH`.
- Examples: `examples/playbook_agent.py`, `examples/playbooks/local_mvp.json`.
- Tests: `tests/test_v046.py` (injected probes, no network).
- GIF storyboard `docs/gifs/playbook-demo.md`.
- HN / Indie Hackers draft `docs/HN_UPDATE_v046.md`.

## [0.45.0] - 2026-10-06

### Added
- Offline MVP runner: intent routing (files, math, search, system, MCP echo) plus the shared tool registry.
- Multi-LLM provider table for Ollama (`:11434`) and LM Studio (`:1234/v1`) with a non-fatal probe.
- `grok-agent mvp`, `examples/mvp_chat.py`, `examples/mvp_automation.py`.
- GIF storyboard `docs/gifs/mvp-demo.md`.

# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.43.0] — 2026-10-02

### Added
- Declarative workflow runner (`Workflow`, `run_workflow`, `load_workflow`) — file ops, injectable web search, MCP echo
- Offline demo chains a chat-style list, an automation write, a search fixture, and an MCP call (no daemon)
- CLI: `grok-agent workflow demo` and `grok-agent workflow run PATH`
- Example: `examples/workflow_agent.py` and `examples/workflows/mvp.json`
- Tests: `tests/test_v043.py` (cwd-safe paths, no network)
- GIF storyboard in `docs/gifs/workflow-demo.md` (binary capture still optional)
- HN / Indie Hackers update draft in `docs/HN_INDIE_HACKERS.md`

## [0.42.0] — 2026-10-01

### Added
- Offline scripted agent loop (`ScriptedLLM`, `run_offline`, `demo_offline`)
- CLI: `grok-agent offline demo`
- Examples: `examples/offline_chat_agent.py`, `examples/offline_automation_agent.py`
- Tests: `tests/test_v042.py`

## [0.41.0] — 2026-09-30

### Added
- Wire `Catalog.pick()` into `MultiLLMRouter` endpoint models (`apply_catalog`)
- Offline demo `demo_catalog_route()` — placeholder models become discovered names
- CLI: `grok-agent route catalog`
- Example: `examples/catalog_route_agent.py`
- Tests: `tests/test_v041.py`

## [0.40.0] — 2026-09-28

### Added
- Local model catalog for Ollama (`/api/tags`) and LM Studio (`/v1/models`)
- Injectable HTTP fetch so CI never contacts a live daemon
- Persist `catalog.json`; `Catalog.pick()` prefers a name prefix
- CLI: `grok-agent models demo|list|refresh`
- Example: `examples/catalog_agent.py`
- Tests: `tests/test_v040.py`

## [0.39.0] — 2026-09-27

### Added
- Portable kit snapshot (`Snapshot`, `collect`, `write_snapshot`, `load_snapshot`)
- Captures version, Python, platform, default tools, and presence of health/roster/board/config files
- CLI: `grok-agent snapshot demo|show|write` (no live LLM)
- Example: `examples/snapshot_agent.py`
- Tests: `tests/test_v039.py`

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
