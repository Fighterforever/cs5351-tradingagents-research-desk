"""AT-05 / FR-002 / INV-001: approvals bind the exact proposal version, and
execution re-evaluates the *current* ledger. A stale approval or a changed
ledger yields REVIEW_REQUIRED with no partial writes.
"""

from __future__ import annotations

from research_desk.models import ProposalStatus, utcnow_iso
from research_desk.review import approve, create_proposal, execute


def _proposal(signal="Buy", price=100.0, proposal_id=None):
    return create_proposal(
        run_id="run-x", ticker="AAPL", trade_date="2026-06-10",
        signal=signal, rating=signal, price=price,
        proposal_id=proposal_id or f"prop-at05-{utcnow_iso()[-9:]}",
    )


def _approve_and_persist(store, p, shares, operator="leo"):
    approved = approve(p, shares=shares, operator=operator)
    store.save_proposal(approved)
    return approved


def test_changed_proposal_cannot_ride_old_approval(store):
    """Approval was for price 100; a later price change invalidates it (AT-05)."""
    p = _proposal(price=100.0, proposal_id="prop-at05-version")
    store.save_proposal(p)
    approved = _approve_and_persist(store, p, shares=100)
    # The binding covers the approved content including the operator quantity.
    assert approved.approved_version  # set at approval time (quantity known)
    assert approved.approved_version != p.proposal_version  # quantity now bound

    # The run is re-evaluated against new evidence: price changes.
    changed = _proposal(price=120.0, proposal_id=p.proposal_id)
    store.save_proposal(changed)
    stored = store.get_proposal(p.proposal_id)
    assert stored.proposal_version != approved.approved_version

    updated, ex = execute(store, stored, operator="leo")
    assert ex.executed is False
    assert updated.status == ProposalStatus.REVIEW_REQUIRED
    assert "version changed" in (updated.reason or "")
    assert store.get_ledger().cash == 100000.0  # no partial write
    assert store.get_ledger().positions == {}


def test_changed_quantity_cannot_ride_old_approval(store):
    """Approval binds the quantity too: changing shares invalidates it (AT-05)."""
    p = _proposal(price=100.0, proposal_id="prop-at05-quantity")
    store.save_proposal(p)
    _approve_and_persist(store, p, shares=100)

    # The operator later edits the approved proposal to a different quantity.
    changed = _proposal(price=100.0, proposal_id=p.proposal_id)
    changed.shares = 90
    store.save_proposal(changed)
    stored = store.get_proposal(p.proposal_id)

    updated, ex = execute(store, stored, operator="leo")
    assert ex.executed is False
    assert updated.status == ProposalStatus.REVIEW_REQUIRED
    assert "version changed" in (updated.reason or "")
    assert store.get_ledger().cash == 100000.0


def test_execution_rechecks_current_ledger(store):
    """An approval made before a competing trade must re-check the new balance."""
    p1 = _proposal(price=100.0, proposal_id="prop-at05-p1")
    store.save_proposal(p1)
    _approve_and_persist(store, p1, shares=100)
    updated1, ex1 = execute(store, store.get_proposal(p1.proposal_id), operator="leo")
    assert ex1.executed is True  # cash -> 90000

    # p2 was approved earlier but executes after p1 drained cash below its cost.
    p2 = _proposal(price=95.0, proposal_id="prop-at05-p2")
    store.save_proposal(p2)
    _approve_and_persist(store, p2, shares=1000)  # cost 95000 > remaining 90000
    updated2, ex2 = execute(store, store.get_proposal(p2.proposal_id), operator="leo")
    assert ex2.executed is False
    assert updated2.status == ProposalStatus.REVIEW_REQUIRED
    assert any(c["check"] == "cash_sufficient" for c in ex2.policy_checks or [])
    # Ledger unchanged by the failed execution.
    ledger = store.get_ledger()
    assert ledger.cash == 90000.0
    assert ledger.positions["AAPL"].shares == 100


def test_no_partial_write_on_policy_failure(store):
    p = _proposal(proposal_id="prop-at05-partial")
    store.save_proposal(p)
    _approve_and_persist(store, p, shares=100)
    # Sabotage the proposal so policy fails at execution time (missing price).
    store.update_proposal_status(p.proposal_id, ProposalStatus.APPROVED, operator="leo")
    bad = store.get_proposal(p.proposal_id)
    bad.price = None
    store.save_proposal(bad)
    updated, ex = execute(store, store.get_proposal(p.proposal_id), operator="leo")
    assert ex.executed is False
    assert store.get_ledger().cash == 100000.0
    assert store.get_ledger().positions == {}
    assert store.list_transactions() == []


def test_reapprove_after_review_required(store):
    """After REVIEW_REQUIRED, the operator can re-approve the corrected version."""
    p = _proposal(price=100.0, proposal_id="prop-at05-reapprove")
    store.save_proposal(p)
    _approve_and_persist(store, p, shares=100)
    changed = _proposal(price=120.0, proposal_id=p.proposal_id)
    store.save_proposal(changed)
    updated, ex = execute(store, store.get_proposal(p.proposal_id), operator="leo")
    assert ex.executed is False
    assert updated.status == ProposalStatus.REVIEW_REQUIRED

    # Re-approve the corrected proposal at a compliant size (80 sh @ 120 = 9600
    # <= 10% of 100000) and it can execute.
    reapproved = approve(store.get_proposal(p.proposal_id), shares=80, operator="leo")
    store.save_proposal(reapproved)
    updated2, ex2 = execute(store, store.get_proposal(p.proposal_id), operator="leo")
    assert ex2.executed is True
    assert store.get_ledger().cash == 100000.0 - 9600.0
