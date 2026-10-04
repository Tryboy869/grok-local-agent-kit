"""Ready-to-run local automation: due jobs, no model server.

    python examples/jobs_agent.py
    grok-agent jobs demo
    grok-agent jobs tick examples/jobs/inbox.json --workspace . --now 1700000000
"""

from grok_local_agent_kit.jobs import demo_jobs


def main() -> None:
    print(demo_jobs())
    print("chat agent (needs Ollama or LM Studio): python examples/chat_agent.py")
    print("automation agent (needs a local model): python examples/automation_agent.py")


if __name__ == "__main__":
    main()
