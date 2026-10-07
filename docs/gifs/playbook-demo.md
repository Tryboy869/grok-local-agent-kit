# GIF storyboard — playbook agent

Binary GIF not generated in CI. Record with [VHS](https://github.com/charmbracelet/vhs).

Duration: ~14s. Terminal 100x24, dark theme.

1. `grok-agent playbook demo` prints `Playbook local-mvp ok=True handoff=scripted`.
2. Provider line shows `ollama=down, lmstudio=down` (or `up` if a daemon is listening). The run still finishes.
3. Step lines: `chat intent=files`, `math intent=math` with `22.0`, `system`, `search`, `mcp`.
4. Last line points at `.grok/playbook/playbook-report.json`.
5. Cut to `python examples/playbook_agent.py`, same five intents, note file created.

Suggested tape:

```
Output docs/gifs/playbook-demo.gif
Set Shell "bash"
Set Width 1000
Set Height 600
Type "grok-agent playbook demo"
Enter
Sleep 2s
Type "python examples/playbook_agent.py"
Enter
Sleep 2s
```
