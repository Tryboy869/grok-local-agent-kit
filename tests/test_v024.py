from pathlib import Path
from tempfile import TemporaryDirectory

from grok_local_agent_kit.plugins import apply_plugins, discover_plugins, load_json_plugin
from grok_local_agent_kit.transcripts import append_turn, new_path, read_transcript, summarize
from grok_local_agent_kit.tools import execute_tool


def test_json_plugin_template(tmp_path: Path):
    p = tmp_path / "greet.json"
    p.write_text(
        '{"name":"greet","description":"say hi","kind":"template","template":"hello {name}","parameters":{"type":"object","properties":{"name":{"type":"string"}}}}',
        encoding="utf-8",
    )
    spec, fn = load_json_plugin(p)
    assert spec["function"]["name"] == "greet"
    assert fn(name="ada") == "hello ada"


def test_discover_and_apply(tmp_path: Path):
    d = tmp_path / "tools"
    d.mkdir()
    (d / "echo.json").write_text(
        '{"name":"plugin_echo","description":"echo json","kind":"json"}',
        encoding="utf-8",
    )
    found = discover_plugins(extra_dirs=[d])
    names = [n for n, _, _ in found]
    assert "plugin_echo" in names
    specs, funcs = apply_plugins([], {}, extra_dirs=[d])
    assert "plugin_echo" in funcs
    out = execute_tool("plugin_echo", {"x": 1}, funcs)
    assert '"x": 1' in out or '"x":1' in out
    assert specs[0]["function"]["name"] == "plugin_echo"


def test_transcript_roundtrip():
    with TemporaryDirectory() as tmp:
        path = new_path("demo", directory=Path(tmp))
        append_turn(path, "user", "hi")
        append_turn(path, "assistant", "hello")
        rows = read_transcript(path)
        assert len(rows) == 2
        assert rows[0]["content"] == "hi"
        assert "user=1" in summarize(path)
