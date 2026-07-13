# 🧠 grok-local-agent-kit

[![GitHub stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org)
[![CI](https://github.com/Tryboy869/grok-local-agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Tryboy869/grok-local-agent-kit/actions)

**Open-source toolkit for building powerful local AI agents with MCP support, multi-LLM routing, and developer tools. Run agents offline-first. Built autonomously by Grok.**

## ✨ Features

- **Local-First**: Full offline support with Ollama and compatible providers
- **Multi-Provider**: Ollama, LM Studio, OpenAI-compatible endpoints
- **Tool System**: Web search, file I/O, shell, custom tools, MCP stubs
- **Autonomous Reasoning**: Tool-calling loops, reflection, error recovery
- **CLI & Python SDK**: Simple usage for scripts and interactive agents
- **Extensible Architecture**: Easy plugin system for new tools/models
- **CI/CD Ready**: GitHub Actions for testing and quality
- **MCP Protocol**: Ready for advanced multi-agent coordination

## 🚀 Quickstart

1. **Install Ollama** (recommended): [ollama.com](https://ollama.com)
2. Pull a model: `ollama pull llama3.2` or `phi3`
3. Install kit:
   ```bash
   pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
   ```
4. Run chat agent:
   ```bash
   grok-agent chat "Help me plan a project to get 10k GitHub stars in 3 months"
   ```

**With LM Studio**:
```bash
grok-agent chat "Your prompt here" --provider lmstudio --base-url http://localhost:1234/v1
```

## 📦 Installation

```bash
pip install grok-local-agent-kit
```

From source:
```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e .
```

## 🛠️ Usage Examples

See [examples/](examples/)

**Basic Agent**
```python
from grok_local_agent_kit.agent import create_agent

agent = create_agent(model="llama3.2")
print(agent.chat("What is the capital of France?"))
```

**Custom Tools**
```python
agent.register_tool(...)
```

## 📖 Documentation

- [Agent Core](grok_local_agent_kit/agent.py)
- [CLI](grok_local_agent_kit/cli.py)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for upcoming features:
- v0.3: Full MCP implementation, multi-agent teams
- v0.4: Vision/multimodal, RAG integration
- v0.5: GUI, deployment tools, benchmarks

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Submit PR with tests

Stars and feedback appreciated! Help us reach 10k stars ⭐

## License
MIT License - see [LICENSE](LICENSE) for details.

**Built with ❤️ by Grok in autonomous mode for the open-source community.**