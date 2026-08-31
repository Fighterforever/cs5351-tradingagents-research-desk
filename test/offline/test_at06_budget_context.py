"""AT-06 / FR-003 / NFR-003: LLM call budget and compact-context invariants.

A fake 3-call trajectory through the evidence recorder proves the budget blocks
a 4th request, usage covers exactly the calls actually made, a budget-stopped
run yields no approvable recommendation, and identity/date/price/constraints
survive compaction while repeated text is de-duplicated and history bounded.
"""

from __future__ import annotations

import pytest

from research_desk.budget import BudgetExhausted, BudgetTracker
from research_desk.evidence import EvidenceLog, EvidenceRecorder
from research_desk.graph_adapter import decide_proposal
from research_desk.models import CallUsage


def _fake_llm_end(recorder, input_tokens, output_tokens, text="ok"):
    from langchain_core.messages import AIMessage
    from langchain_core.outputs import ChatGeneration, LLMResult

    message = AIMessage(content=text, usage_metadata={
        "input_tokens": input_tokens, "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    })
    response = LLMResult(generations=[[ChatGeneration(message=message)]])
    recorder.on_llm_end(response)


def test_budget_blocks_fourth_call_after_limit_of_three():
    """After the 3rd call, the model wants a 4th; it must not start (NFR-003)."""
    log = EvidenceLog()
    budget = BudgetTracker(max_calls=3)
    recorder = EvidenceRecorder(log, budget)

    for i in range(3):
        recorder.on_chat_model_start({"id": "deepseek-chat"}, [["hello"]])
        _fake_llm_end(recorder, input_tokens=100 * (i + 1), output_tokens=20 * (i + 1))

    with pytest.raises(BudgetExhausted):
        recorder.on_chat_model_start({"id": "deepseek-chat"}, [["continue"]])  # 4th blocked

    usage = budget.summary()
    assert usage.calls == 3
    assert usage.input_tokens == 100 + 200 + 300  # only the 3 started calls
    assert usage.output_tokens == 20 + 40 + 60
    assert usage.total_tokens == 720
    assert usage.stop_reason == "budget_exhausted"
    llm_events = [e for e in log.events if e.kind == "llm_request"]
    assert len(llm_events) == 3  # the 4th was never recorded


def test_budget_propagates_through_real_chat_model():
    """The budget guard really stops the next LLM request (NFR-003).

    LangChain swallows callback-handler exceptions by default, so the
    EvidenceRecorder must opt in to propagating (``raise_error``). This test
    drives an actual chat model (not just the tracker) through the recorder and
    asserts the exhausted budget aborts the next request instead of silently
    proceeding.
    """
    from langchain_core.language_models.fake_chat_models import (
        FakeMessagesListChatModel,
    )
    from langchain_core.messages import AIMessage, HumanMessage

    assert EvidenceRecorder(EvidenceLog(), BudgetTracker()).raise_error is True, (
        "recorder must propagate its own exceptions"
    )
    log = EvidenceLog()
    budget = BudgetTracker(max_calls=1)
    recorder = EvidenceRecorder(log, budget)
    llm = FakeMessagesListChatModel(responses=[AIMessage(content="ok")])
    llm.callbacks = [recorder]

    llm.invoke([HumanMessage(content="hi")])
    assert budget.calls_started == 1
    assert budget.can_start() is False

    with pytest.raises(BudgetExhausted):
        llm.invoke([HumanMessage(content="should be refused")])  # blocked, not swallowed
    # The blocked request never completed a response.
    responses = [e for e in log.events if e.kind == "llm_response"]
    assert len(responses) == 1


def test_budget_usage_covers_actual_calls():
    budget = BudgetTracker(max_calls=2)
    budget.start_call()
    budget.record_usage(CallUsage(input_tokens=10, output_tokens=5))
    budget.start_call()
    budget.record_usage(CallUsage(input_tokens=20, output_tokens=15))
    usage = budget.summary()
    assert usage.calls == 2
    assert usage.input_tokens == 30
    assert usage.output_tokens == 20
    assert usage.total_tokens == 50


def test_budget_stop_never_approvable():
    """A budget-stopped (incomplete) run must not become an approvable proposal."""
    from test.fixtures.fixture_packs import stock_data_csv

    dates = ["2026-06-01", "2026-06-10"]
    snapshot = {
        "get_stock_data": {
            '{"end_date": "2026-06-10", "start_date": "2026-06-01", "symbol": "AAPL"}': stock_data_csv("AAPL", [99.0, 100.0], dates)
        }
    }
    assert decide_proposal(
        outcome="budget_stopped", signal="Buy", run_id="r", ticker="AAPL",
        trade_date="2026-06-10", snapshot=snapshot,
    ) is None
    assert decide_proposal(
        outcome="failed", signal="Buy", run_id="r", ticker="AAPL",
        trade_date="2026-06-10", snapshot=snapshot,
    ) is None
    # A completed, tradeable signal does produce a proposal (contrast).
    p = decide_proposal(
        outcome="completed", signal="Buy", run_id="r", ticker="AAPL",
        trade_date="2026-06-10", snapshot=snapshot,
    )
    assert p is not None and p.status.value == "PENDING_REVIEW"


def test_tool_events_recorded_through_recorder():
    log = EvidenceLog()
    budget = BudgetTracker(max_calls=None)
    recorder = EvidenceRecorder(log, budget)
    recorder.on_tool_start({}, '{"symbol": "AAPL"}')
    recorder.on_tool_end("csv...", name="get_stock_data")
    kinds = {e.kind for e in log.events}
    assert "tool_call" in kinds and "tool_result" in kinds


def test_compact_context_invariants():
    """Identity, date, price, constraints and task survive compaction (FR-003)."""
    from research_desk.context import ContextAssembler, StandingConstraints
    from research_desk.evidence import EvidencePackIO
    from research_desk.models import ContextMode

    pack = EvidencePackIO().import_pack("test/fixtures/packs/nvda_compact_memory")
    assembler = ContextAssembler(
        StandingConstraints(
            ticker="NVDA",
            trade_date="2026-06-10",
            identity={"company_name": "NVIDIA Corp", "sector": "Semiconductors"},
            prices={"last_close": 137.0},
            policy={
                "initial_cash": "USD 100000",
                "max_single_position": "10% of equity",
                "integer_shares": "yes",
                "no_shorting": "yes",
            },
            current_task="Produce the research-desk analysis of NVDA on 2026-06-10.",
        )
    )
    baseline = assembler.assemble_from_entries(pack.input.memory_used, ContextMode.BASELINE)
    compact = assembler.assemble_from_entries(pack.input.memory_used, ContextMode.COMPACT)

    assert compact.deduplicated >= 1  # repeated REFLECTION block removed
    assert compact.chars <= baseline.chars  # compact never grows the context
    for needle in ("NVDA", "2026-06-10", "137.0", "USD 100000", "10% of equity", "no_shorting"):
        assert needle in compact.text
    assert "Momentum signals worked well" in compact.text
    assert "REFLECTION:\nREFLECTION" not in compact.text  # no double header

    # On a genuinely long, distinct history, compact is strictly smaller
    # (older discussion is cut at the tighter compact cap).
    long_assembler = ContextAssembler(assembler.constraints)
    long_text = "\n\n".join(f"report {i}: distinct analysis body number {i}" for i in range(400))
    c = long_assembler.assemble(long_text, ContextMode.COMPACT)
    b = long_assembler.assemble(long_text, ContextMode.BASELINE)
    assert c.truncated is True
    assert c.chars < b.chars
