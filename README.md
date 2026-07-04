# Grok Local Agent Kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit.svg?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)

**Autonomous local AI agents powered by Ollama + MCP. Inspired by Grok. Run offline, scale with tools.**

## ✨ Features

- Local LLMs via Ollama (llama3, mistral, etc.)
- MCP support for advanced tooling
- Multi-agent orchestration
- Simple Python API
- CLI tools
- Extensible skills system
- GitHub Actions for CI/CD

## 🚀 Quickstart

1. Install Ollama: https://ollama.com
2. `pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git`
3. ```python
from grok_local_agent_kit.agent import LocalAgent
agent = LocalAgent()
print(agent.run("Hello, world!"))
```

## 📖 Full Documentation
See [docs/](./docs) and [examples/](./examples).

## 🛠️ Roadmap (3 months to 10k stars)
- v0.2: Memory & RAG
- v0.3: Vision & multimodal
- v1.0: Full MCP ecosystem + web UI

**Star if you like offline AI agents!** ⭐

## License
[MIT](./LICENSE) - Free to use, modify, distribute.