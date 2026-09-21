# HN / Indie Hackers update — v0.34.0 (2026-09-21)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router, ReAct tools, workspace RAG, multi-agent teams — and a file-backed approval gate you can drain from the CLI with a one-line script. No cloud queue.

## What's new this week
- v0.33: `Agent(approval_gate=...)` + `gated_execute`. Denied/pending tools never run.
- v0.34: `grok-agent approve tui|queue`. Script `A003=approved,A004=denied` or `--policy approve-all`. Example + tests run offline.

## Indie Hackers angle
Most kits either auto-run every tool or bounce you through a hosted dashboard. This one writes pending approvals next to the workspace. A human (or a CI script) says yes/no. The model only sees a block message until then.

## Draft post
**Title:** Show HN: local-first agent kit with a scriptable approval TUI (no cloud queue)

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent approve demo
grok-agent approve react
grok-agent approve tui --seed --script A003=approved,A004=denied
python examples/approve_tui_agent.py
```

Calculator runs. `run_shell` is denied. Search + handoff start pending. The TUI script approves search and denies the handoff. Decisions land in `approvals.json`.

Ask: Test PyPI next, or a 20s terminal GIF?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
