from grok_local_agent_kit.agent import LocalAgent

if __name__ == "__main__":
    agent = LocalAgent()
    print(agent.run("Write hello world to test.txt using tools and confirm by reading it."))