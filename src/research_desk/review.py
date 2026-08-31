"""Proposal review state machine and simulated-ledger execution.

Flow: research produces a PENDING_REVIEW proposal. A trusted CLI operator
approves or rejects it. Execution re-evaluates the *current* ledger against the
deterministic policy before writing; the approval binds the exact proposal
version, so a changed proposal cannot ride an old approval. Re-executing an
already-simulated proposal is a no-op (idempotence).

No LLM path reaches this module: the research graph only ever writes a proposal
in PENDING_REVIEW, and only the CLI review/execute/ledger commands touch it.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from .models import (
    ExecutionRecord,
    ProposalRecord,
    ProposalStatus,
    TransactionRecord,
    TransactionStatus,
    make_proposal_version,
    utcnow_iso,
)
from .policy import evaluate_buy, evaluate_sell

# Signals that map to a tradeable buy action; everything else is a sell or
# non-tradeable (Hold / REVIEW).
BUY_SIGNALS = {"Buy", "Overweight", "Strong Buy"}
SELL_SIGNALS = {"Sell", "Underweight", "Reduce"}


def _side_for_signal(signal: str) -> str:
    if signal in BUY_SIGNALS:
        return "buy"
    if signal in SELL_SIGNALS:
        return "sell"
    raise ReviewError(f"signal {signal!r} is not tradeable in v1 (Hold/REVIEW do not trade)")


class ReviewError(Exception):
    """Business rejection with a stable message; the ledger stays unchanged."""


def _proposal_content_version(proposal: ProposalRecord) -> str:
    """Fingerprint of the proposal's tradeable inputs, independent of status."""
    return make_proposal_version(
        proposal.ticker,
        proposal.trade_date,
        proposal.signal,
        proposal.price,
        side=proposal.side,
        shares=proposal.shares,
        evidence_id=proposal.evidence_id,
    )


def create_proposal(
    *,
    run_id: str,
    ticker: str,
    trade_date: str,
    signal: str,
    rating: str | None,
    price: float | None,
    proposal_id: str | None = None,
    evidence_id: str | None = None,
) -> ProposalRecord:
    """Create a PENDING_REVIEW proposal from a completed research run.

    Only tradeable signals become proposals: Buy-family signals are buys, Sell-
    family signals are sells (up to owned shares, enforced at execution). Hold
    and REVIEW never produce a tradeable recommendation.
    """
    if signal in ("Hold", "REVIEW"):
        raise ReviewError(
            f"signal {signal!r} is not tradeable in v1; no proposal is created "
            "(REVIEW and Hold do not trade)"
        )
    side = _side_for_signal(signal)
    pid = proposal_id or f"prop-{uuid.uuid4().hex[:12]}"
    return ProposalRecord(
        proposal_id=pid,
        run_id=run_id,
        ticker=ticker,
        trade_date=trade_date,
        signal=signal,
        rating=rating,
        side=side,
        price=price,
        evidence_id=evidence_id,
        status=ProposalStatus.PENDING_REVIEW,
        proposal_version=_proposal_content_version(
            ProposalRecord(
                proposal_id=pid,
                run_id=run_id,
                ticker=ticker,
                trade_date=trade_date,
                signal=signal,
                rating=rating,
                side=side,
                price=price,
                evidence_id=evidence_id,
            )
        ),
        created_at=utcnow_iso(),
    )


def approve(
    proposal: ProposalRecord,
    *,
    shares: int,
    operator: str,
) -> ProposalRecord:
    """Approve an exact proposal version with an operator-supplied share count.

    The approval is bound to the proposal's *content* version, so if the run's
    material inputs (ticker/date/signal/price) later change, the old approval
    no longer matches and execution requires review.
    """
    if proposal.status == ProposalStatus.SIMULATED:
        raise ReviewError(f"proposal {proposal.proposal_id} is already simulated")
    if proposal.status == ProposalStatus.REJECTED:
        raise ReviewError(f"proposal {proposal.proposal_id} is rejected and cannot be approved")
    # REVIEW_REQUIRED is a safe-fail state, not a dead end: after the operator
    # reviews the current evidence, they may approve the corrected version.
    if not operator:
        raise ReviewError("approval requires an operator identity")
    if not isinstance(shares, int) or shares <= 0:
        raise ReviewError(f"shares must be a positive integer, got {shares!r}")
    if proposal.price is None or proposal.price <= 0:
        raise ReviewError(
            f"proposal {proposal.proposal_id} has no evidence price; cannot approve without price"
        )
    proposal.shares = shares
    proposal.operator = operator
    proposal.status = ProposalStatus.APPROVED
    proposal.approved_at = utcnow_iso()
    proposal.approved_version = _proposal_content_version(proposal)
    return proposal


def reject(proposal: ProposalRecord, *, operator: str, reason: str = "rejected by operator") -> ProposalRecord:
    if proposal.status == ProposalStatus.SIMULATED:
        raise ReviewError(f"proposal {proposal.proposal_id} is already simulated")
    proposal.status = ProposalStatus.REJECTED
    proposal.operator = operator
    proposal.reason = reason
    return proposal


def execute(
    store, proposal: ProposalRecord, *, operator: str,
) -> tuple[ProposalRecord, ExecutionRecord]:
    """Re-evaluate the current ledger and simulate the approved buy (or reject).

    Steps (each observable, none partial):
    1. Idempotence: an already-SIMULATED proposal returns its stored execution.
    2. Version binding: the current proposal content must match the approved
       version; otherwise REVIEW_REQUIRED (AT-05).
    3. Re-read the current ledger and run the deterministic policy.
    4. On any failure: return REVIEW_REQUIRED / BLOCKED with reasons; ledger
       unchanged. On success: apply the transaction atomically.
    """
    if proposal.status == ProposalStatus.SIMULATED:
        existing = proposal.execution or ExecutionRecord(executed=True)
        existing.reason = "already executed"
        return proposal, existing

    current_version = _proposal_content_version(proposal)
    # A stale approval for different content is checked before status: an
    # approved proposal whose run inputs changed must not execute the new
    # version (AT-05), even though the row now carries the new content.
    if proposal.approved_version is not None and proposal.approved_version != current_version:
        proposal.status = ProposalStatus.REVIEW_REQUIRED
        proposal.reason = (
            "approval no longer matches the proposal content (version changed "
            f"approved={proposal.approved_version!r} current={current_version!r}); "
            "re-review against the current ledger"
        )
        store.update_proposal_status(
            proposal.proposal_id,
            ProposalStatus.REVIEW_REQUIRED,
            operator=operator,
            reason=proposal.reason,
        )
        return proposal, ExecutionRecord(
            executed=False, reason=proposal.reason, policy_checks=[]
        )
    if proposal.status != ProposalStatus.APPROVED:
        proposal.status = ProposalStatus.REVIEW_REQUIRED
        proposal.reason = (
            f"proposal is not APPROVED (status={proposal.status.value}) and cannot "
            "execute; approve it against the current ledger first"
        )
        store.update_proposal_status(
            proposal.proposal_id,
            ProposalStatus.REVIEW_REQUIRED,
            operator=operator,
            reason=proposal.reason,
        )
        return proposal, ExecutionRecord(
            executed=False, reason=proposal.reason, policy_checks=[]
        )

    if proposal.shares is None or proposal.price is None:
        proposal.status = ProposalStatus.REVIEW_REQUIRED
        proposal.reason = "proposal missing shares or evidence price; cannot execute"
        store.update_proposal_status(
            proposal.proposal_id, ProposalStatus.REVIEW_REQUIRED, operator=operator,
            reason=proposal.reason,
        )
        return proposal, ExecutionRecord(executed=False, reason=proposal.reason, policy_checks=[])

    ledger = store.get_ledger()
    if ledger is None:
        raise ReviewError("ledger is not initialised")

    if proposal.side == "sell":
        return _execute_sell(store, proposal, ledger, operator=operator)
    verdict = evaluate_buy(ledger, proposal.ticker, proposal.shares, proposal.price)
    if not verdict.allowed:
        reasons = [f"{c['check']}: {c['detail']}" for c in verdict.checks if not c["passed"]]
        proposal.status = ProposalStatus.REVIEW_REQUIRED
        proposal.reason = "policy failed at execution time: " + "; ".join(reasons)
        store.update_proposal_status(
            proposal.proposal_id, ProposalStatus.REVIEW_REQUIRED, operator=operator,
            reason=proposal.reason,
        )
        return proposal, ExecutionRecord(
            executed=False,
            reason=proposal.reason,
            policy_checks=verdict.checks,
            equity_before=ledger.equity,
        )

    tx_id = f"tx-{uuid.uuid4().hex[:12]}"
    execution = ExecutionRecord(
        executed=True,
        tx_id=tx_id,
        policy_checks=verdict.checks,
        equity_before=ledger.equity,
        equity_after=ledger.equity,
        cash_delta=-proposal.shares * proposal.price,
    )
    tx = TransactionRecord(
        tx_id=tx_id,
        proposal_id=proposal.proposal_id,
        ticker=proposal.ticker,
        side="buy",
        shares=proposal.shares,
        price=proposal.price,
        cash_delta=execution.cash_delta,
        equity_before=ledger.equity,
        equity_after=ledger.equity,
        status=TransactionStatus.SIMULATED,
        policy_checks=verdict.checks,
        operator=operator,
        created_at=utcnow_iso(),
    )
    store.apply_transaction(tx, execution)
    proposal.status = ProposalStatus.SIMULATED
    proposal.execution = execution
    updated = store.get_proposal(proposal.proposal_id)
    return updated or proposal, proposal.execution


def _execute_sell(store, proposal: ProposalRecord, ledger, *, operator: str):
    """Execute an approved sell up to owned shares; apply the transaction atomically."""
    shares = proposal.shares
    price = proposal.price
    if shares is None or price is None:
        proposal.status = ProposalStatus.REVIEW_REQUIRED
        proposal.reason = "proposal missing shares or evidence price; cannot execute"
        store.update_proposal_status(
            proposal.proposal_id, ProposalStatus.REVIEW_REQUIRED, operator=operator,
            reason=proposal.reason,
        )
        return proposal, ExecutionRecord(executed=False, reason=proposal.reason, policy_checks=[])

    verdict = evaluate_sell(ledger, proposal.ticker, shares, price)
    if not verdict.allowed:
        reasons = [f"{c['check']}: {c['detail']}" for c in verdict.checks if not c["passed"]]
        proposal.status = ProposalStatus.REVIEW_REQUIRED
        proposal.reason = "policy failed at execution time: " + "; ".join(reasons)
        store.update_proposal_status(
            proposal.proposal_id, ProposalStatus.REVIEW_REQUIRED, operator=operator,
            reason=proposal.reason,
        )
        return proposal, ExecutionRecord(
            executed=False,
            reason=proposal.reason,
            policy_checks=verdict.checks,
            equity_before=ledger.equity,
        )

    tx_id = f"tx-{uuid.uuid4().hex[:12]}"
    execution = ExecutionRecord(
        executed=True,
        tx_id=tx_id,
        policy_checks=verdict.checks,
        equity_before=ledger.equity,
        equity_after=ledger.equity,
        cash_delta=shares * price,
    )
    tx = TransactionRecord(
        tx_id=tx_id,
        proposal_id=proposal.proposal_id,
        ticker=proposal.ticker,
        side="sell",
        shares=shares,
        price=price,
        cash_delta=execution.cash_delta,
        equity_before=ledger.equity,
        equity_after=ledger.equity,
        status=TransactionStatus.SIMULATED,
        policy_checks=verdict.checks,
        operator=operator,
        created_at=utcnow_iso(),
    )
    store.apply_transaction(tx, execution)
    proposal.status = ProposalStatus.SIMULATED
    proposal.execution = execution
    updated = store.get_proposal(proposal.proposal_id)
    return updated or proposal, proposal.execution


def evaluate_proposal_legibility(proposal: ProposalRecord) -> list[str]:
    """Non-mutating advisory checks used by the CLI ledger/report views."""
    issues: list[str] = []
    if proposal.status != ProposalStatus.APPROVED:
        issues.append(f"not APPROVED (status={proposal.status.value})")
    if proposal.shares is None or proposal.price is None:
        issues.append("missing shares or evidence price")
    return issues


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
