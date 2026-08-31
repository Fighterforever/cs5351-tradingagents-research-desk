"""Focused fake-model test for the COMMON grounding layer in BOTH modes.

The plain ``GroundingDelegate`` must deliver the same common source/date/identity
constraints to the *real* client through every path the graph actually uses —
plain ``invoke``, ``bind_tools`` and ``with_structured_output`` — while baseline
keeps the substantive history unchanged (grounding is the only addition).

The common grounding is built from the real MSFT frozen case, so the assertions
check the actual per-case ticker, legal company identity, analysis date, frozen
close and both source IDs (``src-msft`` official news, ``market-msft`` market CSV).
"""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel

from research_desk.context import build_common_grounding
from research_desk.eval.compact_delegate import GroundingDelegate
from research_desk.eval.frozen_provider import FrozenMarketProvider
from research_desk.graph_adapter import _available_sources_from_provider

_CASE = FrozenMarketProvider("MSFT")
_AVAILABLE = _available_sources_from_provider(_CASE, "MSFT", _CASE.case["analysis_date"])
_GROUNDING = build_common_grounding("MSFT", _CASE.case["analysis_date"], _AVAILABLE)

_HISTORY = [SystemMessage(content="You are a helpful trading analyst."), HumanMessage(content="Analyze Microsoft.")]


class _DummyResult(BaseModel):
    support: float = 0.0
    rationale: str = ""


class _RecordingModel:
    """A minimal stand-in for the real LangChain client that records inputs."""

    def __init__(self) -> None:
        self.invoked: list = []
        self.bound_invoked: list = []
        self.structured_invoked: list = []

    def invoke(self, input, config=None, **kwargs):
        self.invoked.append(input)
        return AIMessage(content="plain ok")

    def bind_tools(self, tools, **kwargs):
        return _RecordingBound(self, tools, **kwargs)

    def with_structured_output(self, schema, **kwargs):
        return _RecordingStructured(self, schema, **kwargs)


class _RecordingBound:
    def __init__(self, model, tools, **kwargs):
        self.model = model

    def __call__(self, input):
        self.model.bound_invoked.append(input)
        return AIMessage(
            content="",
            tool_calls=[
                {"name": "get_stock_data", "args": {"symbol": "MSFT"}, "id": "call_1", "type": "tool_call"}
            ],
        )


class _RecordingStructured:
    def __init__(self, model, schema, **kwargs):
        self.model = model

    def __call__(self, input):
        self.model.structured_invoked.append(input)
        return _DummyResult(support=0.9, rationale="grounded")


def _texts(messages) -> list[str]:
    return [m.content if isinstance(m.content, str) else str(m.content) for m in messages]


def _grounding_constraints(grounding: str) -> None:
    """The common layer must carry real per-case source/date/identity facts."""
    for needle in (
        "MSFT",
        "Microsoft Corporation",
        "COMMON GROUNDING LAYER",
        "src-msft",
        "market-msft",
        "Analysis date:",
        "Frozen latest close:",
        "CITATION & GROUNDING RULES",
    ):
        assert needle in grounding, f"grounding missing {needle!r}"


def test_grounding_contains_real_facts():
    _grounding_constraints(_GROUNDING)


def test_no_invented_msft_registry_or_example_numbers():
    """No-corpus / another ticker must not invent MSFT numbers or a source registry."""
    # An empty available_sources (ordinary live path) must not fabricate src-/market- IDs.
    empty = build_common_grounding("AAPL", "2026-07-31", {})
    assert "SOURCE-ID REGISTRY" not in empty
    assert "src-msft" not in empty
    assert "src-aapl" not in empty
    assert "market-msft" not in empty
    assert "market-aapl" not in empty
    assert "USD90.0B" not in empty
    assert "76.3" not in empty
    assert "Microsoft Corporation" not in empty
    # A real non-MSFT corpus uses only its own real source IDs, not MSFT's.
    provider = FrozenMarketProvider("NVDA")
    avail = _available_sources_from_provider(provider, "NVDA", provider.case["analysis_date"])
    nvda = build_common_grounding("NVDA", provider.case["analysis_date"], avail)
    assert "src-nvda" in nvda
    assert "market-nvda" in nvda
    assert "MSFT" not in nvda
    assert "USD90.0B" not in nvda
    assert "76.3" not in nvda


def _assert_grounded_first(received) -> None:
    """The first message the real client sees is the common grounding SystemMessage."""
    assert isinstance(received[0], SystemMessage)
    assert received[0].content == _GROUNDING


def _assert_baseline_history_intact(received) -> None:
    """After the grounding header, the substantive history is byte-for-byte unchanged."""
    assert len(received) == 1 + len(_HISTORY)
    for idx, original in enumerate(_HISTORY, start=1):
        assert received[idx].type == original.type
        assert received[idx].content == original.content


def _delegate(mode: str) -> GroundingDelegate:
    return GroundingDelegate(
        _RecordingModel(),
        context_mode=mode,
        common_grounding=_GROUNDING,
    )


def test_plain_invoke_grounding_reaches_real_client_both_modes():
    for mode in ("baseline", "compact"):
        model = _RecordingModel()
        delegate = GroundingDelegate(model, context_mode=mode, common_grounding=_GROUNDING)
        delegate.invoke(_HISTORY)
        assert model.invoked, f"{mode}: real client was never invoked"
        received = model.invoked[0]
        _assert_grounded_first(received)
        assert "src-msft" in _texts(received)[0]
        if mode == "baseline":
            _assert_baseline_history_intact(received)
        else:
            # Compact also injects grounding and keeps the substantive body.
            texts = _texts(received)
            assert any("Analyze Microsoft." in t for t in texts)


def test_bound_tools_grounding_reaches_real_client_both_modes():
    for mode in ("baseline", "compact"):
        model = _RecordingModel()
        delegate = GroundingDelegate(model, context_mode=mode, common_grounding=_GROUNDING)
        bound = delegate.bind_tools([{"name": "get_stock_data"}])
        result = bound.invoke(_HISTORY)
        assert model.bound_invoked, f"{mode}: real bind_tools client never invoked"
        received = model.bound_invoked[0]
        _assert_grounded_first(received)
        assert result.tool_calls[0]["id"] == "call_1"  # tool_calls preserved exactly
        if mode == "baseline":
            _assert_baseline_history_intact(received)
        else:
            assert any("Analyze Microsoft." in t for t in _texts(received))


def test_structured_output_grounding_reaches_real_client_both_modes():
    for mode in ("baseline", "compact"):
        model = _RecordingModel()
        delegate = GroundingDelegate(model, context_mode=mode, common_grounding=_GROUNDING)
        structured = delegate.with_structured_output(_DummyResult)
        result = structured.invoke("Produce the portfolio decision for MSFT.")
        assert model.structured_invoked, f"{mode}: real structured client never invoked"
        received = model.structured_invoked[0]
        _assert_grounded_first(received)
        assert result.support == 0.9  # real structured runnable returned the parsed result
        # The substantive prompt string is preserved after the grounding header.
        texts = _texts(received)
        assert any("Produce the portfolio decision for MSFT." in t for t in texts)
