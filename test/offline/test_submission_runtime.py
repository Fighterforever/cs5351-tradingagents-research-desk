"""Runtime registration: register_proposal imports advisory terms and preserves
operator-assigned shares; legacy packs roundtrip with stable material identity.
"""

from __future__ import annotations

from research_desk.models import ProposalStatus, utcnow_iso
from research_desk.review import approve, create_proposal, execute, reject


def _proposal(*, price=100.0, signal="Buy", proposal_id=None, evidence_id="ev-1"):
    return create_proposal(
        run_id="run-rt",
        ticker="AAPL",
        trade_date="2026-06-10",
        signal=signal,
        rating=signal,
        price=price,
        proposal_id=proposal_id or f"prop-rt-{utcnow_iso()[-9:]}",
        evidence_id=evidence_id,
    )


def test_register_proposal_returns_record_with_advisory_terms(store):
    proposal = _proposal()
    record = store.register_proposal(proposal)
    assert record.proposal_id == proposal.proposal_id
    assert record.status == ProposalStatus.PENDING_REVIEW
    stored = store.get_proposal(proposal.proposal_id)
    assert stored is not None


def test_approved_repeated_unchanged_registration_preserves_shares(store):
    proposal = _proposal(proposal_id="prop-rt-shares")
    original = store.register_proposal(proposal)
    approved = approve(original, shares=42, operator="leo")
    store.save_proposal(approved)
    assert store.get_proposal(proposal.proposal_id).shares == 42

    again = store.register_proposal(proposal)
    assert again.shares == 42
    assert store.get_proposal(proposal.proposal_id).shares == 42
    assert again.approved_version == approved.approved_version


def test_rejected_proposal_retains_status_and_execution(store):
    proposal = _proposal(proposal_id="prop-rt-rej")
    original = store.register_proposal(proposal)
    rejected = reject(original, operator="leo")
    store.update_proposal_status(
        proposal.proposal_id, ProposalStatus.REJECTED, operator="leo", reason=rejected.reason
    )
    stored = store.get_proposal(proposal.proposal_id)
    assert stored.status == ProposalStatus.REJECTED
    assert stored.reason == "rejected by operator"

    again = store.register_proposal(proposal)
    assert again.status == ProposalStatus.REJECTED
    assert store.get_proposal(proposal.proposal_id).status == ProposalStatus.REJECTED


def test_amended_evidence_known_id_requires_fresh_review(store):
    proposal = _proposal(proposal_id="prop-rt-amend")
    original = store.register_proposal(proposal)
    approved = approve(original, shares=100, operator="leo")
    store.save_proposal(approved)

    amended = _proposal(proposal_id=proposal.proposal_id, evidence_id="ev-2")
    record = store.register_proposal(amended)
    assert record.price == 100.0
    assert record.status == ProposalStatus.PENDING_REVIEW
    assert not record.approved_version

    executed, execution = execute(store, record, operator="leo")
    assert executed.status != ProposalStatus.SIMULATED
    assert execution.executed is False


def test_executed_proposal_stays_simulated_on_repeat(store):
    proposal = _proposal(proposal_id="prop-rt-exec")
    original = store.register_proposal(proposal)
    approved = approve(original, shares=100, operator="leo")
    store.save_proposal(approved)

    updated, execution = execute(store, store.get_proposal(proposal.proposal_id), operator="leo")
    assert updated.status == ProposalStatus.SIMULATED
    assert execution.executed is True
    tx_id = execution.tx_id
    ledger_before = store.get_ledger().model_dump()

    again = store.register_proposal(proposal)
    assert again.status == ProposalStatus.SIMULATED
    stored = store.get_proposal(proposal.proposal_id)
    assert stored.status == ProposalStatus.SIMULATED

    re, rex = execute(store, stored, operator="leo")
    assert re.status == ProposalStatus.SIMULATED
    assert rex.executed is True
    assert rex.tx_id == tx_id
    assert store.get_ledger().model_dump() == ledger_before


def test_legacy_pack_roundtrip_material_identity(pack_io, tmp_path):
    pack = pack_io.import_pack("test/fixtures/packs/aapl_buy_complete")
    assert pack.proposal.evidence_id

    out = tmp_path / "exported"
    pack_io.export(pack, out)
    reimported = pack_io.import_pack(out)
    assert reimported.proposal.evidence_id == pack.proposal.evidence_id

    initial = reimported.proposal.evidence_id
    reimported.input.available_sources["sentinel"] = {"note": "changed"}
    out2 = tmp_path / "exported-changed"
    pack_io.export(reimported, out2)
    changed = pack_io.import_pack(out2)
    assert changed.proposal.evidence_id
    assert changed.proposal.evidence_id != initial
