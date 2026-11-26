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

## [0.82.0] - 2026-11-24

### Added
- Offline MVP now supports compound “create directory and save note” goals: mkdir then write_file inside the new directory.
- New ready-to-run example `examples/ready_local_agent_v082.py` demonstrating mkdir→file + shell→file + list→file + search_files→file + http→file + math→file + verify + system→file + datetime→file + code→file + search→file, fully offline.
- Clearer demo storyboards mentioning directory creation chaining.
- Improved route_intent to detect mkdir / create directory / make folder intents.

### Changed
- Version bump to 0.82.0.
- Offline demos now exercise real sequential mkdir + write_file multi-step plans.
- Docs synced (README, CONTRIBUTING, ROADMAP, HN update, STATUS).

## [0.84.0] - 2026-11-26
- Added `move_file` tool (cwd-safe rename/move).
- New ready_local_agent_v084.py example.
- Updated README, ROADMAP, CONTRIBUTING, docs for v0.84.
