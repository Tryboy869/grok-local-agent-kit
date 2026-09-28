"""v0.40 — local model catalog."""

from pathlib import Path

from grok_local_agent_kit.catalog import (
    Catalog,
    ModelEntry,
    collect,
    demo_catalog,
    format_catalog,
    load_catalog,
    write_catalog,
)


def _fake_fetch(url: str, timeout: float):
    if "11434" in url:
        return {
            "models": [
                {"name": "llama3.2:latest", "size": 2048, "digest": "abc"},
                {"name": "nomic-embed-text", "size": 512},
            ]
        }
    if "1234" in url:
        return {"data": [{"id": "qwen2.5-7b", "owned_by": "lmstudio"}]}
    raise RuntimeError(f"unexpected url {url}")


def _down_fetch(url: str, timeout: float):
    raise ConnectionError(f"refused {url}")


def test_collect_injected():
    cat = collect(fetch=_fake_fetch)
    assert cat.backends["ollama"]["reachable"] is True
    assert cat.backends["lmstudio"]["reachable"] is True
    assert cat.names("ollama") == ["llama3.2:latest", "nomic-embed-text"]
    assert cat.names("lmstudio") == ["qwen2.5-7b"]
    picked = cat.pick("ollama", prefer="llama3.2")
    assert picked is not None and picked.name.startswith("llama3.2")
    text = format_catalog(cat)
    assert "llama3.2:latest" in text
    assert "qwen2.5-7b" in text


def test_collect_down():
    cat = collect(fetch=_down_fetch)
    assert cat.backends["ollama"]["reachable"] is False
    assert cat.models == []
    assert cat.pick() is None
    assert "down" in format_catalog(cat)


def test_write_load_demo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dest = write_catalog("catalog.json", catalog=collect(fetch=_fake_fetch))
    assert dest.exists()
    loaded = load_catalog(dest)
    assert isinstance(loaded, Catalog)
    assert len(loaded.models) == 3
    assert all(isinstance(m, ModelEntry) for m in loaded.models)
    text = demo_catalog("catalog.json", fetch=_fake_fetch)
    assert "wrote=" in text
    assert Path("catalog.json").exists()
