# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.31.0] — 2026-09-18

### Added
- Task handoff queue (`HandoffQueue`, `Task`, `save_queue` / `load_queue`)
- Offer / claim / complete / drop with optional Blackboard mirror
- JSON + SQLite persistence (cwd-safe)
- CLI: `grok-agent handoff demo|show` (no live LLM)
- Example: `examples/handoff_agent.py`
- Tests: `tests/test_v031.py`

### Changed
- README features heading aligned to current version
- Public exports for handoff helpers

## [0.30.0] — 2026-09-17

### Added
- Persist team roster to JSON or SQLite (`save_roster` / `load_roster`)
- Optional per-member LLM bindings (`provider` + `model`, `bind_roster`)
- CLI: `grok-agent roster demo|show` (no live LLM unless `--llm`)
- Example: `examples/roster_agent.py`
- Tests: `tests/test_v030.py`

## [0.29.0] — 2026-09-16

### Added
- Persist team blackboard to JSONL or SQLite (`save_board` / `load_board`)
- CLI: `grok-agent board demo|show` (no live LLM)
- Example: `examples/persist_agent.py`
- Tests: `tests/test_v029.py`
- `Blackboard.post_raw` so reloads keep original timestamps

### Changed
- Public exports: `save_board`, `load_board`
- README / ROADMAP / Show HN copy for v0.29

## [0.28.0] — 2026-09-15

### Added
- Multi-agent `Team` + thread-safe `Blackboard` (goal / note / claim / artifact posts)
- CLI: `grok-agent team demo|status` (no live LLM)
- Example: `examples/team_agent.py` (`--llm` optional)
- Tests: `tests/test_v028.py`

## [0.27.0] — 2026-09-14

### Added
- Robust web search (`websearch.search_web`) — duckduckgo-search with DuckDuckGo HTML fallback
- CLI: `grok-agent tools list|demo` (no live LLM)
- Example: `examples/tools_demo_agent.py`
- Tests: `tests/test_v027.py`
