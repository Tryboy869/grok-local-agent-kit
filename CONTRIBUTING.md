# Contributing

Thanks for helping build local-first agents.

## Setup

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Rules of the road

- Python 3.10+, no required cloud APIs.
- New behavior needs tests that run **without a live LLM**.
- Keep the public surface in `grok_local_agent_kit/__init__.py` intentional.
- Prefer small modules (`cli_v0XX.py`, `test_v0XX.py`) over growing god-files.
- File tools stay workspace-scoped. Do not weaken `_safe_path`.
- Do not commit secrets, model weights, or large binaries.

## Pull requests

1. Open an issue if the change is bigger than a small fix.
2. One concern per PR.
3. Update `CHANGELOG.md` and bump version in `pyproject.toml` + `__init__.py` when you add a feature.
4. Run `pytest -q` and `ruff check grok_local_agent_kit tests` if you have ruff.

## Code of conduct

See `CODE_OF_CONDUCT.md`. Security reports: `SECURITY.md`.
