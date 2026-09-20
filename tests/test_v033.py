from grok_local_agent_kit.approvals import ApprovalDenied, ApprovalGate
from grok_local_agent_kit.hooks import HookBus
from grok_local_agent_kit.react_gate import (
    attach_approval_gate,
    check_tool,
    gated_execute,
    tool_block_message,
)


def test_gated_execute_allow_and_deny():
    gate = ApprovalGate(allow=["calculator"], deny=["run_shell"], default="pending")

    def ok():
        return "42"

    def boom():
        return "should-not-run"

    assert gated_execute(gate, "calculator", ok) == "42"
    blocked = gated_execute(gate, "run_shell", boom)
    assert blocked.startswith("blocked by approval gate")
    pending = gated_execute(gate, "web_search", boom)
    assert "pending" in pending


def test_attach_hook_enforces_via_require():
    gate = ApprovalGate(deny=["shell"], default="approved")
    bus = HookBus()
    attach_approval_gate(bus, gate, actor="tester")
    check_tool(gate, "calculator")
    try:
        check_tool(gate, "shell")
        raise AssertionError("expected deny")
    except ApprovalDenied as exc:
        assert "denied" in str(exc)


def test_tool_block_message():
    msg = tool_block_message(ApprovalDenied("[denied] A001 tool:shell actor=agent"))
    assert msg.startswith("blocked by approval gate")
