# Demo GIFs

Record these with asciinema + agg, or VHS. Until binary GIFs are committed, this file is the storyboard.

1. demo-chat.gif — grok-agent chat -v --stream
2. demo-route.gif — grok-agent route
3. demo-mcp.gif — python examples/mcp_agent.py --no-llm
4. demo-hooks.gif — python examples/hooks_agent.py
5. demo-memory.gif — grok-agent memory remember / recall
6. demo-vector.gif — python examples/vector_memory_agent.py
7. demo-skills.gif — python examples/skills_agent.py
8. demo-sandbox.gif — python examples/sandbox_agent.py
9. demo-embed.gif — python examples/embed_agent.py
10. demo-parallel.gif — python examples/parallel_agent.py
11. demo-serve.gif — python examples/serve_agent.py then curl POST /v1/chat
12. demo-planner.gif — python examples/planner_agent.py
13. demo-guardrails.gif — python examples/guardrails_agent.py

Storyboard notes:
- Serve: split pane, server logs + JSON response with text and trace.
- Planner: add two items, mark one done, show .grok/plan.json.
- Guardrails: denied tool name printed, then a timeout message.
