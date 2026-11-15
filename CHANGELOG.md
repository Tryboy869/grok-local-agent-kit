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

## [0.72.0] - 2026-11-14

### Added
- Ready local agent demo now uses real offline MVP routing + tools (`run_mvp`) for authentic multi-step plans.
- Improved compound math→file messaging in offline MVP.
- Clearer demo storyboards and provider probe in ready example.
- Updated CONTRIBUTING.md, public ROADMAP, STATUS, and fresh HN / Indie Hackers update draft.

### Changed
- Version bump to 0.72.0.
- Offline demos now exercise the same tool path as the ReAct loop.
- Docs synced.
