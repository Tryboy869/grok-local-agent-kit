from grok_local_agent_kit.guardrails import ToolGuard
from grok_local_agent_kit.planner import plan_add, plan_clear, plan_done, plan_list
from grok_local_agent_kit.scheduler import Scheduler
from grok_local_agent_kit.serve import serve

import json
import threading
import time
from http.client import HTTPConnection


def test_guard_allow_deny():
    g = ToolGuard(allow={"a", "b"}, deny={"b"}, timeout_s=1)
    assert g.check("a") is None
    assert "deny" in (g.check("b") or "").lower()
    assert "allow" in (g.check("c") or "").lower()


def test_guard_timeout():
    g = ToolGuard(timeout_s=0.1)

    def slow(**_):
        time.sleep(1)
        return "late"

    out = g.run("x", slow, {})
    assert "timed out" in out


def test_planner(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    plan_clear(done_only=False)
    assert "Added" in plan_add("one")
    assert "Added" in plan_add("two")
    listing = plan_list()
    assert "#1" in listing and "#2" in listing
    assert "Marked #1" in plan_done(1)
    open_items = plan_list("open")
    assert "#2" in open_items and "#1" not in open_items


def test_scheduler():
    n = {"v": 0}

    def inc():
        n["v"] += 1
        return str(n["v"])

    s = Scheduler()
    s.add("inc", 0.05, inc)
    s.loop(ticks=4, sleep_s=0.02)
    assert n["v"] >= 2
    assert "inc" in s.describe()


def test_serve_health():
    class Fake:
        last_trace = []

        def run(self, prompt):
            return "R:" + prompt

        def chat(self, prompt):
            return "C:" + prompt

        def list_registered_tools(self):
            return ["calculator"]

        def close(self):
            return None

    httpd = serve("127.0.0.1", 0, agent_factory=Fake)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.05)
    conn = HTTPConnection("127.0.0.1", port, timeout=3)
    conn.request("GET", "/health")
    body = json.loads(conn.getresponse().read().decode())
    assert body["ok"] is True
    conn.request(
        "POST",
        "/v1/chat",
        body=json.dumps({"prompt": "hi"}),
        headers={"Content-Type": "application/json"},
    )
    chat = json.loads(conn.getresponse().read().decode())
    conn.close()
    httpd.shutdown()
    assert chat["text"] == "R:hi"
