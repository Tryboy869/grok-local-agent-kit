# 🚀 Grok Local Agent Kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit.svg?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![PyPI](https://img.shields.io/pypi/v/grok-local-agent-kit)](https://pypi.org/project/grok-local-agent-kit/)

**Open-source toolkit for building powerful local AI agents with Ollama, MCP, and tool integration.** Run agents offline-first, privacy-focused, Grok-inspired.

## ✨ Features

- **Local LLMs**: Full support for Ollama, LM Studio, vLLM
- **Tool Use & MCP**: Web search, file ops, memory/context/planning
- **Multi-Agent & Orchestration**: Chain agents, plan-execute
- **CLI & API**: Easy integration in scripts or apps
- **Extensible**: Custom tools, models, providers
- **CI/CD Ready**: GitHub Actions included

## 🚀 Quick Start

```bash
pip install grok-local-agent-kit

# CLI
npx grok-agent "Help me build a local agent for code review"

grok-agent --model llama3.2 "Your prompt here"

# Python
from grok_local_agent_kit.agent import create_agent

agent = create_agent(model="llama3.2")
response = agent.chat("What is the capital of France? Use tools if needed.")
print(response)
```

## 📋 Installation

1. Install Ollama: https://ollama.com
2. `ollama pull llama3.2`
3. `pip install grok-local-agent-kit`

## 📖 Examples

See `examples/` directory.

## Roadmap

- v0.3: Full MCP implementation, agent swarm
- v0.5: GUI (Streamlit/Tkinter)
- v1.0: Advanced reasoning, RAG, vision support

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome!

## License

MIT - see [LICENSE](LICENSE)

---

*Built autonomously by Grok to empower open-source AI. Target: 10k ⭐ in 3 months. Star, fork, contribute!*