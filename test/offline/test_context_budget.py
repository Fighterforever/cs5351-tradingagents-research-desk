"""ADR-004 whole-input context budget.

Focused fake-model tests: unchanged input below the trigger, successful
compaction above it, refusal before any provider call when mandatory evidence
cannot fit, intact assistant/tool-call pairs, and propagation of configured
caps into both graph delegates.
"""

from __future__ import annotations

import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from research_desk.budget import ContextBudgetExceeded, estimate_input_units
from research_desk.config import (
    DEFAULT_CONTEXT_MAX_TOKENS,
    DEFAULT_CONTEXT_TRIGGER_TOKENS,
    ResearchDeskSettings,
)
from research_desk.eval.compact_delegate import GroundingDelegate, wrap_for_mode


class _RecordingModel:
    def __init__(self) -> None:
        self.calls: list = []

    def invoke(self, input, config=None, **kwargs):
        self.calls.append(input)
        return AIMessage(content="ok")

    def bind_tools(self, tools, **kwargs):
        return _RecordingBound(self)

    def with_structured_output(self, schema, **kwargs):
        return _RecordingStructured(self)


class _RecordingBound:
    def __init__(self, model: _RecordingModel) -> None:
        self.model = model

    def __call__(self, input):
        self.model.calls.append(input)
        return AIMessage(
            content="",
            tool_calls=[
                {"name": "get_stock_data", "args": {}, "id": "call_1", "type": "tool_call"}
            ],
        )


class _RecordingStructured:
    def __init__(self, model: _RecordingModel) -> None:
        self.model = model

    def __call__(self, input):
        self.model.calls.append(input)
        return {"ok": True}


def _delegate(model, *, mode="baseline", cap=2000, trigger=1000) -> GroundingDelegate:
    return GroundingDelegate(
        model,
        context_mode=mode,
        common_grounding="GROUNDING",
        context_max_tokens=cap,
        context_trigger_tokens=trigger,
    )


def _contents(messages) -> list[str]:
    return [m.content if isinstance(m.content, str) else str(m.content) for m in messages]


def test_defaults_are_authoritative_config_values():
    settings = ResearchDeskSettings()
    assert DEFAULT_CONTEXT_MAX_TOKENS == 96000
    assert DEFAULT_CONTEXT_TRIGGER_TOKENS == 72000
    assert settings.context_max_tokens == 96000
    assert settings.context_trigger_tokens == 72000


def test_below_trigger_preserves_messages_unchanged():
    model = _RecordingModel()
    history = [
        SystemMessage(content="system constraints"),
        HumanMessage(content="older discussion"),
        HumanMessage(content="Produce the current task"),
    ]
    _delegate(model, cap=100000, trigger=90000).invoke(history)

    received = model.calls[0]
    assert received[0].content == "GROUNDING"
    assert _contents(received[1:]) == _contents(history)
    assert all(a is b for a, b in zip(received[1:], history, strict=True))


def test_above_trigger_compacts_old_prose_but_keeps_constraints_and_task():
    model = _RecordingModel()
    history = [
        SystemMessage(content="STANDING ANALYSIS CONSTRAINTS: never short"),
        HumanMessage(content="old prose " * 2000),
        AIMessage(content="old answer " * 2000),
        HumanMessage(content="Produce the current task"),
    ]
    delegate = _delegate(model, cap=3000, trigger=1000)
    assert estimate_input_units(history) > 1000

    delegate.invoke(history)

    received = model.calls[0]
    texts = _contents(received)
    assert texts[0] == "GROUNDING"
    assert any("STANDING ANALYSIS CONSTRAINTS" in t for t in texts)
    assert any("Produce the current task" in t for t in texts)
    assert any("[... context compacted ...]" in t for t in texts)
    assert not any("old prose " * 100 in t for t in texts)
    assert estimate_input_units(received) <= 3000


def test_budget_observer_records_conservative_units():
    observations: list[dict] = []
    model = _RecordingModel()
    history = [
        HumanMessage(content="old prose " * 2000),
        HumanMessage(content="Produce the current task"),
    ]
    delegate = GroundingDelegate(
        model,
        context_mode="baseline",
        common_grounding="GROUNDING",
        context_max_tokens=3000,
        context_trigger_tokens=1000,
        budget_observer=observations.append,
    )

    delegate.invoke(history)

    assert len(observations) == 1
    observation = observations[0]
    assert observation["metric"] == "utf8_upper_bound"
    assert observation["before_units"] > observation["after_units"]
    assert observation["trigger"] == 1000
    assert observation["cap"] == 3000
    assert observation["compacted"] is True


def test_uncompressible_fact_evidence_refused_before_client_call():
    model = _RecordingModel()
    history = [
        HumanMessage(content="last_close: 100.0 " + "x" * 5000),
        HumanMessage(content="Produce the current task"),
    ]
    delegate = _delegate(model, cap=1000, trigger=500)

    with pytest.raises(ContextBudgetExceeded) as excinfo:
        delegate.invoke(history)

    assert excinfo.value.stop_reason == "context_budget_exhausted"
    assert excinfo.value.estimated_tokens > 1000
    assert model.calls == []


def test_paired_tool_call_and_tool_message_survive_compaction():
    model = _RecordingModel()
    history = [
        HumanMessage(content="old prose " * 2000),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_stock_data",
                    "args": {"symbol": "MSFT"},
                    "id": "call_abc",
                    "type": "tool_call",
                }
            ],
        ),
        ToolMessage(content="csv evidence", tool_call_id="call_abc"),
        HumanMessage(content="Produce the current task"),
    ]
    delegate = _delegate(model, cap=3000, trigger=1000)

    delegate.invoke(history)

    received = model.calls[0]
    ai = next(m for m in received if isinstance(m, AIMessage) and m.tool_calls)
    tool = next(m for m in received if isinstance(m, ToolMessage))
    assert ai.tool_calls[0]["id"] == "call_abc"
    assert tool.tool_call_id == "call_abc"
    assert tool.content == "csv evidence"


def test_custom_settings_propagate_to_both_graph_delegates(monkeypatch):
    from research_desk import graph_adapter

    class _FakeWorkflow:
        def compile(self):
            return object()

    class _FakeSetup:
        def __init__(self, quick, deep, tools, logic):
            self.quick, self.deep = quick, deep

        def setup_graph(self, analysts):
            return _FakeWorkflow()

    class _FakeReflector:
        def __init__(self, llm):
            self.llm = llm

    class _FakeSignalProcessor:
        def __init__(self, llm):
            self.llm = llm

    class _FakeGraph:
        def __init__(self, *args, **kwargs):
            self.quick_thinking_llm = _RecordingModel()
            self.deep_thinking_llm = _RecordingModel()
            self.tool_nodes = {}
            self.conditional_logic = object()

    import tradingagents.graph.reflection as reflection_mod
    import tradingagents.graph.setup as setup_mod
    import tradingagents.graph.signal_processing as signal_mod

    monkeypatch.setattr(graph_adapter, "EvidenceTradingGraph", _FakeGraph)
    monkeypatch.setattr(reflection_mod, "Reflector", _FakeReflector)
    monkeypatch.setattr(setup_mod, "GraphSetup", _FakeSetup)
    monkeypatch.setattr(signal_mod, "SignalProcessor", _FakeSignalProcessor)

    settings = ResearchDeskSettings(context_max_tokens=1234, context_trigger_tokens=999)
    runner = graph_adapter.ResearchRunner(settings)
    graph = runner._build_graph(
        {},
        None,
        None,
        frozen_snapshot={},
        frozen_identity=None,
        ticker="MSFT",
        trade_date="2026-06-10",
    )

    for llm in (graph.quick_thinking_llm, graph.deep_thinking_llm):
        assert llm.context_max_tokens == 1234
        assert llm.context_trigger_tokens == 999


def test_wrap_for_mode_defaults_match_authoritative_values():
    delegate = wrap_for_mode(_RecordingModel(), "baseline", common_grounding="G")
    assert delegate.context_max_tokens == DEFAULT_CONTEXT_MAX_TOKENS
    assert delegate.context_trigger_tokens == DEFAULT_CONTEXT_TRIGGER_TOKENS
