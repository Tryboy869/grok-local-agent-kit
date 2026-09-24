from pathlib import Path

import pytest

from grok_local_agent_kit.health import (
    CLOSED,
    HALF_OPEN,
    OPEN,
    HealthBoard,
    demo_health,
    format_board,
    load_board,
    save_board,
)


def test_trip_opens_after_threshold():
    board = HealthBoard(threshold=2, cooldown_s=60)
    board.failure("ollama", "timeout")
    assert board.breaker("ollama").state == CLOSED
    board.failure("ollama", "timeout")
    assert board.breaker("ollama").state == OPEN
    assert board.allow("ollama") is False


def test_cooldown_moves_to_half_open_then_close():
    board = HealthBoard(threshold=1, cooldown_s=10)
    now = 1_000.0
    board.failure("lmstudio", "down", now=now)
    assert board.allow("lmstudio", now=now + 1) is False
    assert board.allow("lmstudio", now=now + 11) is True
    assert board.breaker("lmstudio").state == HALF_OPEN
    board.success("lmstudio")
    assert board.breaker("lmstudio").state == CLOSED
    assert board.allow("lmstudio") is True


def test_half_open_failure_reopens():
    board = HealthBoard(threshold=1, cooldown_s=5)
    now = 50.0
    board.failure("x", "boom", now=now)
    board.allow("x", now=now + 6)
    board.failure("x", "still", now=now + 6)
    assert board.breaker("x").state == OPEN


def test_persist_roundtrip(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    board = HealthBoard(threshold=3, cooldown_s=9)
    board.success("ollama")
    board.trip("lmstudio", error="manual")
    dest = save_board(board, "health.json")
    loaded = load_board(dest)
    assert loaded.breaker("ollama").state == CLOSED
    assert loaded.breaker("lmstudio").state == OPEN
    assert loaded.breaker("lmstudio").last_error == "manual"
    text = format_board(loaded)
    assert "ollama" in text and "lmstudio" in text


def test_path_escapes(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="escapes"):
        save_board(HealthBoard(), "/tmp/outside-health.json")


def test_demo_offline(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    text = demo_health("health.json")
    assert "ollama" in text and "lmstudio" in text
    assert Path("health.json").exists()
