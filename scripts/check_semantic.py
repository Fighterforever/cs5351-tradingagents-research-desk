"""Gate 4: fixed semantic regression over captured evidence and the frozen corpus.

Two deterministic offline parts, clearly labelled (this is NOT a claim of fresh
live-model quality):

A. Captured-output regression: every committed evidence pack under
   ``test/fixtures/packs`` is replayed with networking blocked for ALL replays,
   compared against hard-coded fixed expected decisions and preserved source
   facts, with deterministic policy/budget properties rechecked. The fixed pack
   names are required so deleting one cannot make the suite pass.

B. AT-07 deterministic prompt-transform regression over the real frozen
   six-case corpus in ``src/research_desk/eval`` (``case_registry.all_cases`` +
   ``compact_delegate.compact_transform``): builds a grounded message from each
   case's real fields, runs the real compact transform, and verifies that the
   retained output preserves symbol / date / price / source identifiers and
   numeric facts. The 2 development / 4 held-out split is verified.

The synthetic padding in part B is ONLY an offline stress input to prove fact
retention under compaction; it is never presented as a live token-saving
baseline. No provider request is ever made. Live judge/CLI output evaluation is
a separate recorded release experiment owned by the source/evaluation thread.
"""

from __future__ import annotations

import argparse
import socket
import sys
import tempfile
from pathlib import Path

from _gate_lib import add_change_args, changed_files, fail, resolve_root

# Committed fixture packs that must exist (deleting one must fail the gate).
REQUIRED_PACKS = ("aapl_buy_complete", "msft_review", "tsla_hold", "nvda_compact_memory")

# Fixed expected outcomes for the committed fixture corpus (offline regression).
EXPECTED = {
    "aapl_buy_complete": {
        "signal": "Buy",
        "ticker": "AAPL",
        "price": 100.0,
        "proposal": True,
        "max_by_cap": 100,
        "max_by_cash": 1000,
    },
    "msft_review": {"signal": "REVIEW", "proposal": False},
    "tsla_hold": {"signal": "Hold", "proposal": False},
    "nvda_compact_memory": {
        "signal": "Buy",
        "ticker": "NVDA",
        "price": 137.0,
        "proposal": True,
        "max_by_cap": 72,
        "max_by_cash": 729,
    },
}


class _NetworkBlock:
    """Blocks real socket I/O and counts any attempted external call."""

    def __init__(self) -> None:
        self.attempts = 0

    def _block(self, *args, **kwargs):  # noqa: ANN002,ANN003
        self.attempts += 1
        raise OSError("network blocked during offline gate")


def _grounded_message(case: dict) -> str:
    """A grounded prompt carrying each case's real identity/date/price/source facts."""
    lines = [
        "STANDING ANALYSIS CONSTRAINTS (always true for this run):",
        f"Instrument identity: {case['ticker']}",
        f"Company: {case['identity']['company_name']}",
        f"Sector/industry: {case['identity']['sector']} / {case['identity']['industry']}",
        f"Analysis date: {case['analysis_date']}",
        f"Announcement date: {case['announcement_date']}",
        f"last_close: {case['latest_close']}",
        f"source_id: {case['source_id']}",
        f"source_url: {case['source_url']}",
        "Evidence notes:",
    ]
    lines += [f"- {note}" for note in case["notes"]]
    lines.append("Balance guidance: " + case["balance"])
    # Synthetic verbose padding: an OFFLINE stress input only, to prove fact
    # retention when compaction trimming would otherwise apply. This is not a
    # live token-saving baseline.
    for i in range(8):
        lines.append(f"verbose analyst draft paragraph {i}: " + "non-grounding filler text. " * 30)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gate 4: fixed semantic regression (offline captured + prompt-transform)."
    )
    add_change_args(parser)
    parser.add_argument("--packs-dir", default="test/fixtures/packs")
    args = parser.parse_args()

    root: Path = resolve_root(args.root)
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "src"))

    checks: list[str] = []
    failures: list[str] = []

    net = _NetworkBlock()
    socket.socket.connect = net._block
    socket.socket.sendall = net._block
    socket.socket.recv = net._block
    socket.getaddrinfo = net._block

    packs_dir = root / args.packs_dir
    if not packs_dir.is_dir():
        fail(checks, [f"fixture packs dir missing: {packs_dir}"])
    present = {p.name for p in packs_dir.iterdir() if (p / "manifest.json").exists()}
    for name in REQUIRED_PACKS:
        if name not in present:
            failures.append(f"required fixed pack missing: {name}")
    checks.append(f"FIXED_CORPUS_PACKS={len(present)}")
    checks.append(f"REQUIRED_PACKS={len(REQUIRED_PACKS)}")

    from research_desk.evidence import EvidencePackIO
    from research_desk.models import LedgerState
    from research_desk.policy import policy_bounds
    from research_desk.replay import ReplayEngine

    io = EvidencePackIO()
    engine = ReplayEngine()

    for pack_name in REQUIRED_PACKS:
        pack_dir = packs_dir / pack_name
        if not pack_dir.is_dir():
            continue  # absence already reported above
        expected = EXPECTED[pack_name]
        try:
            pack = io.import_pack(str(pack_dir))
        except Exception as exc:  # noqa: BLE001 - surface as a failure
            failures.append(f"pack {pack_name} failed to import: {exc}")
            continue

        if expected.get("ticker") and pack.manifest.ticker != expected["ticker"]:
            failures.append(f"{pack_name}: ticker {pack.manifest.ticker!r} != {expected['ticker']!r}")
        if pack.manifest.signal != expected["signal"]:
            failures.append(
                f"{pack_name}: manifest signal {pack.manifest.signal!r} != expected {expected['signal']!r}"
            )
        if not pack.manifest.trade_date:
            failures.append(f"{pack_name}: missing trade_date in manifest")
        if not pack.manifest.prompt_version:
            failures.append(f"{pack_name}: missing prompt_version in manifest")

        with tempfile.TemporaryDirectory() as tmp:
            try:
                result = engine.replay(pack, Path(tmp), ledger=LedgerState(cash=100000.0))
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{pack_name}: replay raised {exc}")
                continue
            if result.external_calls != 0:
                failures.append(f"{pack_name}: replay reported {result.external_calls} external calls")
            if result.signal != expected["signal"]:
                failures.append(f"{pack_name}: replayed signal {result.signal!r} != expected {expected['signal']!r}")
            if result.signal != pack.manifest.signal:
                failures.append(
                    f"{pack_name}: replayed signal {result.signal!r} != manifest {pack.manifest.signal!r}"
                )

        prop = pack.proposal
        if expected["proposal"]:
            if prop is None:
                failures.append(f"{pack_name}: expected a PENDING_REVIEW proposal, got none")
            else:
                if prop.price is not None and abs(prop.price - expected["price"]) > 1e-9:
                    failures.append(f"{pack_name}: proposal price {prop.price} != {expected['price']}")
                bounds = policy_bounds(LedgerState(cash=100000.0), pack.manifest.ticker, prop.price)
                if bounds.get("max_by_cap") != expected["max_by_cap"]:
                    failures.append(f"{pack_name}: max_by_cap {bounds.get('max_by_cap')} != {expected['max_by_cap']}")
                if bounds.get("max_by_cash") != expected["max_by_cash"]:
                    failures.append(f"{pack_name}: max_by_cash {bounds.get('max_by_cash')} != {expected['max_by_cash']}")
        else:
            if prop is not None:
                failures.append(f"{pack_name}: expected no proposal for {expected['signal']}, got one")

        usage = pack.usage
        if usage.total_tokens != usage.input_tokens + usage.output_tokens:
            failures.append(
                f"{pack_name}: usage total {usage.total_tokens} != input {usage.input_tokens} + output {usage.output_tokens}"
            )
        if usage.stop_reason not in {"completed", "budget_exhausted", "error"}:
            failures.append(f"{pack_name}: unknown usage stop_reason {usage.stop_reason!r}")

    # --- AT-07 deterministic prompt-transform regression over the frozen corpus ---
    try:
        from research_desk.eval.case_registry import all_cases
        from research_desk.eval.compact_delegate import compact_transform
    except ImportError as exc:
        failures.append(f"AT-07 eval module missing under src/research_desk/eval: {exc}")
        all_cases = None  # type: ignore[assignment]
        compact_transform = None  # type: ignore[assignment]

    if all_cases is not None:
        cases = all_cases()
        checks.append(f"AT07_CORPUS_CASES={len(cases)}")
        if len(cases) != 6:
            failures.append(f"expected 6 frozen evaluation cases, got {len(cases)}")
        dev = [c for c in cases if c.get("split") == "development"]
        held = [c for c in cases if c.get("split") == "held_out"]
        checks.append(f"AT07_SPLIT: development={len(dev)}, held_out={len(held)}")
        if len(dev) != 2 or len(held) != 4:
            failures.append(f"AT-07 split must be 2 development / 4 held-out; got {len(dev)}/{len(held)}")

        for case in cases:
            ticker = case["ticker"]
            csv_path = Path(case["csv_path"])
            if not csv_path.exists():
                failures.append(f"AT-07 case {ticker}: csv missing -> {csv_path}")
            out = compact_transform(_grounded_message(case))
            out_text = "\n".join(
                m.content if isinstance(m.content, str) else str(m.content)
                for m in (out if isinstance(out, list) else [out])
            )
            facts = [
                ticker,
                case["analysis_date"],
                str(case["latest_close"]),
                case["source_id"],
                case["source_url"],
            ]
            for fact in facts:
                if fact not in out_text:
                    failures.append(f"AT-07 case {ticker}: compact output dropped fact {fact!r}")
            for note in case["notes"]:
                if note not in out_text:
                    failures.append(f"AT-07 case {ticker}: compact output dropped a numeric note")
                    break

    checks.append(
        "GATE4_OFFLINE_SCOPE=fixed captured-output replay + deterministic prompt-transform "
        "regression (no live model quality claim)"
    )
    checks.append(
        "PADDING=offline fact-retention stress input only; NOT a live token-saving baseline"
    )

    if net.attempts:
        failures.append(f"network access attempted during offline gate ({net.attempts} attempt(s))")
    else:
        checks.append("external network calls attempted: 0")

    changed = changed_files(root, args.base_ref, args.head_ref, args.changed_files)
    if changed:
        prompt_changes = [
            c for c in changed
            if c.endswith(".py") or "prompt" in c.lower() or "/prompts/" in c
        ]
        if prompt_changes:
            checks.append(
                f"prompt/model change detected ({len(prompt_changes)} file(s)); "
                "fixed captured-output + prompt-transform gate applies (live quality "
                "requires the recorded release experiment)"
            )

    fail(checks, failures)


if __name__ == "__main__":
    main()
