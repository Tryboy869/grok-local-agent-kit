from grok_local_agent_kit.agent import LocalAgent

if __name__ == "__main__":
    agent = LocalAgent()
    print("Chat example:")
    print(agent.run("Hello, demonstrate a tool use."))