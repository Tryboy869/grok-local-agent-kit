"""
Example: give the agent a goal and let it use tools autonomously.
"""

from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2", verbose=True)

goal = """
List the files in the current directory, then summarize what kind of project this is.
If you find a README, read the first 500 characters and use that in your summary.
"""

if __name__ == "__main__":
    print("Running autonomous goal...\n")
    result = agent.run(goal)
    print("\n=== FINAL RESULT ===")
    print(result)
