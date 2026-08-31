"""Pydantic data records for the Research Desk offline slice.

These records are the single source of truth for everything the evidence
packs, the simulated ledger, and the review state machine store on disk.
Fields are explicit so a packed evidence bundle is self-describing and can
be validated by an external JSON schema (see ``docs/req/req-schema.json``).

Conventions enforced here:
- Amounts are floats in USD; share counts are positive integers.
- Every proposal and every ledger transaction carries a ``proposal_version``
  that binds an approval to the exact proposal contents it was granted for.
- Nothing in these records holds credentials.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Shared enums
# ---------------------------------------------------------------------------


class RunOutcome(str, Enum):
    """How a research run ended."""

    COMPLETED = "completed"
    BUDGET_STOPPED = "budget_stopped"
    FAILED = "failed"


class ContextMode(str, Enum):
    """Which context-assembly configuration produced a run's prompts."""

    BASELINE = "baseline"
    COMPACT = "compact"


class RunDataMode(str, Enum):
    """Where a run's tool data came from."""

    LIVE = "live"  # real vendor fetches through the real graph
    FROZEN = "frozen"  # controlled rerun on frozen evidence (same graph, no network)


class ProposalStatus(str, Enum):
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SIMULATED = "SIMULATED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class TransactionStatus(str, Enum):
    SIMULATED = "SIMULATED"
    BLOCKED = "BLOCKED"


class EventKind(str, Enum):
    """Event types recorded in an evidence pack's event log."""

    RUN_START = "run_start"
    LLM_REQUEST = "llm_request"
    LLM_RESPONSE = "llm_response"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    DATA_READ = "data_read"  # direct data paths callbacks cannot see
    CONTEXT_ASSEMBLED = "context_assembled"
    BUDGET_STOP = "budget_stop"
    RUN_END = "run_end"


# ---------------------------------------------------------------------------
# Usage / calls
# ---------------------------------------------------------------------------


class CallUsage(BaseModel):
    """Actual token usage reported by an LLM provider for one call."""

    input_tokens: int = 0
    output_tokens: int = 0


class UsageSummary(BaseModel):
    """Aggregated LLM usage across a run or a compare arm."""

    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    stop_reason: str | None = None  # "completed" | "budget_exhausted" | "error"

    def add(self, usage: CallUsage) -> None:
        self.calls += 1
        self.input_tokens += usage.input_tokens
        self.output_tokens += usage.output_tokens
        self.total_tokens += usage.input_tokens + usage.output_tokens


class CallRecord(BaseModel):
    """One LLM or tool call observed during a run."""

    seq: int = 0
    ts: str = ""
    kind: str = "llm"  # "llm" | "tool"
    node: str | None = None  # best-effort graph node attribution (langgraph_node metadata)
    model: str | None = None
    name: str = ""  # tool name for tool calls
    input_tokens: int = 0
    output_tokens: int = 0
    args: dict[str, Any] | None = None
    result: str | None = None
    prompt: str | None = None  # material input, kept for evidence completeness
    response: str | None = None


# ---------------------------------------------------------------------------
# Events / manifest / evidence pack
# ---------------------------------------------------------------------------


class EvidenceEvent(BaseModel):
    seq: int
    kind: str
    ts: str
    node: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class RunManifest(BaseModel):
    """Provenance header of a research run and its evidence pack."""

    run_id: str
    ticker: str
    trade_date: str
    asset_type: str = "stock"
    analysts: list[str] = Field(default_factory=list)
    context_mode: str = "baseline"
    data_mode: str = "live"  # live | frozen
    outcome: str = "completed"
    signal: str | None = None
    prompt_version: str = ""
    package_schema_version: int = 1
    created_at: str = ""
    operator: str = "research-desk"
    model_quick: str | None = None
    model_deep: str | None = None
    budget_max_calls: int | None = None
    source_pack: str | None = None  # when this pack is a controlled rerun of another pack
    reason: str | None = None


class InputSnapshot(BaseModel):
    """The material inputs a run consumed, so a rerun can be replayed."""

    instrument_context: str = ""
    past_context: str = ""
    initial_state: dict[str, Any] = Field(default_factory=dict)
    identity: dict[str, Any] = Field(default_factory=dict)
    data_snapshot: dict[str, dict[str, str]] = Field(
        default_factory=dict
    )  # tool_name -> {"canonical args key": result text}
    memory_used: list[dict[str, Any]] = Field(default_factory=list)
    memory_sources: list[str] = Field(default_factory=list)
    # Factual *available* corpus for the case (identity, full market CSV, official
    # news notes) recorded separately from the tool calls actually made. This is
    # what makes the evidence-derived price available for proposal/replay even
    # when a model path did not ask one of the data tools.
    available_sources: dict[str, Any] = Field(default_factory=dict)


class EvidencePack(BaseModel):
    """A complete, self-contained evidence package for one run.

    ``final_state`` is the graph's merged terminal state; it is the material
    needed to rebuild reports and derive the signal and policy outputs offline
    with zero external calls.
    """

    manifest: RunManifest
    input: InputSnapshot
    events: list[EvidenceEvent] = Field(default_factory=list)
    final_state: dict[str, Any] = Field(default_factory=dict)
    usage: UsageSummary = Field(default_factory=UsageSummary)
    calls: list[CallRecord] = Field(default_factory=list)
    reports_written: list[str] = Field(default_factory=list)
    proposal: ProposalRecord | None = None
    complete: bool = False  # set True only when a full pack was exported

    @field_validator("final_state")
    @classmethod
    def _final_state_serializable(cls, v):
        if not v:
            return v
        if not isinstance(v, dict):
            raise ValueError("final_state must be a dict")
        return v


class ProposalRecord(BaseModel):
    """A single reviewable proposal produced by a research run."""

    proposal_id: str
    run_id: str
    ticker: str
    trade_date: str
    signal: str
    rating: str | None = None
    side: str = "buy"  # "buy" | "sell"; derived from the tradeable signal
    price: float | None = None  # from evidence only, never operator-typed
    shares: int | None = None  # from the trusted CLI operator
    evidence_id: str | None = None  # identity of the frozen evidence that supplied price/signal
    status: ProposalStatus = ProposalStatus.PENDING_REVIEW
    proposal_version: str = ""  # binds approvals to this exact content
    operator: str | None = None
    created_at: str = ""
    approved_at: str | None = None
    approved_version: str | None = None
    reason: str | None = None
    execution: ExecutionRecord | None = None

    @field_validator("shares")
    @classmethod
    def _shares_positive_int(cls, v):
        if v is None:
            return v
        if not isinstance(v, int) or v <= 0:
            raise ValueError("shares must be a positive integer")
        return v


class ExecutionRecord(BaseModel):
    """Result of executing an approved proposal against the current ledger."""

    executed: bool
    tx_id: str | None = None
    policy_checks: list[dict[str, Any]] = Field(default_factory=list)
    equity_before: float | None = None
    equity_after: float | None = None
    cash_delta: float | None = None
    reason: str | None = None


class LedgerPosition(BaseModel):
    ticker: str
    shares: int = 0
    avg_price: float | None = None


class LedgerState(BaseModel):
    cash: float = 100000.0
    positions: dict[str, LedgerPosition] = Field(default_factory=dict)
    last_updated: str = ""

    @property
    def equity(self) -> float:
        """Equity = cash + sum(position market value at avg price)."""
        total = self.cash
        for pos in self.positions.values():
            if pos.avg_price is not None:
                total += pos.shares * pos.avg_price
        return total


class TransactionRecord(BaseModel):
    tx_id: str
    proposal_id: str
    ticker: str
    side: str = "buy"
    shares: int
    price: float
    cash_delta: float
    equity_before: float
    equity_after: float
    status: TransactionStatus = TransactionStatus.SIMULATED
    policy_checks: list[dict[str, Any]] = Field(default_factory=list)
    operator: str | None = None
    created_at: str = ""


# ---------------------------------------------------------------------------
# Run result returned by the research runner
# ---------------------------------------------------------------------------


class RunResult(BaseModel):
    run_id: str
    ticker: str
    trade_date: str
    outcome: str
    signal: str | None = None
    usage: UsageSummary = Field(default_factory=UsageSummary)
    events: list[EvidenceEvent] = Field(default_factory=list)
    final_state: dict[str, Any] = Field(default_factory=dict)
    proposal: ProposalRecord | None = None
    pack_path: str | None = None
    error: str | None = None
    stop_reason: str | None = None


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def make_proposal_version(
    ticker: str,
    trade_date: str,
    signal: str,
    price: float | None,
    *,
    side: str = "buy",
    shares: int | None = None,
    evidence_id: str | None = None,
) -> str:
    """Content fingerprint binding an approval to the exact proposal inputs.

    The fingerprint covers every *tradeable* field: ticker, analysis date,
    action (side), signal, price (from evidence), evidence identity, and the
    operator-supplied quantity. Changing any of these requires a new approval.
    """
    import hashlib

    payload = "|".join(
        [
            ticker.upper(),
            str(trade_date),
            str(side),
            str(signal),
            str(price),
            str(evidence_id or ""),
            str(shares if shares is not None else ""),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


EvidencePack.model_rebuild()
