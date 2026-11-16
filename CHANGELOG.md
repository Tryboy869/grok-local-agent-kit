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

## [0.73.0] - 2026-11-15

### Added
- Offline MVP now supports a “code” intent that routes to sandboxed `execute_python` (safe local code execution without LLM).
- New ready-to-run example `examples/ready_local_agent_v073.py` demonstrating code + compound plans fully offline.
- Clearer demo storyboards mentioning code execution step.
- Updated CONTRIBUTING.md, public ROADMAP, STATUS, and fresh HN / Indie Hackers update draft.

### Changed
- Version bump to 0.73.0.
- Offline demos now exercise code execution path used by the ReAct loop.
- Docs synced.
