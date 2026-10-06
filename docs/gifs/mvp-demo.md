# GIF storyboard — offline MVP

Binary GIF not generated in CI. Record with [VHS](https://github.com/charmbracelet/vhs).

Duration: ~12s. Terminal 100x24, dark theme.

1. `grok-agent mvp` prints `MVP demo (no LLM required)` and the provider table `ollama, lmstudio`.
2. Chat line shows `intent=math` and `22.0` from `sqrt(144)+10`.
3. Automation line shows `wrote=True` after `mvp_note.txt` is created under `.grok/mvp/auto`.
4. Search line shows the injected top hit. Provider probes print `down` if nothing is listening on 11434 / 1234.
5. Cut to `python examples/mvp_chat.py "search local agents"` then `python examples/mvp_automation.py`.

Suggested tape:

```
Output docs/gifs/mvp-demo.gif
Set Shell "bash"
Set Width 1000
Set Height 600
Type "grok-agent mvp"
Enter
Sleep 2s
```
