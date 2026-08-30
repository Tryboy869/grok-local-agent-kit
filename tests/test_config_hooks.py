"""Config + hooks unit tests (no live LLM)."""

from grok_local_agent_kit.config import KitConfig, load_config, write_example_config
from grok_local_agent_kit.hooks import HookBus, default_verbose_hooks
from grok_local_agent_kit.mcp_http import HTTPMCPClient
from grok_local_agent_kit.factory import create_agent


def test_write_and_load_toml(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dest = write_example_config(tmp_path / "grok-agent.toml")
    assert dest.is_file()
    cfg = load_config(dest)
    assert cfg.model == "llama3.2"
    assert cfg.provider == "ollama"
    assert "model" in cfg.to_agent_kwargs()


def test_env_overrides_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "grok-agent.json").write_text('{"model": "from-file", "provider": "ollama"}')
    monkeypatch.setenv("GROK_AGENT_MODEL", "from-env")
    cfg = load_config(tmp_path / "grok-agent.json")
    assert cfg.model == "from-env"


def test_hook_bus_emits():
    bus = HookBus()
    seen = []
    bus.on("before_tool", lambda **p: seen.append(p["name"]))
    bus.emit("before_tool", name="calculator", args={})
    assert seen == ["calculator"]


def test_default_verbose_hooks_do_not_crash():
    lines = []
    bus = default_verbose_hooks(print_fn=lines.append)
    bus.emit("before_tool", name="x", args={"a": 1})
    bus.emit("after_tool", name="x", result="ok")
    bus.emit("on_final", text="done")
    assert any("before_tool" in line for line in lines)


def test_agent_on_helper():
    agent = create_agent(model="dummy", provider="ollama")
    fired = []
    agent.on("on_final", lambda **p: fired.append(p["text"]))
    agent.hooks.emit("on_final", text="hello")
    assert fired == ["hello"]
    agent.close()


def test_http_mcp_client_constructs():
    client = HTTPMCPClient("http://127.0.0.1:9/mcp")
    assert client.url.endswith("/mcp")
    assert client.initialized is False


def test_kitconfig_defaults():
    cfg = KitConfig()
    assert cfg.max_iterations == 12
    assert cfg.session_name == "default"
