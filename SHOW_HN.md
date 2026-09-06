# Show HN: grok-local-agent-kit 0.18 — local agents that can kill hung shells

I keep shipping a small Python kit for **offline-first agents** on Ollama / LM Studio.

v0.18 is the unglamorous safety slice: when a tool timeout fires, `run_shell` no longer leaves a `sleep` (or worse) running. Children are started in a new session and SIGTERM/SIGKILL'd via a process registry + `CancelToken`.

Also still in the box: bearer token on `grok-agent serve`, replay of `export_trace()` without a GPU, MCP stdio/HTTP/SSE, router, planner, guardrails.

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/cancel_agent.py
pytest -q
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit
