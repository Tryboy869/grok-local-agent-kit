## [0.63.0] - 2026-11-01

### Added
- New ready-to-run offline MVP example: `examples/mvp_chat_automation.py` (chat + automation via intent routing + real tools, no LLM required).
- Clearer demo storyboards in README (GIFs described; record with VHS from docs/gifs).
- HN/Indie Hackers update draft for v0.63.0.

### Changed
- README quick-start and examples section refreshed for the MVP surface.
- Version bump to 0.63.0.

## [0.62.0] - 2026-10-29

### Added
- Compound intent routing in offline MVP core: detect math + "save/write to file" and chain calculator → write_file (result injected into the file).
- Read-file intent for simple "read X.txt" goals.
- New ready-to-run example: `examples/ready_compound_agent.py` — demonstrates math→file chaining + read-back, fully offline.
- Version bump to 0.62.0 with README, ROADMAP, and HN/Indie Hackers update.

### Changed
- `run_mvp` now passes real calculator output into subsequent write steps for compound plans.
- More robust multi-step tool plans without requiring a live LLM.

## [0.61.0] - 2026-10-27

### Added
- Improved math routing in offline MVP core: better support for power operators (** and ^), more prefix cleaning, and refined expression extraction.
- Version bump to 0.61.0 with README, ROADMAP, and HN/Indie Hackers update sync.

### Changed
- More robust intent detection and calculator plan generation for noisy or natural-language math prompts.
