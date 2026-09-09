"""v0.21 tests — tool cache + telemetry. No live LLM."""

from __future__ import annotations

from grok_local_agent_kit.cache import ToolCache, cache_key, cached_execute, reset_cache
from grok_local_agent_kit.telemetry import Telemetry, reset_telemetry, timed_execute


def test_cache_key_stable():
    a = cache_key("calculator", {"expression": "2+2"})
    b = cache_key("calculator", {"expression": "2+2"})
    c = cache_key("calculator", {"expression": "3+3"})
    assert a == b
    assert a != c


def test_cache_hit_and_miss():
    cache = ToolCache(ttl=30)
    calls = {"n": 0}

    def runner(name, args):
        calls["n"] += 1
        return str(eval(args["expression"]))  # noqa: S307 — test only

    out1 = cached_execute("calculator", {"expression": "2+2"}, runner, cache)
    out2 = cached_execute("calculator", {"expression": "2+2"}, runner, cache)
    assert out1 == "4"
    assert out2 == "4"
    assert calls["n"] == 1
    assert cache.hits == 1
    assert cache.misses == 1


def test_cache_ttl_expiry():
    cache = ToolCache(ttl=-1)
    cache.put("t", {}, "old")
    assert cache.get("t", {}) is None


def test_cache_clear_and_disable():
    cache = reset_cache()
    cache.put("t", {"a": 1}, "v")
    assert cache.clear() == 1
    cache.enabled = False
    cache.put("t", {}, "x")
    assert cache.get("t", {}) is None


def test_telemetry_summary():
    tel = reset_telemetry()
    tel.record("calculator", 1.5, cached=False)
    tel.record("calculator", 0.0, cached=True)
    tel.record("web_search", 12.0, cached=False, ok=False)
    s = tel.summary()
    assert s["calls"] == 3
    assert s["tools"]["calculator"]["cached"] == 1
    assert s["tools"]["web_search"]["errors"] == 1


def test_timed_execute_records_ms():
    tel = Telemetry()
    out = timed_execute("echo", {}, lambda n, a: "ok", telemetry=tel)
    assert out == "ok"
    assert tel.events[0].name == "echo"
    assert tel.events[0].ms >= 0
