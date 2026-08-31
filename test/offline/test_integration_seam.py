"""Integration seam: the real TradingAgentsGraph subclass, frozen tool nodes,
direct-data-path recording, and the runner's proposal decision matrix.

Construction uses the same mocked LLM factory the upstream ``tests/conftest.py``
uses, so no live API is touched. This verifies the *seam*: frozen tool nodes
serve frozen evidence through the same graph topology, identity reads are
recorded, and the proposal decision honours evidence and outcome.
"""

from __future__ import annotations

from research_desk.evidence import EvidenceLog
from research_desk.graph_adapter import (
    EvidenceTradingGraph,
    _provider_tools,
    decide_proposal,
    price_from_evidence,
)
from research_desk.models import RunOutcome
from tradingagents.default_config import DEFAULT_CONFIG


def _graph_config():
    cfg = DEFAULT_CONFIG.copy()
    cfg["data_cache_dir"] = "/tmp/research-desk-test-cache"
    cfg["results_dir"] = "/tmp/research-desk-test-results"
    return cfg


def _frozen_provider(ticker="AAPL"):
    from research_desk.eval import case_registry
    from research_desk.eval.frozen_provider import FrozenMarketProvider

    return FrozenMarketProvider(ticker, case_registry.MARKET_DIR / f"{ticker}.csv")


def _snapshot(price=100.0):
    from test.fixtures.fixture_packs import stock_data_csv

    dates = ["2026-06-01", "2026-06-10"]
    return {
        "get_stock_data": {
            '{"end_date": "2026-06-10", "start_date": "2026-06-01", "symbol": "AAPL"}': stock_data_csv("AAPL", [99.0, price], dates)
        }
    }


def test_frozen_tool_nodes_serve_frozen_data(mock_llm_client):
    """Same graph topology; frozen ToolNodes serve frozen data, no network."""
    graph = EvidenceTradingGraph(
        selected_analysts=("market", "news"),
        debug=False,
        config=_graph_config(),
        data_mode="frozen",
        data_snapshot=_snapshot(price=100.0),
        frozen_identity={"company_name": "Apple Inc", "sector": "Technology"},
        frozen_provider=_frozen_provider("AAPL"),
    )
    market_tools = sorted(graph.tool_nodes["market"].tools_by_name.keys())
    assert "get_stock_data" in market_tools
    assert "get_indicators" in market_tools
    assert "get_verified_market_snapshot" in market_tools
    news_tools = sorted(graph.tool_nodes["news"].tools_by_name.keys())
    assert "get_news" in news_tools

    tools = _provider_tools(_frozen_provider("AAPL"))
    result = tools["get_stock_data"].invoke(
        {"symbol": "AAPL", "start_date": "2026-06-01", "end_date": "2026-06-10"}
    )
    assert "Stock data for AAPL" in result


def test_frozen_tool_unknown_call_returns_no_data_sentinel(mock_llm_client):
    graph = EvidenceTradingGraph(
        selected_analysts=("market",),
        debug=False,
        config=_graph_config(),
        data_mode="frozen",
        data_snapshot=_snapshot(),
        frozen_identity={},
    )
    assert "market" in graph.tool_nodes
    tools = _provider_tools(_frozen_provider("AAPL"))
    result = tools["get_stock_data"].invoke(
        {"symbol": "TSLA", "start_date": "2026-01-01", "end_date": "2026-01-31"}
    )
    assert "NO_DATA_AVAILABLE" in result  # never fabricate (SEC-001)


def test_identity_read_recorded_in_frozen_mode(mock_llm_client):
    log = EvidenceLog()
    graph = EvidenceTradingGraph(
        selected_analysts=("market", "news"),
        debug=False,
        config=_graph_config(),
        data_mode="frozen",
        evidence_log=log,
        frozen_identity={"company_name": "Apple Inc", "sector": "Technology"},
    )
    ctx = graph.resolve_instrument_context("AAPL", "stock")
    assert "Apple Inc" in ctx
    reads = [e for e in log.events if e.kind == "data_read"]
    assert len(reads) == 1
    assert reads[0].payload["source"] == "instrument_identity"
    assert reads[0].payload["ticker"] == "AAPL"
    assert reads[0].payload["payload"]["company_name"] == "Apple Inc"


def test_live_mode_resolve_records_identity(mock_llm_client, monkeypatch):
    """The narrow hook records the real identity read even in live mode."""
    from research_desk import graph_adapter as ga

    captured = {}

    def fake_resolve(ticker):
        captured["ticker"] = ticker
        return {"company_name": "Apple Inc", "sector": "Technology"}

    monkeypatch.setattr(ga, "resolve_instrument_identity", fake_resolve)
    log = EvidenceLog()
    graph = EvidenceTradingGraph(
        selected_analysts=("market", "news"),
        debug=False,
        config=_graph_config(),
        data_mode="live",
        evidence_log=log,
    )
    ctx = graph.resolve_instrument_context("AAPL", "stock")
    assert "Apple Inc" in ctx
    assert captured["ticker"] == "AAPL"
    reads = [e for e in log.events if e.kind == "data_read"]
    assert len(reads) == 1 and reads[0].payload["source"] == "instrument_identity"


def test_frozen_mode_skips_network_returns_read(mock_llm_client):
    log = EvidenceLog()
    graph = EvidenceTradingGraph(
        selected_analysts=("market",),
        debug=False,
        config=_graph_config(),
        data_mode="frozen",
        evidence_log=log,
    )
    out = graph._fetch_returns("AAPL", "2026-06-10", holding_days=5, benchmark="SPY")
    assert out == (None, None, None, None)  # frozen: never fetches returns over network
    reads = [e for e in log.events if e.kind == "data_read"]
    assert any(e.payload["source"] == "realized_returns" for e in reads)


def test_price_from_evidence_boundary():
    assert price_from_evidence(_snapshot(price=100.0), "AAPL") == 100.0
    assert price_from_evidence(_snapshot(price=120.5), "AAPL") == 120.5
    assert price_from_evidence({}, "AAPL") is None


def test_decide_proposal_matrix():
    snap = _snapshot(price=100.0)
    assert decide_proposal(
        outcome=RunOutcome.COMPLETED.value, signal="Buy", run_id="r", ticker="AAPL",
        trade_date="2026-06-10", snapshot=snap,
    ) is not None
    assert decide_proposal(
        outcome=RunOutcome.COMPLETED.value, signal="Overweight", run_id="r", ticker="AAPL",
        trade_date="2026-06-10", snapshot=snap,
    ) is not None
    # Sell-family signals now produce sell proposals (valid sells up to owned
    # shares execute); only Hold/REVIEW are non-tradeable.
    sell = decide_proposal(
        outcome=RunOutcome.COMPLETED.value, signal="Sell", run_id="r", ticker="AAPL",
        trade_date="2026-06-10", snapshot=snap,
    )
    assert sell is not None and sell.side == "sell"
    for bad_signal in ("Hold", "REVIEW"):
        assert decide_proposal(
            outcome=RunOutcome.COMPLETED.value, signal=bad_signal, run_id="r",
            ticker="AAPL", trade_date="2026-06-10", snapshot=snap,
        ) is None
    for bad_outcome in ("budget_stopped", "failed"):
        assert decide_proposal(
            outcome=bad_outcome, signal="Buy", run_id="r", ticker="AAPL",
            trade_date="2026-06-10", snapshot=snap,
        ) is None
    # No evidence price -> no proposal.
    assert decide_proposal(
        outcome=RunOutcome.COMPLETED.value, signal="Buy", run_id="r", ticker="AAPL",
        trade_date="2026-06-10", snapshot={},
    ) is None
