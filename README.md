# 🧠 grok-local-agent-kit

[![Stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit)](https://github.com/Tryboy869/grok-local-agent-kit/stargazers)
[![Forks](https://img.shields.io/github/forks/Tryboy869/grok-local-agent-kit)](https://github.com/Tryboy869/grok-local-agent-kit/network/members)
[![License](https://img.shields.io/github/license/Tryboy869/grok-local-agent-kit)](https://github.com/Tryboy869/grok-local-agent-kit/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-green)](https://ollama.com)

**Build powerful local AI agents with Ollama, MCP support, tool calling, multi-LLM routing, and full autonomy. Offline-first, no cloud dependency. Built with ❤️ by Grok.**

## ✨ Features

- **Local LLM Integration**: Full support for Ollama (llama3.2, mistral, etc.)
- **Tool Calling & MCP**: Native function calling with file, web, and custom tools
- **Autonomous Agents**: Self-improving loops, planning, and execution
- **Multi-Provider Routing**: Ollama, local Grok-like, future LM Studio, etc.
- **CLI & Python SDK**: Easy integration and command-line usage
- **Examples**: Chat, automation, research agents ready to run
- **GitHub Actions CI**: Automated testing and packaging

## 🚀 Quick Start

1. **Install Ollama**: [ollama.com](https://ollama.com)
   ```bash
   ollama pull llama3.2
   ```

2. **Install the Kit**:
   ```bash
   pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git
   ```

3. **Run an Example**:
   ```bash
   python -m grok_local_agent_kit.cli chat "What can you do?"
   # or
   python examples/chat_agent.py
   ```

## 📖 Documentation

- [Agent API](./grok_local_agent_kit/agent.py)
- [CLI](./grok_local_agent_kit/cli.py)
- [Examples](./examples/)
- [Roadmap](./ROADMAP.md)

## 🛠️ Installation from Source

```bash
git clone https://github.com/Tryboy869/grok-local-agent-kit.git
cd grok-local-agent-kit
pip install -e .
```

## 🎯 Use Cases

- Personal automation assistants
- Code generation & debugging agents
- Research & knowledge agents
- Local RAG pipelines
- Multi-agent collaboration systems

## 📊 Roadmap

See [ROADMAP.md](ROADMAP.md) for v1.0, v2.0 plans including GUI, more integrations, MCP full spec.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

**Star this repo if you find it useful!** Let's build the future of local AI agents together. Feedback and PRs welcome!