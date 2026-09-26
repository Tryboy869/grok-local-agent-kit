"""v0.38 — routed health decisions persist to health.json."""

from pathlib import Path

from grok_local_agent_kit.health import load_board
from grok_local_agent_kit.router import MultiLLMRouter, demo_persisted_route


class _Fake:
    def __init__(self, name: str, status: str):
        self.name = name
        self.status = status

    def ping(self) -> str:
        return self.status

    def chat(self, *a, **k):
        return {"content": f"ok via {self.name}", "tool_calls": []}

    def close(self) -> None:
        return None


def test_pick_writes_health_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dest = Path("health.json")
    from grok_local_agent_kit.health import HealthBoard

    board = HealthBoard(threshold=1, cooldown_s=60)
    router = MultiLLMRouter(health=board, sticky=False, persist_path=dest)
    router._clients["ollama"] = _Fake("ollama", "ok")
    router._clients["lmstudio"] = _Fake("lmstudio", "connection refused")
    ep, _ = router.pick()
    assert ep.name == "ollama"
    assert dest.exists()
    loaded = load_board(dest)
    assert loaded.breaker("lmstudio").state == "open"
    assert loaded.breaker("ollama").state == "closed"


def test_attach_persist_reloads(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dest = Path("health.json")
    from grok_local_agent_kit.health import HealthBoard

    board = HealthBoard(threshold=1, cooldown_s=60)
    first = MultiLLMRouter(health=board, sticky=False, persist_path=dest)
    first._clients["ollama"] = _Fake("ollama", "ok")
    first._clients["lmstudio"] = _Fake("lmstudio", "down")
    first.pick()

    second = MultiLLMRouter(sticky=False)
    second.attach_persist(dest)
    assert second.health is not None
    assert second.health.allow("lmstudio") is False
    assert second.health.allow("ollama") is True


def test_demo_persisted_route(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    text = demo_persisted_route("health.json")
    assert "picked=ollama" in text
    assert "wrote=" in text
    assert "lmstudio" in text
    assert Path("health.json").exists()
