"""Research Desk CLI: analyze, export, replay, propose, review, execute, ledger, compare.

Every feature the offline slice needs is reachable here. The review/execute/
ledger paths are operator-only: an LLM never reaches them.
"""

from __future__ import annotations

import getpass
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from .config import ResearchDeskSettings
from .evidence import EvidencePackIO
from .graph_adapter import ResearchRunner
from .models import ContextMode, ProposalStatus, RunOutcome, RunResult
from .replay import ReplayEngine
from .report import (
    render_compare_report,
    render_ledger_report,
)
from .review import ReviewError, approve as _approve, execute as _execute, reject as _reject
from .storage import ResearchDeskStore

app = typer.Typer(
    name="research-desk",
    help="CS5351 TradingAgents Research Desk: evidence packs, simulated ledger, compact context.",
    add_completion=False,
)

console = Console()


def _settings() -> ResearchDeskSettings:
    return ResearchDeskSettings()


def _store(settings: ResearchDeskSettings | None = None) -> ResearchDeskStore:
    settings = settings or _settings()
    settings.ensure_dirs()
    return ResearchDeskStore(settings.db_path)


def _default_operator() -> str:
    try:
        return getpass.getuser()
    except Exception:  # noqa: BLE001
        return "operator"


# ---------------------------------------------------------------------------
# analyze
# ---------------------------------------------------------------------------


@app.command()
def analyze(
    ticker: str = typer.Argument(..., help="US equity ticker, e.g. AAPL"),
    trade_date: str = typer.Argument(..., help="Analysis date YYYY-MM-DD"),
    context_mode: str = typer.Option("baseline", "--context-mode", help="baseline | compact"),
    data_mode: str = typer.Option("live", "--data-mode", help="live | frozen"),
    max_calls: int | None = typer.Option(None, "--max-calls", help="LLM call budget"),
    fixture: str | None = typer.Option(None, "--fixture", help="Source pack for a frozen rerun"),
    no_proposal: bool = typer.Option(False, "--no-proposal", help="Do not create a proposal"),
    analysts: str = typer.Option("market,news", "--analysts", help="Comma-separated analyst keys"),
):
    """Run a research session against the real TradingAgentsGraph and capture evidence."""
    settings = _settings()
    settings.analysts = tuple(a.strip() for a in analysts.split(",") if a.strip())
    settings.max_calls = max_calls
    settings.ensure_dirs()

    source_pack = None
    if data_mode == "frozen":
        if not fixture:
            raise typer.BadParameter("--data-mode frozen requires --fixture <evidence pack>")
        source_pack = EvidencePackIO().import_pack(fixture)

    runner = ResearchRunner(
        settings,
        context_mode=context_mode,
        data_mode=data_mode,
        source_pack=source_pack,
    )
    with console.status(f"Running research on {ticker} ({trade_date})..."):
        result = runner.run(ticker, trade_date)

    store = _store(settings)
    if result.proposal is not None and not no_proposal:
        store.save_proposal(result.proposal)
    store.close()

    _print_run_result(result)
    if result.outcome == RunOutcome.BUDGET_STOPPED.value:
        console.print(
            "[yellow]Budget stopped: incomplete research returned, no approvable "
            "recommendation was created (NFR-003).[/yellow]"
        )


def _print_run_result(result: RunResult) -> None:
    table = Table(title=f"Run {result.run_id}")
    table.add_column("field")
    table.add_column("value")
    rows = [
        ("ticker", result.ticker),
        ("trade_date", result.trade_date),
        ("outcome", result.outcome),
        ("signal", result.signal or "n/a"),
        ("LLM calls", str(result.usage.calls)),
        ("input tokens", str(result.usage.input_tokens)),
        ("output tokens", str(result.usage.output_tokens)),
        ("stop reason", result.stop_reason or "n/a"),
        ("pack", result.pack_path or "n/a"),
    ]
    if result.proposal is not None:
        rows.append(("proposal", result.proposal.proposal_id))
        rows.append(("proposal status", result.proposal.status.value))
        rows.append(("price (evidence)", str(result.proposal.price)))
    if result.error:
        rows.append(("error", result.error))
    for name, value in rows:
        table.add_row(name, value)
    console.print(table)


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------


@app.command()
def export(
    run_id: str = typer.Argument(...),
    out: str | None = typer.Option(None, "--out", help="Output ZIP path"),
):
    """Package a run's evidence pack as a portable ZIP (self-contained)."""
    settings = _settings()
    run_dir = settings.runs_dir / run_id
    if not run_dir.exists():
        raise typer.BadParameter(f"run {run_id!r} not found under {settings.runs_dir}")
    io = EvidencePackIO()
    pack = io.import_pack(run_dir)
    zip_path = out or str(settings.runs_dir / f"{run_id}.zip")
    io.export_zip(pack, zip_path)
    console.print(f"[green]Exported {run_id} to {zip_path}[/green]")


# ---------------------------------------------------------------------------
# replay
# ---------------------------------------------------------------------------


@app.command()
def replay(
    source: str = typer.Argument(...),
    out: str | None = typer.Option(None, "--out", help="Directory to rebuild reports into"),
    with_ledger: bool = typer.Option(False, "--ledger", help="Evaluate proposal policy against the current ledger"),
):
    """Offline replay of a complete evidence pack (zero external calls)."""
    engine = ReplayEngine()
    settings = _settings()
    out_dir = out or str(settings.reports_dir / f"replay-{Path(source).stem}")
    ledger = None
    if with_ledger:
        ledger = _store(settings).get_ledger()
    result = engine.replay(source, out_dir, ledger=ledger)
    console.print(f"[green]Replayed {result.pack.manifest.run_id}[/green] (external calls: {result.external_calls})")
    console.print(f"signal: {result.signal or 'n/a'}")
    console.print(f"reports: {len(result.report_files)} files under {out_dir}")
    if result.incomplete:
        raise typer.Exit(f"incomplete pack: {result.error}")
    if result.policy_bounds is not None:
        bounds = result.policy_bounds
        if bounds.get("price_present"):
            console.print(
                f"policy: max {bounds['max_by_cap']} shares by 10% cap, "
                f"max {bounds['max_by_cash']} by cash, on equity ${bounds['equity']:,.2f}"
            )
        else:
            console.print("policy: price missing from evidence; nothing is executable")
    if result.policy_verdict is not None:
        console.print(f"policy allowed: {result.policy_verdict.allowed}")
        for c in result.policy_verdict.checks:
            console.print(f"  - {c['check']}: {'PASS' if c['passed'] else 'FAIL'} ({c['detail']})")


# ---------------------------------------------------------------------------
# propose
# ---------------------------------------------------------------------------


@app.command()
def propose(
    run_id: str = typer.Argument(...),
    shares: int | None = typer.Option(None, "--shares", help="Operator share count (positive integer)"),
    operator: str = typer.Option(None, "--operator", help="Operator identity (defaults to local user)"),
):
    """Register a run's PENDING_REVIEW proposal in the ledger store."""
    settings = _settings()
    io = EvidencePackIO()
    pack = io.import_pack(settings.runs_dir / run_id)
    if pack.proposal is None:
        raise typer.BadParameter(f"run {run_id!r} has no proposal (signal not tradeable or budget stopped)")
    store = _store(settings)
    store.save_proposal(pack.proposal)
    console.print(f"[green]Proposal {pack.proposal.proposal_id} registered (status {pack.proposal.status.value})[/green]")
    store.close()


# ---------------------------------------------------------------------------
# review / execute / ledger
# ---------------------------------------------------------------------------


@app.command()
def review(
    action: str = typer.Argument(..., help="approve | reject"),
    proposal_id: str = typer.Argument(...),
    shares: int | None = typer.Option(None, "--shares", help="Shares to approve (approve only)"),
    operator: str = typer.Option(None, "--operator", help="Operator identity (defaults to local user)"),
):
    """Approve or reject a PENDING_REVIEW proposal (operator-only)."""
    store = _store()
    proposal = store.get_proposal(proposal_id)
    if proposal is None:
        raise typer.BadParameter(f"no proposal {proposal_id!r}")
    op = operator or _default_operator()
    try:
        if action == "approve":
            if shares is None:
                raise typer.BadParameter("approve requires --shares <positive int>")
            updated = _approve(proposal, shares=shares, operator=op)
            store.save_proposal(updated)  # persists shares, status, version binding
            console.print(
                f"[green]Approved {proposal_id} ({proposal.ticker}, {proposal.signal}) "
                f"for {shares} shares at ${proposal.price or 'n/a'} by {op}[/green]"
            )
        elif action == "reject":
            updated = _reject(proposal, operator=op)
            store.update_proposal_status(
                proposal.proposal_id, ProposalStatus.REJECTED, operator=op, reason=updated.reason
            )
            console.print(f"[yellow]Rejected {proposal_id} by {op}[/yellow]")
        else:
            raise typer.BadParameter("action must be approve | reject")
    except ReviewError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from None
    finally:
        store.close()


@app.command()
def execute(
    proposal_id: str = typer.Argument(...),
    operator: str = typer.Option(None, "--operator", help="Operator identity (defaults to local user)"),
):
    """Re-evaluate the current ledger and simulate an approved buy (idempotent)."""
    store = _store()
    proposal = store.get_proposal(proposal_id)
    if proposal is None:
        raise typer.BadParameter(f"no proposal {proposal_id!r}")
    op = operator or _default_operator()
    try:
        updated, execution = _execute(store, proposal, operator=op)
        if execution.executed:
            ledger_state = store.get_ledger()
            cash = ledger_state.cash if ledger_state is not None else 0.0
            console.print(
                f"[green]Simulated {updated.side}: {updated.ticker} {updated.shares} sh @ ${updated.price:.2f} "
                f"(tx {execution.tx_id}) — cash now ${cash:,.2f}[/green]"
            )
        else:
            console.print(
                f"[yellow]Not executed: {execution.reason or 'policy failed at execution time'}. "
                f"Ledger unchanged.[/yellow]"
            )
    except ReviewError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from None
    finally:
        store.close()


@app.command()
def ledger(report: bool = typer.Option(False, "--report", help="Print full markdown report")):
    """Show the current simulated ledger, proposals and transactions."""
    store = _store()
    state = store.get_ledger()
    if state is None:
        store.close()
        raise typer.BadParameter("ledger is not initialised")
    proposals = store.list_proposals()
    txs = store.list_transactions()
    table = Table(title="Ledger")
    table.add_column("field")
    table.add_column("value")
    table.add_row("cash", f"USD {state.cash:,.2f}")
    table.add_row("equity", f"USD {state.equity:,.2f}")
    for ticker, pos in sorted(state.positions.items()):
        table.add_row(f"position {ticker}", f"{pos.shares} sh @ {pos.avg_price or 'n/a'}")
    console.print(table)
    if report:
        console.print(Markdown(render_ledger_report(state, txs, proposals)))
    store.close()


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------


@app.command()
def compare(
    source: str = typer.Argument(...),
    max_calls: int | None = typer.Option(None, "--max-calls"),
    analysts: str = typer.Option("market,news", "--analysts"),
):
    """Run baseline and compact arms on the same frozen evidence (FR-003).

    Requires live LLM credentials; it genuinely re-runs the same graph on the
    same frozen evidence with different context assembly.
    """
    settings = _settings()
    settings.analysts = tuple(a.strip() for a in analysts.split(",") if a.strip())
    settings.max_calls = max_calls
    settings.ensure_dirs()
    pack = EvidencePackIO().import_pack(source)

    arms = {}
    for mode in (ContextMode.BASELINE.value, ContextMode.COMPACT.value):
        runner = ResearchRunner(
            settings, context_mode=mode, data_mode="frozen", source_pack=pack
        )
        start = time.time()
        result = runner.run(pack.manifest.ticker, pack.manifest.trade_date)
        wall = time.time() - start
        store = _store(settings)
        if result.proposal is not None:
            store.save_proposal(result.proposal)
        store.close()
        arms[mode] = {
            "calls": result.usage.calls,
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
            "total_tokens": result.usage.total_tokens,
            "wall_seconds": round(wall, 3),
            "stop_reason": result.stop_reason or "n/a",
            "context_chars": _context_chars(result),
            "signal": result.signal,
        }
    console.print(Markdown(render_compare_report(arms[ContextMode.BASELINE.value], arms[ContextMode.COMPACT.value])))


def _context_chars(result: RunResult) -> int:
    for ev in result.events:
        if ev.kind == "context_assembled":
            return int(ev.payload.get("chars", 0))
    return 0


# ---------------------------------------------------------------------------
# live evaluation: evaluate-case / judge-case / aggregate
# ---------------------------------------------------------------------------


@app.command("evaluate-case")
def evaluate_case(
    ticker: str = typer.Argument(..., help="Frozen evaluation ticker, e.g. NVDA"),
    mode: str = typer.Option("baseline", "--mode", help="baseline | compact"),
    out: str = typer.Option(..., "--out", help="Output root directory"),
    max_calls: int | None = typer.Option(None, "--max-calls", help="LLM call budget"),
):
    """Run one frozen case through the real graph with real DeepSeek clients."""
    from .eval.live import run_evaluate_case

    with console.status(f"Running {ticker} {mode} (real DeepSeek)..."):
        summary = run_evaluate_case(ticker, mode, out, max_calls=max_calls)
    console.print(
        f"[green]{ticker} [{mode}] outcome={summary['outcome']} "
        f"signal={summary['signal'] or 'n/a'} calls={summary['calls']} "
        f"tokens={summary['total_tokens']} wall={summary['wall_seconds']}s[/green]"
    )
    console.print(f"  run dir: {summary['run_dir']}")
    if summary.get("error"):
        console.print(f"  [red]error: {summary['error']}[/red]")


@app.command("judge-case")
def judge_case(
    ticker: str = typer.Argument(..., help="Frozen evaluation ticker"),
    out: str = typer.Option(..., "--out", help="Output root directory (same as evaluate-case)"),
    max_calls: int | None = typer.Option(None, "--max-calls", help="Judge LLM call budget"),
):
    """Independently judge a completed run's report with a real DeepSeek evaluator."""
    from .eval.live import run_judge_case

    with console.status(f"Judging {ticker} (real DeepSeek evaluator)..."):
        result = run_judge_case(ticker, out, max_calls=max_calls)
    for mode, score in result.get("arms", {}).items():
        if isinstance(score, dict) and not score.get("error"):
            console.print(
                f"[green]{ticker} [{mode}] support={score['support']} "
                f"relevance={score['relevance']}[/green]"
            )
        else:
            console.print(f"[yellow]{ticker} [{mode}] not judged: {score}[/yellow]")


@app.command("aggregate")
def aggregate(
    out: str = typer.Argument(..., help="Output root directory containing ticker arms"),
):
    """Compute six paired baseline/compact metrics from existing run outputs."""
    from .eval.live import run_aggregate

    result = run_aggregate(out)
    console.print(Markdown(result["report"]))


if __name__ == "__main__":
    app()
