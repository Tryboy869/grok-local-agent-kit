from pathlib import Path

from grok_local_agent_kit.plugins import apply_plugins, discover_plugins, skipped_py_plugins


def test_py_plugin_skipped_by_default(tmp_path: Path):
    d = tmp_path / "tools"
    d.mkdir()
    (d / "secret.py").write_text(
        "NAME='secret'\nDESCRIPTION='x'\ndef handler(**kw):\n    return 'loaded'\n",
        encoding="utf-8",
    )
    found = discover_plugins(extra_dirs=[d])
    assert found == []
    assert any(p.name == "secret.py" for p in skipped_py_plugins())


def test_py_plugin_allow_flag(tmp_path: Path):
    d = tmp_path / "tools"
    d.mkdir()
    (d / "secret.py").write_text(
        "NAME='secret'\nDESCRIPTION='x'\ndef handler(**kw):\n    return 'loaded'\n",
        encoding="utf-8",
    )
    found = discover_plugins(extra_dirs=[d], allow_py=True)
    assert [n for n, _, _ in found] == ["secret"]
    _, fn = found[0][1], found[0][2]
    assert fn() == "loaded"


def test_json_still_loads(tmp_path: Path):
    d = tmp_path / "tools"
    d.mkdir()
    (d / "ping.json").write_text(
        '{"name":"ping","description":"p","kind":"template","template":"pong"}',
        encoding="utf-8",
    )
    specs, funcs = apply_plugins([], {}, extra_dirs=[d])
    assert "ping" in funcs
    assert funcs["ping"]() == "pong"
