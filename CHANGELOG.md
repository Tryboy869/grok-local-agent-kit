## [0.81.0] - 2026-11-23

### Added
- Offline MVP now supports compound “run shell command and save” goals: restricted shell output is automatically injected into a subsequent write_file.
- New ready-to-run example `examples/ready_local_agent_v081.py` demonstrating shell→file, list→file, search_files→file, http→file, math→file + verification, system→file, datetime→file, code→file, search→file, and workspace listing — fully offline.
- Clearer demo storyboards mentioning shell-to-file chaining.
- Improved route_intent to detect shell / run command intents.

### Changed
- Version bump to 0.81.0.
- Offline demos now exercise real result injection for run_shell→file multi-step plans.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update, STATUS).

## [0.80.0] - 2026-11-22

### Added
- Offline MVP now supports compound “list files and save” and “search files for X and save” goals: list_files and search_files results are automatically injected into a subsequent write_file.
- New ready-to-run example `examples/ready_local_agent_v080.py` demonstrating list→file, search_files→file, http→file, math→file + verification, system→file, datetime→file, code→file, search→file, and workspace listing — fully offline.
- Clearer demo storyboards mentioning list-to-file and local file search chaining.
- Improved route_intent to distinguish local file search from web search.

### Changed
- Version bump to 0.80.0.
- Offline demos now exercise real result injection for list_files→file and search_files→file multi-step plans.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update, STATUS).

## [0.79.0] - 2026-11-21

### Added
- Offline MVP now supports compound “fetch URL and save” goals: http_get result is automatically injected into a subsequent write_file.
- New ready-to-run example `examples/ready_local_agent_v079.py` demonstrating http→file, math→file + verification, system→file, datetime→file, code→file, search→file, and workspace listing — fully offline.
- Clearer demo storyboards mentioning http-to-file chaining.

### Changed
- Version bump to 0.79.0.
- Offline demos now exercise real result injection for http_get→file multi-step plans.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update).

## [0.78.0] - 2026-11-20

### Added
- Offline MVP now supports improved compound “calculate and save” goals: calculator result is automatically injected into write_file, with optional read-back verification step when the goal mentions “verify” / “read back”.
- New ready-to-run example `examples/ready_local_agent_v078.py` demonstrating math→file + verification, system→file, datetime→file, code→file, search→file, and workspace listing — fully offline.
- Clearer demo storyboards mentioning math-to-file chaining with verification.

### Changed
- Version bump to 0.78.0.
- Offline demos now exercise real result injection for math→file multi-step plans + verification.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update, STATUS).
