from pathlib import Path

from grok_local_agent_kit.persist import load_board, save_board
from grok_local_agent_kit.team import Blackboard, Team


def test_jsonl_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    team = Team()
    team.run("ship offline agents", rounds=1)
    dest = save_board(team.board, "board.jsonl")
    assert dest.exists()
    restored = load_board(dest)
    assert len(restored) == len(team.board)
    dump = restored.dump()
    assert "ship offline agents" in dump
    assert "coordinator" in dump


def test_sqlite_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    board = Blackboard()
    board.post("system", "hello sqlite", kind="goal")
    board.post("researcher", "fact", kind="claim", tags=["src"])
    dest = save_board(board, "board.sqlite")
    restored = load_board(dest)
    posts = restored.recent(10)
    assert posts[0].body == "hello sqlite"
    assert posts[1].tags == ["src"]


def test_append_after_reload(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    team = Team()
    team.run("first", rounds=1)
    save_board(team.board, Path("board.jsonl"))
    board = load_board("board.jsonl")
    team2 = Team(board=board)
    team2.run("second", rounds=1)
    save_board(team2.board, "board.jsonl")
    again = load_board("board.jsonl")
    dump = again.dump()
    assert "first" in dump and "second" in dump
