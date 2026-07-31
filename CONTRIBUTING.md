# Contributing to grok-local-agent-kit

Thanks for helping make local AI agents better.

## Quick start for contributors

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e ".[dev]"
```

## Development workflow

1. Fork & create a branch: `git checkout -b feature/your-idea`
2. Make changes + add tests if possible
3. Lint & format:
   ```bash
   ruff check --fix .
   black .
   ```
4. Run tests: `pytest`
5. Commit with a clear message (conventional commits preferred):
   - `feat: ...`
   - `fix: ...`
   - `docs: ...`
6. Open a Pull Request against `main`

## What we need most

- Real MCP client implementation (stdio / SSE) — **highest priority for v0.6**
- More robust tool sandboxing (especially `execute_python` & `run_shell`)
- Memory / conversation persistence
- Vision support (local multimodal models)
- Better error messages & structured logging
- Demo GIFs / recordings for the README
- Windows & macOS packaging notes
- Additional ready-to-run examples
- Calculator / math tool enhancements
- CI coverage for more edge cases

## Code style

- Python 3.10+
- Type hints encouraged
- Keep the core dependency surface small
- Prefer clarity over cleverness
- No live LLM required for unit tests

## Reporting issues

Open an issue with:
- OS + Python version
- LLM provider & model
- Minimal reproduction steps
- Expected vs actual behavior

Thank you! 🧠
