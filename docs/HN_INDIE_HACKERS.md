# HN / Indie Hackers update — v0.32.0 (2026-09-19)

## One-liner
Local-first Python agent kit: Ollama + LM Studio router, ReAct tools, workspace RAG, multi-agent teams that persist their roster / board / work queue — plus a file-backed approval gate so a human can allow or deny a tool or a task claim without sending anything to the cloud.

## What's new this week
- v0.31: `HandoffQueue` — offer / claim / complete / drop. Mirrors onto the blackboard.
- v0.32: `ApprovalGate` — allow/deny lists, programmable decider, JSON persist. `grok-agent approve demo`.
- Tests run without a live LLM.

## Indie Hackers angle
Most agent kits either auto-run every tool or bounce you through a hosted dashboard. This one writes pending approvals next to the workspace. Cron, a TUI, or a human can decide later. No Redis, no SaaS queue, no API key for the happy path.

## Draft post
**Title:** Show HN: local-first agent kit with a file-backed approval gate (no cloud queue)

Built a Python toolkit so agents on Ollama / LM Studio can share a team blackboard, persist a roster, hand off tasks, and now pause for a human before a dangerous tool or a claim.

```
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent approve demo
python examples/approve_agent.py
```

Calculator is allow-listed, `shell` is denied, a handoff claim stays pending until you decide. Decisions land in `approvals.json`.

Ask: would you rather we ship a 20s terminal GIF next, or a Test PyPI package?

## Links
- Repo: https://github.com/Tryboy869/grok-local-agent-kit
- Show HN draft: `SHOW_HN.md`
- Roadmap: `ROADMAP.md`
