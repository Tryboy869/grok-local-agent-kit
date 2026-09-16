# Demo GIFs (storyboards)

Binary GIFs are not checked in. Record with [VHS](https://github.com/charmbracelet/vhs) or `script` + `agg`.

## 1. Chat + tools

```
grok-agent chat -v --stream
# user: list files in this folder
# user: calculate 21*2
```

## 2. Plugin sandbox

```
python examples/sandbox_plugin_agent.py
grok-agent sandbox status
grok-agent sandbox skipped
GROK_AGENT_ALLOW_PY_PLUGINS=1 grok-agent plugins list
```

Expected: JSON plugins appear; `.py` plugins stay skipped until the env flag or allowlist.

## 3. Serve

```
GROK_AGENT_SERVE_TOKEN=dev grok-agent serve --port 8765
```

## 4. Persisted team board (v0.29)

```
grok-agent team demo
grok-agent board demo --path board.jsonl
grok-agent board show board.jsonl
python examples/persist_agent.py --sqlite
```

Expected: posts survive the process; a second demo appends another goal/round.
