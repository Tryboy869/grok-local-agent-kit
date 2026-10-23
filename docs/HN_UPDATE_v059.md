# HN / Indie Hackers update — grok-local-agent-kit v0.59.0

**Title ideas:**
- Show HN: grok-local-agent-kit v0.59 – offline-first local AI agents (Ollama, LM Studio, MCP, ReAct)
- Local AI agents that work fully offline (updated toolkit)

**Body:**

I built an offline-first Python toolkit for local agents.

It talks to Ollama or LM Studio (OpenAI-compatible), runs a ReAct tool loop, multi-LLM fallback with circuit breaker, and ships with real tools out of the box.

**What’s new in v0.59.0:**
- Improved math expression extraction in the offline MVP core (`plan_for`) so calculator routing is more reliable.
- New clean ready-to-run example: `python examples/ready_core_agent.py` — routing + datetime, math, files, search fixture, system info, MCP echo + multi-LLM probes. Fully offline.
- README refreshed: 1-command install reinforced, clearer demo storyboards.

**Quick start (still one command):**
```bash
curl -fsSL https://raw.githubusercontent.com/Tryboy869/grok-local-agent-kit/main/scripts/install.sh | bash
grok-agent doctor
python examples/ready_core_agent.py
python examples/enhanced_core_agent.py
```

Most demos run completely offline. No API key required for local models.

Repo: https://github.com/Tryboy869/grok-local-agent-kit  
License: MIT. Python >= 3.10.  
Built autonomously by Grok. Stars welcome if useful.

From source:
```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python examples/ready_core_agent.py
```

Feedback welcome — especially on the offline routing and tool surface.
