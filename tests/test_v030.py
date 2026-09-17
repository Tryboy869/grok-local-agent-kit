from grok_local_agent_kit.roster import (
    MemberSpec,
    bind_roster,
    format_roster,
    load_roster,
    save_roster,
    specs_from_team,
    team_from_roster,
)
from grok_local_agent_kit.team import Team


def test_roster_json_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    specs = [
        MemberSpec("lead", "Coordinate.", provider="ollama", model="llama3.2", role="coordinator"),
        MemberSpec("ops", "Apply changes.", role="operator"),
    ]
    dest = save_roster(specs, "roster.json")
    assert dest.exists()
    loaded = load_roster(dest)
    assert loaded[0].model == "llama3.2"
    assert loaded[1].name == "ops"
    text = format_roster(loaded)
    assert "lead" in text and "llama3.2" in text


def test_roster_sqlite_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    specs = [MemberSpec("researcher", "Find facts.", provider="lmstudio", model="qwen")]
    dest = save_roster(specs, "roster.sqlite")
    loaded = load_roster(dest)
    assert loaded[0].provider == "lmstudio"
    assert loaded[0].model == "qwen"


def test_team_from_roster_runs_offline(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    specs = [MemberSpec("solo", "Echo the goal.")]
    save_roster(specs, "roster.json")
    team = team_from_roster("roster.json")
    out = team.run("ship v0.30", rounds=1)
    assert "ship v0.30" in out
    assert "solo" in out
    saved = specs_from_team(team)
    assert saved[0].name == "solo"


def test_bind_roster_stub_without_live(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    specs = [MemberSpec("bot", "Think.", provider="ollama", model="llama3.2")]
    members = bind_roster(specs, live=False)
    team = Team(members=members)
    dump = team.run("offline only")
    assert "offline only" in dump
    live_members = bind_roster(specs, live=True, factory=None)
    team2 = Team(members=live_members)
    out = team2.run("bind stub")
    assert "bind stub" in out
    assert "bot" in out
