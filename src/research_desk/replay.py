"""Offline replay of a complete evidence pack.

Replay imports a saved pack (directory or ZIP), validates that it is complete,
then rebuilds the deterministic outputs with **zero external calls**: the
report tree from the captured final state, the structured signal via the same
deterministic heuristic the graph uses, and the policy verdict for the pack's
proposal against a supplied ledger.

This is the *offline reproduction* path. It is deliberately distinct from a
controlled LLM rerun (``data_mode="frozen"`` in the runner), which re-executes
the real graph over frozen evidence. Replay never starts an LLM request.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from tradingagents.graph.signal_processing import SignalProcessor
from tradingagents.reporting import write_report_tree

from .evidence import EvidencePackIO
from .models import EvidencePack
from .policy import PolicyVerdict, evaluate_buy, evaluate_sell, policy_bounds


@dataclass
class ReplayResult:
    pack: EvidencePack
    signal: str | None = None
    report_files: list[str] = field(default_factory=list)
    policy_verdict: PolicyVerdict | None = None
    policy_bounds: dict | None = None
    external_calls: int = 0  # always 0 for offline replay
    incomplete: bool = False
    error: str | None = None


class ReplayEngine:
    """Rebuilds reports, signal and policy outputs from a complete evidence pack."""

    def __init__(self, io: EvidencePackIO | None = None):
        self.io = io or EvidencePackIO()
        # Deterministic heuristic; the graph constructs it the same way.
        self._signal_processor = SignalProcessor()

    def load(self, source: str | Path) -> EvidencePack:
        return self.io.import_pack(source)

    def replay(
        self,
        source: str | Path | EvidencePack,
        out_dir: str | Path,
        ledger=None,
    ) -> ReplayResult:
        """Rebuild the pack's outputs under ``out_dir`` with no network calls."""
        pack = source if isinstance(source, EvidencePack) else self.load(source)
        result = ReplayResult(pack=pack)

        if pack.manifest.outcome == "completed" and not pack.final_state:
            result.incomplete = True
            result.error = "pack claims completion but has no final_state"
            return result

        signal = None
        if pack.final_state.get("final_trade_decision"):
            signal = self._signal_processor.process_signal(
                pack.final_state["final_trade_decision"]
            )
        result.signal = signal

        out = Path(out_dir)
        try:
            complete = write_report_tree(pack.final_state, pack.manifest.ticker, out)
            result.report_files = [str(p) for p in out.rglob("*") if p.is_file()]
            if complete not in result.report_files:
                result.report_files.append(str(complete))
        except Exception as exc:  # noqa: BLE001 - report rebuild is best-effort
            result.error = f"report rebuild failed: {exc}"

        if ledger is not None and pack.proposal is not None:
            prop = pack.proposal
            result.policy_bounds = policy_bounds(ledger, prop.ticker, prop.price)
            if prop.shares is not None and prop.price is not None:
                verdict = (
                    evaluate_sell(ledger, prop.ticker, prop.shares, prop.price)
                    if prop.side == "sell"
                    else evaluate_buy(ledger, prop.ticker, prop.shares, prop.price)
                )
                result.policy_verdict = verdict
            else:
                result.policy_verdict = PolicyVerdict(
                    allowed=False,
                    checks=[
                        {
                            "check": "proposal_material",
                            "passed": False,
                            "detail": "proposal missing operator shares (supplied at approval); "
                            "policy bounds are reported instead",
                        }
                    ],
                )

        return result
