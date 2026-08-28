"""Named session persistence tests (no live LLM)."""

from grok_local_agent_kit.agent import create_agent
from grok_local_agent_kit.session import list_sessions, sanitize_session_name


def test_sanitize_session_name():
    assert sanitize_session_name("My Session!") == "My-Session"
    assert sanitize_session_name("") == "default"


def test_named_session_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    agent = create_agent(model="dummy", provider="ollama", session_name="demo")
    agent.history = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
    msg = agent.save_named_session("demo")
    assert "Saved session" in msg
    assert "demo" in list_sessions()

    other = create_agent(model="dummy", provider="ollama")
    loaded = other.load_named_session("demo")
    assert "Loaded session" in loaded
    assert other.history[0]["content"] == "hi"
    listed = other.list_named_sessions()
    assert "demo" in listed
    agent.close()
    other.close()
