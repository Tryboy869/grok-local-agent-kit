"""ReAct loop tests with a fake LLM (no live model)."""

from grok_local_agent_kit.agent import Agent
from grok_local_agent_kit.factory import create_agent
from grok_local_agent_kit.hooks import EVENTS
from grok_local_agent_kit.skills import load_skill_file, load_skills


class FakeLLM:
    def __init__(self, script):
        self.script = list(script)
        self.model = "fake"
        self.provider = "fake"
        self.base_url = ""

    def chat(self, messages, tools=None, tool_choice="auto"):
        if not self.script:
            return {"content": "done", "tool_calls": None, "raw": None}
        return self.script.pop(0)

    def stream_chat(self, messages, tools=None):
        yield from []
        return {"content": "done", "tool_calls": None, "raw": None}

    def ping(self):
        return "ok — fake"

    def close(self):
        return None


def test_loop_emits_hooks_and_calls_calculator():
    agent = Agent(model="dummy", provider="ollama", verbose=False)
    agent.llm = FakeLLM(
        [
            {
                "content": "I'll use the calculator.",
                "tool_calls": [
                    {
                        "id": "c1",
                        "name": "calculator",
                        "arguments": {"expression": "2+2"},
                    }
                ],
            },
            {"content": "The answer is 4.", "tool_calls": None},
        ]
    )
    events = []
    agent.on("before_tool", lambda **p: events.append(("before", p["name"])))
    agent.on("after_tool", lambda **p: events.append(("after", p["name"], p["result"])))
    agent.on("on_final", lambda **p: events.append(("final", p["text"])))
    agent.on("on_thought", lambda **p: events.append(("thought", p["text"])))

    out = agent.run("what is 2+2?")
    assert "4" in out
    kinds = [e[0] for e in events]
    assert "before" in kinds and "after" in kinds and "final" in kinds
    assert "on_thought" in EVENTS
    assert any(step["type"] == "tool" for step in agent.last_trace)
    agent.close()


def test_factory_agent_has_hooks_and_memory_tools():
    agent = create_agent(model="dummy", provider="ollama")
    assert hasattr(agent, "hooks")
    assert "remember" in agent.tool_funcs
    assert "recall" in agent.tool_funcs
    agent.close()


def test_skill_loader(tmp_path):
    skill = tmp_path / "demo.json"
    skill.write_text(
        """
        {
          "name": "demo",
          "tools": [
            {
              "name": "shout",
              "description": "Shout a message",
              "kind": "template",
              "template": "SHOUT:{msg}",
              "parameters": {
                "type": "object",
                "properties": {"msg": {"type": "string"}},
                "required": ["msg"]
              }
            }
          ]
        }
        """
    )
    tools = load_skill_file(skill)
    assert tools[0]["func"](msg="hi") == "SHOUT:hi"

    agent = Agent(model="dummy", provider="ollama")
    added = load_skills(agent, str(tmp_path))
    assert "shout" in added
    assert agent.tool_funcs["shout"](msg="yo") == "SHOUT:yo"
    agent.close()
