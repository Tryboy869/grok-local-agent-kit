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

## 5. Approval TUI (v0.34)

```
grok-agent approve react
grok-agent approve queue --seed
grok-agent approve tui --seed --script A003=approved,A004=denied
python examples/approve_tui_agent.py
```

Expected: two pending rows (web_search, T004); after the script the queue is empty and `approvals.json` records the decisions.

## 6. Health board (v0.36)

```
grok-agent health demo
grok-agent health show
grok-agent health reset lmstudio
python examples/health_agent.py --demo
```

Expected: ollama stays closed/allow=ok; lmstudio is open after two refused connections.
