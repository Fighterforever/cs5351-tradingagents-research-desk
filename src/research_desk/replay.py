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
from .report import apply_research_identity_header, render_research_identity


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
        before = _file_state(out)
        complete: Path | None = None
        try:
            complete = write_report_tree(pack.final_state, pack.manifest.ticker, out)
            apply_research_identity_header(complete, render_research_identity(pack))
        except Exception as exc:  # noqa: BLE001 - report rebuild is best-effort
            result.error = f"report rebuild failed: {exc}"
        finally:
            result.report_files = _written_files(out, before, complete)

        if ledger is not None and pack.proposal is not None:
            prop = pack.proposal
            result.policy_bounds = _policy_bounds_for(ledger, prop)
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


def _file_state(root: Path) -> dict[str, tuple[int, int]]:
    """Snapshot existing files so unrelated preexisting output is not counted."""
    if not root.exists():
        return {}
    state: dict[str, tuple[int, int]] = {}
    for path in root.rglob("*"):
        if path.is_file():
            stat = path.stat()
            state[str(path)] = (stat.st_mtime_ns, stat.st_size)
    return state


def _written_files(
    root: Path, before: dict[str, tuple[int, int]], complete: Path | None
) -> list[str]:
    """Unique files this replay actually wrote (new or changed), as strings."""
    written: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        stat = path.stat()
        if before.get(str(path)) != (stat.st_mtime_ns, stat.st_size):
            written.add(str(path))
    if complete is not None:
        written.add(str(complete))
    return sorted(written)


def _policy_bounds_for(ledger, prop) -> dict:
    """Deterministic bounds, using the policy owner for buy and sell semantics."""
    bounds = policy_bounds(ledger, prop.ticker, prop.price)
    if prop.side != "sell":
        return bounds

    position = ledger.positions.get(prop.ticker.upper())
    owned = position.shares if position is not None else 0
    bounds = dict(bounds)
    bounds["side"] = "sell"
    bounds["max_sell"] = owned
    # A sale never adds shares and needs no cash; report nonnegative limits
    # instead of the buy-oriented additional-share/cash caps.
    bounds["max_by_cap"] = 0
    bounds["max_by_cash"] = 0
    return bounds
