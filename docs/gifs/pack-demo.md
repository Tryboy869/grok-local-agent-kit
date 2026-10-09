# GIF storyboard — session pack (v0.48)

Binary GIFs are not committed. Recreate with [VHS](https://github.com/charmbracelet/vhs) when a terminal recorder is available.

## Tape

```
Output docs/gifs/pack-demo.gif
Set Shell bash
Set Width 1100
Set Height 640
Type "grok-agent pack demo"
Enter
Sleep 2s
Type "sed -n '1,20p' .grok/pack/SESSION.md"
Enter
Sleep 2s
```

## What the viewer should see

1. `grok-agent pack demo` prints four goals: chat (math), automation (write_file), research (web_search fixture), MCP echo.
2. Provider lines say `not-probed` unless `--probe` is passed.
3. `.grok/pack/SESSION.md` and `pack-report.json` appear beside the note file.
4. No Ollama or LM Studio window is required. The demo still passes if both daemons are down.
