"""ADR-004 bounded revision contracts: terminal rejection, EPS periods, model
version and the judge semantic-validity condition.

The review tests use a Mock store so they assert the state transition itself
(no persistence call, no ledger read) rather than a database implementation.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from research_desk.context import build_common_grounding
from research_desk.eval.case_registry import case_for
from research_desk.models import ProposalStatus, utcnow_iso
from research_desk.review import ReviewError, approve, create_proposal, execute, reject


def _proposal(*, price: float = 100.0, proposal_id: str | None = None):
    return create_proposal(
        run_id="run-revision",
        ticker="AAPL",
        trade_date="2026-06-10",
        signal="Buy",
        rating="Buy",
        price=price,
        proposal_id=proposal_id or f"prop-revision-{utcnow_iso()[-9:]}",
    )


def test_rejected_execute_remains_rejected_and_cannot_be_approved():
    """Execution cannot turn a rejection into an approvable REVIEW_REQUIRED row."""
    store = MagicMock()
    proposal = _proposal()
    reject(proposal, operator="leo")
    assert proposal.status == ProposalStatus.REJECTED

    updated, execution = execute(store, proposal, operator="leo")

    assert updated.status == ProposalStatus.REJECTED
    assert execution.executed is False
    assert execution.reason == "proposal rejected"
    store.update_proposal_status.assert_not_called()
    store.apply_transaction.assert_not_called()
    store.get_ledger.assert_not_called()

    with pytest.raises(ReviewError, match="rejected"):
        approve(updated, shares=100, operator="leo")


def test_previously_approved_then_rejected_stays_rejected_on_execute():
    """A rejection is terminal even when an earlier approval version is present."""
    store = MagicMock()
    proposal = _proposal()
    approved = approve(proposal, shares=100, operator="leo")
    assert approved.approved_version
    reject(approved, operator="leo")
    assert approved.status == ProposalStatus.REJECTED

    updated, execution = execute(store, approved, operator="leo")

    assert updated.status == ProposalStatus.REJECTED
    assert execution.executed is False
    assert execution.reason == "proposal rejected"
    store.update_proposal_status.assert_not_called()
    store.apply_transaction.assert_not_called()

    with pytest.raises(ReviewError, match="rejected"):
        approve(updated, shares=100, operator="leo")


def test_common_grounding_names_eps_period_and_ttm_limit():
    grounding = build_common_grounding("AAPL", "2026-07-31", {})
    lower = grounding.lower()
    assert "quarterly eps" in lower
    assert "trailing-twelve-month (ttm)" in lower
    assert "trailing p/e" in lower
    assert "actual ttm evidence" in lower
    # No fixed stock examples or invented figures in the shared rules.
    assert "microsoft" not in lower
    assert "usd90.0b" not in lower


def test_authoritative_model_and_prompt_version_are_consistent():
    from research_desk.config import (
        DEFAULT_BASE_URL,
        DEFAULT_MODEL,
        DEFAULT_PROVIDER,
        PROMPT_VERSION,
        ResearchDeskSettings,
    )
    from research_desk.eval import live

    assert live.MODEL == DEFAULT_MODEL == "deepseek-flash"
    assert live.PROVIDER == DEFAULT_PROVIDER == "deepseek"
    assert DEFAULT_BASE_URL == "https://api.aiohub.org/v1"
    assert ResearchDeskSettings().prompt_version == PROMPT_VERSION

    snapshot = yaml.safe_load(
        Path("prompts/runtime-prompts-v0.1.2.yaml").read_text(encoding="utf-8")
    )
    assert snapshot["prompt_version"] == PROMPT_VERSION
    assert snapshot["model"] == DEFAULT_MODEL
    assert snapshot["provider"] == DEFAULT_PROVIDER
    assert snapshot["base_url"] == DEFAULT_BASE_URL


def test_judge_prompt_requires_semantic_validity():
    from research_desk.eval.live import _judge_prompt

    prompt = _judge_prompt(
        case_for("AAPL"),
        "report text",
        [],
        available_sources={},
        events=[],
    )
    assert "semantic_valid" in prompt
    assert "semantic_errors" in prompt
    assert "quarterly EPS" in prompt
    assert "trailing P/E" in prompt
    assert "Valid citation IDs do NOT rescue" in prompt


def test_judge_score_defaults_invalid_and_errors_force_false():
    from research_desk.eval.live import JudgeScore

    legacy = JudgeScore(
        support=0.9,
        relevance=0.9,
        cited_claim_count=2,
        supported_cited_claim_count=2,
    )
    assert legacy.semantic_valid is False  # absent field is never a pass
    assert legacy.semantic_errors == []

    flagged = JudgeScore(
        support=0.9,
        relevance=0.9,
        cited_claim_count=2,
        supported_cited_claim_count=2,
        semantic_valid=True,
        semantic_errors=["quarterly EPS labeled as TTM"],
    )
    assert flagged.semantic_valid is False


def test_llm_judge_records_semantic_fields(monkeypatch):
    from langchain_core.messages import AIMessage

    from research_desk.eval import live

    class _FakeLLM:
        def __init__(self):
            self.extra_body = None

        def with_structured_output(self, schema, include_raw=False):
            def invoke(_prompt):
                parsed = live.JudgeScore(
                    support=0.9,
                    relevance=0.9,
                    cited_claim_count=2,
                    supported_cited_claim_count=2,
                    semantic_valid=True,
                    semantic_errors=["quarterly EPS relabeled as TTM"],
                )
                return {"raw": AIMessage(content=""), "parsed": parsed, "parsing_error": None}

            return type("SO", (), {"invoke": staticmethod(invoke)})()

    class _FakeClient:
        def get_llm(self):
            return _FakeLLM()

    monkeypatch.setattr(
        "tradingagents.llm_clients.create_llm_client", lambda *a, **k: _FakeClient()
    )

    _raw, score = live._llm_judge(
        case_for("AAPL"),
        "report text",
        [],
        available_sources={},
        events=[],
    )
    assert score["semantic_valid"] is False
    assert score["semantic_errors"] == ["quarterly EPS relabeled as TTM"]


def test_deepseek_transport_disables_reasoning_via_extra_body(monkeypatch):
    """The verified endpoint flag reaches the real DeepSeek request payload."""
    from langchain_core.messages import HumanMessage

    from research_desk.config import DEFAULT_BASE_URL, DEFAULT_MODEL, DEFAULT_PROVIDER
    from research_desk.eval import live
    from tradingagents.llm_clients import create_llm_client
    from tradingagents.llm_clients.openai_client import DeepSeekChatOpenAI

    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key-not-used")

    llm = create_llm_client(
        DEFAULT_PROVIDER,
        DEFAULT_MODEL,
        base_url=DEFAULT_BASE_URL,
        max_tokens=live.OUTPUT_CAP,
        temperature=0,
    ).get_llm()
    assert isinstance(llm, DeepSeekChatOpenAI)
    # Same assignment the graph adapter and judge apply before invocation.
    llm.extra_body = dict(live.THINKING_DISABLED_EXTRA_BODY)

    payload = llm._get_request_payload([HumanMessage(content="ping")])
    assert payload["extra_body"]["reasoning_effort"] == "none"
    assert payload["extra_body"]["thinking"] == {"type": "disabled"}

    structured = llm.with_structured_output(live.JudgeScore, include_raw=True)
    raw_binding = structured.steps[0].steps__["raw"]
    bound = raw_binding.bound
    assert isinstance(bound, DeepSeekChatOpenAI)
    structured_payload = bound._get_request_payload(
        [HumanMessage(content="ping")], **raw_binding.kwargs
    )
    assert structured_payload["extra_body"]["reasoning_effort"] == "none"
    assert structured_payload["extra_body"]["thinking"] == {"type": "disabled"}
