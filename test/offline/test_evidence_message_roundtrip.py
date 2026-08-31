"""FR-001 / SEC-001 regression: real message values survive evidence export/import.

A real AAPL pilot export failed on a nested LangChain ``HumanMessage`` in
``final_state.json``, and ``sanitize_secrets`` redacted ``input_tokens`` /
``output_tokens`` merely because a key contains "token". Both directory and ZIP
exports must now convert actual Pydantic message values (HumanMessage,
AIMessage, ToolMessage) to JSON-native dicts via ``model_dump(mode="json")``,
preserve message type/content/tool id/usage metadata and numeric event/call
token metrics, redact only genuine credential fields, and still replay offline
with networking blocked.
"""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from research_desk.models import CallRecord, EvidencePack, UsageSummary

_NETWORK_BLOCKED_REPLAY = """
import json, socket, sys
# Block real network I/O (the established test approach): any socket that
# actually tries to connect raises, proving replay performs zero external calls.
def _block(*a, **k):
    raise OSError("network blocked during offline replay")
socket.socket.connect = _block
socket.socket.sendall = _block
socket.socket.recv = _block
socket.getaddrinfo = _block
from research_desk.models import LedgerState
from research_desk.replay import ReplayEngine
from research_desk.policy import policy_bounds
engine = ReplayEngine()
pack = engine.load(sys.argv[1])
res = engine.replay(pack, sys.argv[2], ledger=None)
bounds = None
if res.pack.proposal is not None and res.pack.proposal.price is not None:
    bounds = policy_bounds(LedgerState(cash=100000.0), res.pack.proposal.ticker, res.pack.proposal.price)
print(json.dumps({
    "signal": res.signal,
    "manifest_signal": res.pack.manifest.signal,
    "reports": len(res.report_files),
    "external_calls": res.external_calls,
    "max_by_cap": None if bounds is None else bounds["max_by_cap"],
    "max_by_cash": None if bounds is None else bounds["max_by_cash"],
}))
"""


def _augmented_pack(aapl_pack: EvidencePack) -> EvidencePack:
    """aapl_buy_complete with real messages, numeric usage and a credential field.

    ``final_state`` gains a LangChain message list (HumanMessage/AIMessage with
    a tool call and usage metadata/ToolMessage carrying the tool call id), a
    credential field, and the event/call usage is set to real numeric values so
    the roundtrip proves measurements survive redaction.
    """
    pack = aapl_pack.model_copy(deep=True)
    final_state = dict(aapl_pack.final_state)
    final_state["messages"] = [
        HumanMessage(content="Operator: analyze AAPL.", additional_kwargs={"source": "operator"}),
        AIMessage(
            content="Market research plan locked.",
            tool_calls=[
                {
                    "name": "get_stock_data",
                    "args": {"symbol": "AAPL", "start_date": "2026-06-01", "end_date": "2026-06-10"},
                    "id": "call_tool_1",
                    "type": "tool_call",
                }
            ],
            usage_metadata={"input_tokens": 121, "output_tokens": 42, "total_tokens": 163},
            response_metadata={"token_usage": {"prompt_tokens": 121, "completion_tokens": 42, "total_tokens": 163}},
        ),
        ToolMessage(content="AAPL 8-day series returned.", tool_call_id="call_tool_1"),
    ]
    final_state["api_key"] = "sk-test-secret"
    pack.final_state = final_state

    events = [ev.model_copy(deep=True) for ev in aapl_pack.events]
    for ev in events:
        if ev.kind == "llm_response":
            ev.payload = {"input_tokens": 121, "output_tokens": 42, "response": "..."}
    pack.events = events
    pack.calls = [
        CallRecord(
            seq=1,
            ts="2026-06-10T00:00:00Z",
            kind="llm",
            node="market_analyst",
            model="deepseek-chat",
            input_tokens=121,
            output_tokens=42,
            response="...",
        )
    ]
    pack.usage = UsageSummary(calls=1, input_tokens=121, output_tokens=42, total_tokens=163, stop_reason="completed")
    return pack


@pytest.mark.parametrize("as_zip", [False, True], ids=["directory", "zip"])
def test_evidence_message_roundtrip(as_zip, aapl_pack, pack_io, tmp_path):
    """Message type/content/tool id/usage survive dir+ZIP export/import; secrets redact."""
    pack = _augmented_pack(aapl_pack)
    io = pack_io

    if as_zip:
        source = tmp_path / "evidence.zip"
        io.export_zip(pack, source)
        with zipfile.ZipFile(source) as zf:
            raw_final_state = zf.read("final_state.json").decode("utf-8")
            raw_events = zf.read("events.jsonl").decode("utf-8")
            raw_calls = zf.read("calls.json").decode("utf-8")
    else:
        source = tmp_path / "evidence_dir"
        io.export(pack, source)
        raw_final_state = (source / "final_state.json").read_text(encoding="utf-8")
        raw_events = (source / "events.jsonl").read_text(encoding="utf-8")
        raw_calls = (source / "calls.json").read_text(encoding="utf-8")

    imported = io.import_pack(source)

    # Real messages became JSON-native structured dicts with type/content intact.
    msgs = imported.final_state["messages"]
    assert [m["type"] for m in msgs] == ["human", "ai", "tool"]
    assert msgs[0]["content"] == "Operator: analyze AAPL."
    assert msgs[0]["additional_kwargs"] == {"source": "operator"}
    assert msgs[1]["content"] == "Market research plan locked."
    assert msgs[1]["tool_calls"][0]["id"] == "call_tool_1"
    assert msgs[1]["tool_calls"][0]["name"] == "get_stock_data"
    assert msgs[1]["tool_calls"][0]["args"] == {"symbol": "AAPL", "start_date": "2026-06-01", "end_date": "2026-06-10"}
    assert msgs[1]["usage_metadata"] == {"input_tokens": 121, "output_tokens": 42, "total_tokens": 163}
    assert msgs[1]["response_metadata"]["token_usage"]["prompt_tokens"] == 121
    assert msgs[2]["type"] == "tool"
    assert msgs[2]["tool_call_id"] == "call_tool_1"
    assert msgs[2]["content"] == "AAPL 8-day series returned."

    # Credential field is redacted on disk and after import; no secret leaks.
    assert imported.final_state["api_key"] == "**REDACTED**"
    assert "sk-test-secret" not in raw_final_state

    # Numeric usage/count fields are evidence, not credentials.
    response_event = next(ev for ev in imported.events if ev.kind == "llm_response")
    assert response_event.payload["input_tokens"] == 121
    assert response_event.payload["output_tokens"] == 42
    assert imported.usage.input_tokens == 121
    assert imported.usage.output_tokens == 42
    assert imported.usage.total_tokens == 163
    assert imported.calls[0].input_tokens == 121
    assert imported.calls[0].output_tokens == 42
    assert "**REDACTED**" not in raw_events
    assert "**REDACTED**" not in raw_calls

    # The corrected pack still replays offline with networking blocked.
    out_dir = tmp_path / "reports"
    out_dir.mkdir()
    proc = subprocess.run(
        [sys.executable, "-c", _NETWORK_BLOCKED_REPLAY, str(source), str(out_dir)],
        capture_output=True,
        text=True,
        timeout=60,
        env={"PYTHONPATH": ".", "PATH": "/usr/bin:/bin"},
    )
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout.strip().splitlines()[-1])
    assert result["external_calls"] == 0
    assert result["signal"] == "Buy"
    assert result["signal"] == result["manifest_signal"]
    assert result["max_by_cap"] == 100
    assert result["max_by_cash"] == 1000
    assert result["reports"] >= 1
