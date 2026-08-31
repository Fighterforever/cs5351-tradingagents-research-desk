"""AT-03 / FR-002 / INV-001: normal approval path and transaction idempotence.

Cash 100000, zero positions, price 100; the operator approves 100 shares. The
first execution debits cash to 90000 and records 100 shares with the approver,
approval version and passed policy checks. Executing the same proposal again is
a no-op — no double debit.
"""

from __future__ import annotations

from research_desk.models import ProposalStatus, utcnow_iso
from research_desk.review import approve, create_proposal, execute


def _proposal(*, signal="Buy", price=100.0, proposal_id=None):
    return create_proposal(
        run_id="run-test",
        ticker="AAPL",
        trade_date="2026-06-10",
        signal=signal,
        rating=signal,
        price=price,
        proposal_id=proposal_id or f"prop-at03-{utcnow_iso()[-9:]}",
    )


def test_at03_approve_execute_records_and_idempotent(store):
    """First execution debits cash and records shares; re-execution is a no-op."""
    proposal = _proposal()
    store.save_proposal(proposal)

    approved = approve(proposal, shares=100, operator="leo")
    store.save_proposal(approved)
    assert approved.approved_version  # approval bound to this exact proposal version

    updated, execution = execute(store, store.get_proposal(proposal.proposal_id), operator="leo")
    ledger = store.get_ledger()
    assert execution.executed is True
    assert execution.tx_id
    assert ledger.cash == 90000.0  # 100000 - 100*100
    assert ledger.positions["AAPL"].shares == 100
    assert ledger.positions["AAPL"].avg_price == 100.0
    assert updated.status == ProposalStatus.SIMULATED
    assert execution.policy_checks  # the deterministic policy results are recorded

    # The proposal itself carries the approver/version/policy trail (INV-001).
    stored = store.get_proposal(proposal.proposal_id)
    assert stored.operator == "leo"
    assert stored.approved_version == approved.approved_version

    # Idempotence: executing the same proposal again changes nothing.
    before = store.get_ledger()
    re, rex = execute(store, store.get_proposal(proposal.proposal_id), operator="leo")
    after = store.get_ledger()
    assert re.status == ProposalStatus.SIMULATED
    assert rex.reason == "already executed"
    assert after.cash == before.cash == 90000.0
    assert after.positions["AAPL"].shares == 100
    assert len(store.list_transactions()) == 1  # no second transaction


def test_at03_exact_cap_boundary_allowed(store):
    """100 shares @ 100 on 100000 cash is exactly the 10% cap: allowed."""
    from research_desk.models import LedgerState
    from research_desk.policy import evaluate_buy

    verdict = evaluate_buy(LedgerState(cash=100000.0), "AAPL", 100, 100.0)
    assert verdict.allowed is True
    assert abs(verdict.position_value - 10000.0) < 1e-9
    assert abs(verdict.equity - 100000.0) < 1e-9


def test_at03_accumulates_multiple_positions(store):
    """The cap counts TOTAL holdings after the buy, not each independent ticket."""
    from research_desk.policy import evaluate_buy

    p1 = _proposal(proposal_id="prop-at03-a")
    store.save_proposal(p1)
    a1 = approve(p1, shares=100, operator="leo")
    store.save_proposal(a1)
    execute(store, store.get_proposal(p1.proposal_id), operator="leo")

    # After the first buy the position is exactly at the 10% cap (100 sh @ 100
    # = 10000 on equity 100000). The cap is on *total* holdings, so a second buy
    # of ANY positive amount pushes total holdings above the cap and is rejected.
    verdict = evaluate_buy(store.get_ledger(), "AAPL", 1, 100.0)
    assert verdict.allowed is False
    assert any(c["check"] == "position_cap_10pct" and not c["passed"] for c in verdict.checks)

    p2 = _proposal(proposal_id="prop-at03-b")
    store.save_proposal(p2)
    a2 = approve(p2, shares=100, operator="leo")
    store.save_proposal(a2)
    updated2, ex2 = execute(store, store.get_proposal(p2.proposal_id), operator="leo")
    ledger = store.get_ledger()
    assert ex2.executed is False
    assert updated2.status == ProposalStatus.REVIEW_REQUIRED
    # Ledger unchanged by the rejected second buy.
    assert ledger.cash == 90000.0
    assert ledger.positions["AAPL"].shares == 100
