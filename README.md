# 🚀 Grok Local Agent Kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)
[![PyPI](https://img.shields.io/pypi/v/grok-local-agent-kit)](https://pypi.org/project/grok-local-agent-kit/)

**Open-source toolkit for building powerful local AI agents. Supports Ollama, local models, MCP (Model Context Protocol), multi-agent systems, tools, and offline execution. Powered by Grok's autonomous development.**

## ✨ Features

- **Local-first**: Ollama, LM Studio, vLLM, GGUF models
- **MCP Support**: Standardized tool calling and agent interoperability
- **Agent Types**: Reactive, planning, multi-agent, hierarchical, swarms
- **Rich Tools**: Shell, code exec, file ops, web (via proxies), custom skills
- **CLI & API**: `grok-agent` command, Python library
- **Extensible**: .grok/skills system for domain-specific agents
- **Production Ready**: Logging, error handling, persistence

## Quickstart

```bash
pip install grok-local-agent-kit ollama

# Start Ollama and pull model
ollama pull llama3.2

# Run agent
grok-agent "Create a simple FastAPI todo app with SQLite"
```

See [examples/](examples/) for more.

## Roadmap

See [ROADMAP.md](ROADMAP.md) - v1.0 Q3 2026: Full MCP, agent marketplace.

## Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - see LICENSE.

*Autonomously built and maintained with Grok. Aim: 10k stars!*