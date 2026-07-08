# 🧠 grok-local-agent-kit

**MVP for building powerful local AI agents. Offline, tool-calling enabled, multi-LLM support (Ollama + LM Studio compat). Inspired by Grok's autonomy.**

![Stars](https://img.shields.io/github/stars/Tryboy869/grok-local-agent-kit?style=social)
![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **Core Agent** with routing & tool calling via Ollama
- **Tools**: Web search (placeholder), file ops, extensible
- **Multi-LLM**: Ollama primary, OpenAI-compatible (LM Studio)
- **Examples**: Chat & automation agents ready-to-run
- **MCP ready**: Foundation for Model Context Protocol integration
- **Pythonic & CLI**

## 🚀 1-Command Install & Run

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# Install kit
pip install git+https://github.com/Tryboy869/grok-local-agent-kit.git

# Run chat example
python examples/chat_agent.py
```

## 📋 Examples

**Chat Agent**
```bash
python examples/chat_agent.py
```

**Automation Agent**
```bash
python examples/automation_agent.py
```

## 🛠️ Advanced

Extend with custom tools in your scripts.

## Roadmap
See [ROADMAP.md](ROADMAP.md)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

**Push to HN/Indie Hackers:** 'Open Source Local Grok-like Agent Kit - Run autonomous agents offline with Ollama!'

Built autonomously.