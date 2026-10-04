"""v0.44 job ledger — no network, no daemon."""

from pathlib import Path

from grok_local_agent_kit.jobs import JobLedger, JobSpec, due, load_ledger, save_ledger, tick


def _ledger() -> JobLedger:
    return JobLedger(
        jobs=[
            JobSpec(
                name="digest",
                every_s=100,
                workflow={
                    "name": "digest",
                    "steps": [
                        {"tool": "write_file", "arguments": {"path": "out.txt", "content": "ran\n"}},
                        {"tool": "web_search", "arguments": {"query": "local"}},
                    ],
                },
            )
        ]
    )


def test_tick_fires_once_then_skips(tmp_path: Path):
    ledger = _ledger()
    first = tick(ledger, tmp_path, now=1_000, search=lambda q: f"hit:{q}")
    assert first["fired"] == ["digest"]
    assert first["ok"] is True
    assert (tmp_path / "out.txt").read_text(encoding="utf-8") == "ran\n"
    second = tick(ledger, tmp_path, now=1_050, search=lambda q: "nope")
    assert second["fired"] == []
    assert second["skipped"] == ["digest"]
    assert due(ledger, 1_100)[0].name == "digest"


def test_disabled_job_never_fires(tmp_path: Path):
    ledger = _ledger()
    ledger.jobs[0].enabled = False
    result = tick(ledger, tmp_path, now=5_000)
    assert result["fired"] == []
    assert not (tmp_path / "out.txt").exists()


def test_roundtrip_and_state(tmp_path: Path):
    path = tmp_path / "jobs.json"
    save_ledger(_ledger(), path)
    loaded = load_ledger(path)
    tick(loaded, tmp_path / "ws", now=9, search=lambda q: "ok", persist=True)
    again = load_ledger(path)
    assert again.runs["digest"]["runs"] == 1
    assert again.runs["digest"]["last_ok"] is True
