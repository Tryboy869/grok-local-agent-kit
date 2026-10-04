# GIF storyboard — job ledger (v0.44)

Binary GIF is not generated in CI. Record locally:

```bash
# asciinema rec docs/gifs/jobs-demo.cast
grok-agent jobs demo
# agg docs/gifs/jobs-demo.cast docs/gifs/jobs-demo.gif
```

12-second storyboard:

1. `00:00` prompt: `grok-agent jobs demo`
2. `00:02` ledger loads `inbox-digest` (every 3600s)
3. `00:05` workflow lists `inbox.txt` and writes `digest.txt`
4. `00:08` web_search returns the offline fixture (no DuckDuckGo call)
5. `00:10` second tick prints `fired=- skipped=inbox-digest`
6. `00:12` line `wrote=True` — Ollama / LM Studio stay unused

Chat and automation GIFs still need a local model:

- `python examples/chat_agent.py` after `ollama pull llama3.2`
- `python examples/automation_agent.py` for a one-shot tool goal
