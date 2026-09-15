from grok_local_agent_kit import Team, Blackboard, Member, demo_team, __version__
from grok_local_agent_kit.team import ALLOWED_KINDS


def test_version():
    assert __version__ == "0.28.0"


def test_blackboard_post_and_dump():
    board = Blackboard()
    board.post("alice", "hello", kind="note", tags=["hi"])
    board.post("bob", "world", kind="claim")
    text = board.dump()
    assert "alice/note" in text
    assert "bob/claim" in text
    assert len(board) == 2
    assert board.recent(1)[0].author == "bob"


def test_unknown_kind_falls_back():
    board = Blackboard()
    p = board.post("sys", "x", kind="not-a-kind")
    assert p.kind == "note"
    assert "note" in ALLOWED_KINDS


def test_team_run_llm_free():
    out = demo_team("Stay offline.")
    assert "Stay offline." in out
    assert "coordinator/" in out
    assert "researcher/" in out
    assert "operator/" in out
    assert "team finished" in out


def test_custom_member():
    seen = {}

    def handler(board, goal):
        seen["goal"] = goal
        return "custom-ok"

    team = Team(members=[Member("custom", "do the thing", handler)])
    text = team.run("ping", rounds=1)
    assert seen["goal"] == "ping"
    assert "custom-ok" in text
    assert "members=custom" in team.status()
