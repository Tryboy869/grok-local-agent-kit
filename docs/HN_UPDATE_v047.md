# HN / Indie Hackers update — v0.47

Title: Show HN: grok-local-agent-kit v0.47 — local playbooks that can hand off to Ollama

Repo: https://github.com/Tryboy869/grok-local-agent-kit
License: MIT. Python >= 3.10. Package version 0.47.0.

## What changed

v0.46 recorded a ReAct handoff descriptor and never opened a chat socket. v0.47 calls the loop when you ask it to.

- `execute_handoff` runs an injected callable, or `Agent.run` when `live=True`
- Providers still down: the offline MVP (files, math, search, system, MCP echo) finishes and marks react as skipped
- `grok-agent handoff demo` uses a scripted stand-in so the call path is visible without a daemon
- `grok-agent handoff live` probes Ollama (:11434) and LM Studio (:1234) and only then talks to a model

## Try it

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent handoff demo
python examples/handoff_react_agent.py
```

No API key. No cloud. Live mode is opt-in and fails inside the report if the daemon is down.

## Honest limits

The demo callable is not a model. Live mode needs a local server you already run. GIFs in docs/gifs are storyboards, not recorded binaries. Stars are not a feature.
