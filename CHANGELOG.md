# Changelog

All notable changes to grok-local-agent-kit are documented here.

## [0.28.0] — 2026-09-15

### Added
- Multi-agent `Team` + thread-safe `Blackboard` (goal / note / claim / artifact posts)
- CLI: `grok-agent team demo|status` (no live LLM)
- Example: `examples/team_agent.py` (`--llm` optional)
- Tests: `tests/test_v028.py`

### Changed
- Public exports: `Team`, `Blackboard`, `Member`, `demo_team`
- README / ROADMAP / Show HN copy for v0.28

## [0.27.0] — 2026-09-14

### Added
- Robust web search (`websearch.search_web`) — duckduckgo-search with DuckDuckGo HTML fallback
- CLI: `grok-agent tools list|demo` (no live LLM)
- Example: `examples/tools_demo_agent.py`
- Tests: `tests/test_v027.py`

### Changed
- `tools.web_search` now delegates to the fallback pipeline
- README: 1-command install, demo storyboard, examples table

## [0.26.0] — 2026-09-13

### Added
- Workspace packer (`pack_workspace`) — cwd-safe file list + snippets
- Local file RAG (`search_workspace`) — ranks files with hash embeddings (no network)
- CLI: `grok-agent workspace pack|search`
- Example: `examples/workspace_agent.py`
- Tests: `tests/test_v026.py` (no live LLM)
