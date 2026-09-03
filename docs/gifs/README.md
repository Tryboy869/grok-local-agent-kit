# Demo GIFs

Record these with [asciinema](https://asciinema.org/) + `agg`, or [VHS](https://github.com/charmbracelet/vhs).
Until binary GIFs are committed, this file is the storyboard.

## 1. demo-chat.gif

```
$ grok-agent chat -v --stream
You › list files in this folder then summarize README.md
  · thought: I'll list the workspace then read README.md
  → tool: list_files({})
  → tool: read_file({path: README.md})
Agent › This kit runs local ReAct agents on Ollama / LM Studio...
```

## 2. demo-route.gif

```
$ grok-agent route
ollama  llama3.2   http://127.0.0.1:11434   ok
lmstudio local-model http://127.0.0.1:1234/v1   down — skipped
picked ollama
```

## 3. demo-sandbox.gif

```
$ python examples/sandbox_agent.py
>>> print(sum(range(10)))
    45
>>> import os
    Blocked import of 'os'
```

## 4. demo-embed.gif

```
$ GROK_EMBED_BACKEND=hash python examples/embed_agent.py
embed backend: hash  dim=256
Vector-remembered id=1
Vector memory:
- #1 score=0.71 ... Ship grok-local-agent-kit v0.14
```

## 5. demo-mcp.gif / demo-hooks.gif / demo-vector.gif

See `examples/mcp_agent.py --no-llm`, `examples/hooks_agent.py`, `examples/vector_memory_agent.py`.

## 6. demo-parallel.gif

```
$ python examples/parallel_agent.py
  · thought: I'll list files and compute 7*6 in parallel.
  ⇢ running 2 tools in parallel
  → tool: list_files({'path': '.'})
  → tool: calculator({'expression': '7*6'})
Wrote trace (3 steps) to .../.grok/traces/last.json
```
