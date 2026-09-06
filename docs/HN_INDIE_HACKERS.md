# Launch update — v0.18.0 (HN / Indie Hackers)

**One-liner:** Local AI agents that call tools, fail over Ollama ↔ LM Studio, speak MCP, stream thoughts, replay traces without a GPU — and now **actually kill hung shell children** when you cancel or hit a tool timeout.

**What's new since v0.17**

- `CancelToken` + process-group `run_shell` (`Popen`, `start_new_session=True`)
- Timeout / `cancel_all()` sends SIGTERM then SIGKILL to tracked PIDs
- `grok-agent cancel` and `python examples/cancel_agent.py` (no LLM)
- `tests/test_v018.py`

**Install**

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor && grok-agent route
python examples/cancel_agent.py
pytest -q
```

**Ask:** Next blocker for 1.0 — sqlite-vec, recorded GIFs, or a frozen PyPI API?

Repo: https://github.com/Tryboy869/grok-local-agent-kit
