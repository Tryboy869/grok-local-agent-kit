# GIF storyboard — ReAct handoff (v0.47)

Binary GIF is not committed. Recreate with [VHS](https://github.com/charmbracelet/vhs) or any terminal recorder.

## Frame 1 — install

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
```

## Frame 2 — offline call

```bash
grok-agent handoff demo
```

Terminal shows five steps with `handoff=react react=called` and answers prefixed `[react-scripted] ollama`. No model daemon is required. `playbook-report.json` lands in `.grok/handoff/`.

## Frame 3 — live opt-in

```bash
ollama serve   # optional
grok-agent handoff live
```

If the probe is down, steps stay `react=skipped` and the scripted MVP answers still print. If Ollama or LM Studio is up, `react_called` is greater than 0 and the answer comes from `Agent.run`.

Suggested crop: 100 columns, 28 rows, 8 seconds, dark terminal.
