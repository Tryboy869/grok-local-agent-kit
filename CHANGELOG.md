## [0.85.0] - 2026-11-27

### Added
- Real offline MVP core (`grok_local_agent_kit/mvp.py`) with `route_intent` + `run_mvp`.
  Supports compound plans with previous-result injection: shell→file, list→file, search_files→file, http→file, math→file (+verify), code→file, web search→file, system→file, datetime→file, copy→list, mkdir→file, move_file.
- New ready-to-run example `examples/ready_local_agent_v085.py` that exercises the real router and tools fully offline.
- `probe_providers()` for non-blocking Ollama / LM Studio health checks.

### Changed
- Version bump to 0.85.0.
- README, CONTRIBUTING, ROADMAP, STATUS, SHOW_HN and HN update refreshed.
- Offline demos now run real sequential tool execution without any LLM.

## [0.84.0] - 2026-11-26
- Added `move_file` tool (cwd-safe rename/move).
- New ready_local_agent_v084.py example.
- Updated README, ROADMAP, CONTRIBUTING, docs for v0.84.

## [0.83.0] - 2026-11-25

### Added
- Offline MVP now supports compound “create a note and copy it” goals: write_file then copy_file with proper sequencing and result handling.
- New ready-to-run example `examples/ready_local_agent_v083.py` demonstrating copy→list + mkdir→file + shell→file + list→file + search_files→file + http→file + math→file + verify + system→file + datetime→file + code→file + search→file, fully offline.
- Clearer demo storyboards mentioning file copy chaining.
- Improved route_intent to detect copy / duplicate file intents.

### Changed
- Version bump to 0.83.0.
- Offline demos now exercise real sequential write + copy_file multi-step plans.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update, STATUS).
