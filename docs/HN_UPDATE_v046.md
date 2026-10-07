# HN / Indie Hackers update — v0.46 (2026-10-07)

Title: Show HN: local agent kit – one playbook runs chat, files, search, and MCP with no cloud

Body:

v0.46 of grok-local-agent-kit adds a playbook runner on top of the offline MVP.

What changed:

- `grok-agent playbook demo` runs five goals: write a note, `sqrt(144)+10`, system info, web search (injectable), MCP echo.
- Same path as `python examples/playbook_agent.py` and `examples/playbooks/local_mvp.json`.
- If Ollama (`:11434`) or LM Studio (`:1234/v1`) answers a probe, the report records a ReAct handoff (`mode=react`, provider, base URL, model). The playbook itself still does not open a chat socket, so CI stays offline.
- If both providers are down, every step stays on the scripted router (`handoff=scripted`) and the demo still exits 0.
- Report lands in `.grok/playbook/playbook-report.json`.

Install:

```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
grok-agent playbook demo
python examples/mvp_chat.py "compute sqrt(144) + 10"
python examples/mvp_automation.py
```

Optional live chat (Ollama or LM Studio):

```bash
ollama pull llama3.2
grok-agent chat -v --stream --router
```

Repo: https://github.com/Tryboy869/grok-local-agent-kit

GIF: storyboard only in `docs/gifs/playbook-demo.md` (no binary in the repo). Terminal shows the five intents, `22.0` from the calculator, and provider probes `down` or `up`.

Indie Hackers angle: local-first agent toolkit, MIT, one-command install, no API key for the demo path. Looking for people who already run Ollama and want a small Python control plane instead of another hosted agent framework.
