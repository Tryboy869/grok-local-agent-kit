#!/usr/bin/env python3
"""
Research agent example — web search + synthesis + file output.

Searches the web for a topic, summarizes findings, and writes a short
markdown report to disk.

Requires Ollama (or LM Studio) running + network for web_search.

Usage:
  python examples/research_agent.py
  python examples/research_agent.py --topic "MCP protocol for AI agents"
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from grok_local_agent_kit import create_agent, __version__


def main() -> None:
    parser = argparse.ArgumentParser(description="Local research agent")
    parser.add_argument(
        "--topic",
        default="local AI agents and MCP 2026",
        help="Research topic",
    )
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument(
        "--provider",
        default="ollama",
        choices=["ollama", "lmstudio", "openai"],
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    agent = create_agent(
        model=args.model,
        provider=args.provider,
        verbose=args.verbose,
    )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    out_path = f"research_{stamp}.md"

    print(f"🔬 Research Agent (v{__version__})")
    print(f"   Topic: {args.topic}\n")

    goal = (
        f"Research the topic: '{args.topic}'. "
        "1. Use web_search (max_results=6) to gather current information. "
        "2. Synthesize a short structured markdown report with: "
        "title, 3–5 key points, notable projects/tools, and a one-paragraph conclusion. "
        f"3. Write the full report to the file '{out_path}' using write_file. "
        "4. Confirm the file was written and give me a 2-sentence summary."
    )

    result = agent.run(goal)
    print("\n=== Final answer ===")
    print(result)

    agent.close()


if __name__ == "__main__":
    main()
