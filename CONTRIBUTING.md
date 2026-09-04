# Contributing to grok-local-agent-kit

Thanks for helping make local AI agents better.

## Quick start for contributors

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
pytest -q
```

## Development workflow

1. Fork & create a branch: `git checkout -b feature/your-idea`
2. Make changes + add tests if possible
3. Lint & format (`ruff check --fix .` and `black .`)
4. Run tests: `pytest`
5. Commit with conventional messages (`feat:`, `fix:`, `docs:`)
6. Open a Pull Request against `main`

## What we need most (priority order)

1. sqlite-vec behind the existing vector memory API
2. Optional bearer auth + request logging for `grok-agent serve`
3. Full MCP Streamable HTTP session ids + cancellation
4. Per-tool timeouts that cancel `run_shell` subprocesses
5. Vision support (local multimodal models)
6. Demo GIFs / asciinema recordings (`docs/gifs/`)
7. Windows & macOS packaging notes
8. Additional examples and skill packs
9. PyPI-stable 1.0 API freeze

## Code style

- Python 3.10+
- Type hints encouraged
- Keep the core dependency surface small (stdlib first)
- No live LLM required for unit tests
- Default network binds to loopback. Do not change `serve` to `0.0.0.0` without an explicit flag and a warning.

Thank you!
