from grok_local_agent_kit.health import OPEN, HealthBoard
from grok_local_agent_kit.router import LLMEndpoint, MultiLLMRouter, demo_routed_health, format_probe


class FakeClient:
    def __init__(self, name: str, status: str = "ok", chat_text: str = ""):
        self.name = name
        self.status = status
        self.chat_text = chat_text or f"hello from {name}"
        self.pings = 0
        self.chats = 0

    def ping(self) -> str:
        self.pings += 1
        return self.status

    def chat(self, messages, tools=None, tool_choice="auto"):
        self.chats += 1
        return {"content": self.chat_text, "tool_calls": []}

    def close(self) -> None:
        return None


def _router(health=None):
    chain = [
        LLMEndpoint(name="ollama", provider="ollama", model="llama3.2"),
        LLMEndpoint(name="lmstudio", provider="openai", model="local-model", base_url="http://127.0.0.1:1234/v1"),
    ]
    r = MultiLLMRouter(chain=chain, sticky=False, health=health)
    r._clients["ollama"] = FakeClient("ollama", "ok")
    r._clients["lmstudio"] = FakeClient("lmstudio", "ok")
    return r


def test_pick_skips_open_breaker():
    board = HealthBoard(threshold=1, cooldown_s=60)
    board.trip("ollama", error="down")
    r = _router(health=board)
    ep, client = r.pick()
    assert ep.name == "lmstudio"
    assert client.name == "lmstudio"
    assert board.breaker("ollama").state == OPEN


def test_probe_marks_breaker_open_without_ping():
    board = HealthBoard(threshold=1, cooldown_s=60)
    board.trip("lmstudio")
    r = _router(health=board)
    rows = {row["name"]: row["status"] for row in r.probe()}
    assert rows["lmstudio"] == "breaker-open"
    assert rows["ollama"].startswith("ok")
    assert r._clients["lmstudio"].pings == 0


def test_chat_falls_back_and_trips_unhealthy():
    board = HealthBoard(threshold=1, cooldown_s=60)
    r = _router(health=board)
    r._clients["ollama"] = FakeClient("ollama", "ok", chat_text="[LLM error] boom")
    result = r.chat([{"role": "user", "content": "hi"}])
    assert result["routed_via"] == "lmstudio"
    assert "hello from lmstudio" in result["content"]
    assert board.breaker("ollama").failures >= 1


def test_sticky_clears_when_active_trips():
    board = HealthBoard(threshold=1, cooldown_s=60)
    r = MultiLLMRouter(
        chain=[
            LLMEndpoint(name="ollama", provider="ollama", model="m"),
            LLMEndpoint(name="lmstudio", provider="openai", model="m"),
        ],
        sticky=True,
        health=board,
    )
    r._clients["ollama"] = FakeClient("ollama", "ok")
    r._clients["lmstudio"] = FakeClient("lmstudio", "ok")
    first, _ = r.pick()
    assert first.name == "ollama"
    board.trip("ollama")
    second, _ = r.pick()
    assert second.name == "lmstudio"


def test_demo_offline():
    text = demo_routed_health()
    assert "picked=ollama" in text
    assert "breaker-open" in text
    assert "LLM route probe" in format_probe([{"name": "x", "provider": "p", "model": "m", "base_url": "", "status": "ok"}])
