## [0.75.0] - 2026-11-17

### Added
- Offline MVP now supports compound “search / lookup and save the results” goals: web_search result is automatically injected into a subsequent write_file.
- Improved natural-language plan extraction for multi-step compound goals.
- New ready-to-run example `examples/ready_local_agent_v075.py` demonstrating datetime, math, code, **code→file**, **search→file**, system info, and compound plans — fully offline.
- Clearer demo storyboards mentioning search-to-file chaining.
- Updated CONTRIBUTING.md, public ROADMAP, STATUS, and fresh HN / Indie Hackers update draft.

### Changed
- Version bump to 0.75.0.
- Offline demos now exercise real result injection for search→file multi-step plans.
- Docs synced.

## [0.74.0] - 2026-11-16

### Added
- Offline MVP now supports compound “code → file” goals: sandboxed `execute_python` result is automatically injected into a subsequent `write_file`.
- New ready-to-run example `examples/ready_local_agent_v074.py` demonstrating datetime, math, code, **code→file**, system info, and compound plans — fully offline.
- Clearer demo storyboards mentioning code-to-file chaining.
- Updated CONTRIBUTING.md, public ROADMAP, STATUS, and fresh HN / Indie Hackers update draft.

### Changed
- Version bump to 0.74.0.
- Offline demos now exercise real result injection for multi-step plans.
- Docs synced.
