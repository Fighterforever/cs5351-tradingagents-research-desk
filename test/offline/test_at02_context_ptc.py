"""AT-02 / SEC-001 / QUALITY-001: time-aware context and de-duplication.

Historical runs must not learn from outcomes that were only known after the
trade date; repeated source text is de-duplicated while staying traceable; and
material with an unknown availability time is explicitly marked as unsuitable
for historical evaluation.
"""

from __future__ import annotations

from research_desk.context import ContextAssembler, StandingConstraints, dedup_repeated_blocks
from research_desk.models import ContextMode

FUTURE_ENTRY = {
    "date": "2026-06-01",
    "ticker": "NVDA",
    "rating": "Buy",
    "decision": "DECISION:\nBought NVDA and it worked.",
    "reflection": "REFLECTION:\n+5.2% after the trade date.",
    "resolved": "2026-07-20",  # outcome known only in July
}

PAST_ENTRY = {
    "date": "2026-05-01",
    "ticker": "NVDA",
    "rating": "Overweight",
    "decision": "DECISION:\nData-center demand strong.",
    "reflection": "REFLECTION:\nWorked out.",
    "resolved": "2026-05-15",
}

NO_RESOLUTION_ENTRY = {
    "date": "2026-04-01",
    "ticker": "NVDA",
    "rating": "Hold",
    "decision": "DECISION:\nValuation elevated.",
    "reflection": "REFLECTION:\nStill pending outcome.",
    "resolved": None,
}

LONG_ENTRY = {
    "date": "2026-03-01",
    "ticker": "NVDA",
    "rating": "Hold",
    "decision": "DECISION:\n" + ("Range-bound tape. " * 400),
    "reflection": "REFLECTION:\n" + ("No conviction either way. " * 400),
    "resolved": "2026-03-15",
}


def _assembler() -> ContextAssembler:
    constraints = StandingConstraints(
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
    return ContextAssembler(constraints)


def test_future_known_lesson_excluded_at_cutoff():
    """SEC-001: an outcome resolved after the trade date is excluded."""
    result = _assembler().assemble_from_entries(
        [FUTURE_ENTRY, PAST_ENTRY], ContextMode.BASELINE, as_of="2026-06-10"
    )
    assert "Bought NVDA" not in result.text  # future knowledge excluded
    assert "Data-center demand strong" in result.text  # past knowledge kept


def test_without_cutoff_future_lesson_is_kept():
    result = _assembler().assemble_from_entries(
        [FUTURE_ENTRY, PAST_ENTRY], ContextMode.BASELINE
    )
    assert "Bought NVDA" in result.text


def test_unknown_availability_marked_for_historical_eval():
    result = _assembler().assemble_from_entries(
        [NO_RESOLUTION_ENTRY], ContextMode.BASELINE, as_of="2026-06-10"
    )
    assert "not suitable for historical evaluation" in result.text


def test_dedup_repeated_reports_keeps_traceability():
    text = "report A\n\nreport B\n\nreport A\n\nreport C"
    deduped = dedup_repeated_blocks(text)
    assert deduped.count("report A") == 1
    assert deduped.count("report B") == 1
    assert deduped.count("report C") == 1
    assert deduped.index("report A") < deduped.index("report B")


def test_compact_bound_earlier_history():
    """The long entry is bounded so compact stays short but complete on facts."""
    assembler = _assembler()
    baseline = assembler.assemble_from_entries([LONG_ENTRY], ContextMode.BASELINE)
    compact = assembler.assemble_from_entries([LONG_ENTRY], ContextMode.COMPACT)
    assert compact.truncated is True
    assert compact.chars < baseline.chars
    assert "Range-bound tape." in compact.text


def test_compact_preserves_identity_date_price_constraints():
    """FR-003: compaction keeps the standing constraints verbatim."""
    from research_desk.evidence import EvidencePackIO

    pack = EvidencePackIO().import_pack("test/fixtures/packs/nvda_compact_memory")
    assembler = _assembler()
    entries = pack.input.memory_used
    baseline = assembler.assemble_from_entries(entries, ContextMode.BASELINE)
    compact = assembler.assemble_from_entries(entries, ContextMode.COMPACT)
    for needle in [
        "NVDA",
        "2026-06-10",
        "last_close",
        "137.0",
        "USD 100000",
        "10% of equity",
        "integer_shares",
        "no_shorting",
        "research-desk analysis",
    ]:
        assert needle in compact.text, f"compact dropped {needle!r}"
    assert compact.chars <= baseline.chars  # compact never grows the context
    assert compact.deduplicated >= 1  # repeated report body collapsed


def test_collection_and_cutoff_dates_distinct():
    """The pack keeps the memory source and the assembler applies the cutoff separately."""
    from research_desk.context import ContextAssembler
    from research_desk.evidence import EvidencePackIO

    pack = EvidencePackIO().import_pack("test/fixtures/packs/nvda_compact_memory")
    entries = pack.input.memory_used
    assert all(e["resolved"] for e in entries)  # collection/availability recorded
    assembler = ContextAssembler(StandingConstraints(ticker="NVDA", trade_date="2026-06-10"))
    as_of = "2026-04-01"
    kept = assembler.assemble_from_entries(entries, ContextMode.BASELINE, as_of=as_of)
    assert "2026-04-15" not in kept.text  # resolved 2026-04-30 > 2026-04-01
    assert "2026-03-01" in kept.text  # resolved 2026-03-15 <= 2026-04-01
