# Demo GIFs

Binary GIFs are not generated in this environment. Recreate with [VHS](https://github.com/charmbracelet/vhs) or `script` + `agg`.

## Storyboards

1. **tools** — `grok-agent tools demo` → calculator `21*2` = 42.
2. **team + board** — `grok-agent team demo` then `board demo`.
3. **roster + handoff + approvals** — roster / handoff / `approve react` / `approve tui`.
4. **live eval stub** — `grok-agent eval-demo` prints `2/2 passed`.
5. **health board** — `grok-agent health demo`.
6. **health-aware router** — `grok-agent route demo`.
7. **persisted route health** — `grok-agent route persist`.
8. **kit snapshot** — `grok-agent snapshot demo`.
9. **model catalog** — `grok-agent models demo`.
10. **catalog → router** — `grok-agent route catalog` rewrites `placeholder` / env defaults to `llama3.2:latest` and `qwen2.5-7b`.

```
You › grok-agent route catalog
catalog-route
before:
  ollama model=llama3.2
  lmstudio model=local-model
changes:
  ollama: llama3.2 -> llama3.2:latest
  lmstudio: local-model -> qwen2.5-7b
after:
  ollama model=llama3.2:latest
  lmstudio model=qwen2.5-7b
pick(ollama, prefer=llama3.2)=llama3.2:latest
```
