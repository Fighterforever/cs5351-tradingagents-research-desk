"""Readable markdown reports for runs, proposals and the ledger.

Reports are the human-facing evidence/provenance view: run manifest + config +
input snapshot + event/usage summary + signal + proposal, the ledger state, and
the proposal review trail. They are pure rendering (no calls).
"""

from __future__ import annotations

from .models import EvidencePack, LedgerState, ProposalRecord


def render_run_report(pack: EvidencePack) -> str:
    m = pack.manifest
    lines = [
        f"# Research Desk Run Report: {m.ticker} on {m.trade_date}",
        "",
        f"- run_id: `{m.run_id}`",
        f"- outcome: `{m.outcome}`",
        f"- signal: `{m.signal or 'n/a'}`",
        f"- context mode: `{m.context_mode}`",
        f"- data mode: `{m.data_mode}`",
        f"- analysts: {', '.join(m.analysts)}",
        f"- prompt version: `{m.prompt_version}`",
        f"- created at: {m.created_at}",
        f"- source pack: {m.source_pack or 'none (original run)'}",
        f"- budget max calls: {m.budget_max_calls}",
        "",
        "## Usage",
        "",
        f"- LLM calls: {pack.usage.calls}",
        f"- input tokens: {pack.usage.input_tokens}",
        f"- output tokens: {pack.usage.output_tokens}",
        f"- total tokens: {pack.usage.total_tokens}",
        f"- stop reason: {pack.usage.stop_reason}",
        "",
        "## Input snapshot",
        "",
        f"- instrument context chars: {len(pack.input.instrument_context)}",
        f"- past context chars: {len(pack.input.past_context)}",
        f"- identity: {pack.input.identity or '{}'}",
        f"- frozen tool data: {sum(len(v) for v in pack.input.data_snapshot.values())} entries",
        f"- memory sources: {', '.join(pack.input.memory_sources) or 'none'}",
        "",
        "## Events",
        "",
    ]
    kinds: dict[str, int] = {}
    for ev in pack.events:
        kinds[ev.kind] = kinds.get(ev.kind, 0) + 1
    lines.append("| kind | count |")
    lines.append("|---|---|")
    for kind, count in sorted(kinds.items()):
        lines.append(f"| {kind} | {count} |")
    if pack.proposal is not None:
        lines.extend(
            [
                "",
                "## Proposal",
                "",
                render_proposal_report(pack.proposal),
            ]
        )
    if pack.reports_written:
        lines.extend(["", "## Reports written", ""])
        lines.extend(f"- `{p}`" for p in pack.reports_written)
    return "\n".join(lines)


def render_proposal_report(prop: ProposalRecord) -> str:
    lines = [
        f"### Proposal `{prop.proposal_id}`",
        "",
        f"- status: `{prop.status.value}`",
        f"- run: `{prop.run_id}`",
        f"- ticker: {prop.ticker} on {prop.trade_date}",
        f"- signal: {prop.signal}",
        f"- side: {prop.side}",
        f"- price (from evidence): {prop.price}",
        f"- evidence id: {prop.evidence_id or 'n/a'}",
        f"- shares (operator): {prop.shares}",
        f"- proposal version: `{prop.proposal_version}`",
        f"- operator: {prop.operator or 'n/a'}",
        f"- approved version: {prop.approved_version or 'n/a'}",
        f"- reason: {prop.reason or 'n/a'}",
    ]
    if prop.execution is not None:
        ex = prop.execution
        lines.extend(
            [
                "",
                "#### Execution",
                "",
                f"- executed: {ex.executed}",
                f"- tx_id: {ex.tx_id or 'n/a'}",
                f"- equity before: {ex.equity_before}",
                f"- equity after: {ex.equity_after}",
                f"- cash delta: {ex.cash_delta}",
                f"- reason: {ex.reason or 'n/a'}",
            ]
        )
        if ex.policy_checks:
            lines.extend(["", "##### Policy checks", ""])
            lines.append("| check | passed | detail |")
            lines.append("|---|---|---|")
            for c in ex.policy_checks:
                lines.append(f"| {c['check']} | {c['passed']} | {c['detail']} |")
    return "\n".join(lines)


def render_ledger_report(ledger: LedgerState, transactions: list[dict], proposals: list[ProposalRecord]) -> str:
    lines = [
        "# Research Desk Ledger",
        "",
        f"- last updated: {ledger.last_updated}",
        f"- cash: **USD {ledger.cash:,.2f}**",
        f"- equity: **USD {ledger.equity:,.2f}**",
        "",
        "## Positions",
        "",
    ]
    if ledger.positions:
        lines.append("| ticker | shares | avg price | value |")
        lines.append("|---|---|---|---|")
        for ticker, pos in sorted(ledger.positions.items()):
            value = pos.shares * (pos.avg_price or 0.0)
            lines.append(f"| {ticker} | {pos.shares} | {pos.avg_price or 'n/a'} | {value:,.2f} |")
    else:
        lines.append("_none_")
    lines.extend(["", "## Proposals", ""])
    if proposals:
        lines.append("| id | ticker | signal | price | shares | status |")
        lines.append("|---|---|---|---|---|---|")
        for p in proposals:
            lines.append(
                f"| {p.proposal_id} | {p.ticker} | {p.signal} | {p.price or 'n/a'} | "
                f"{p.shares or 'n/a'} | {p.status.value} |"
            )
    else:
        lines.append("_none_")
    lines.extend(["", "## Transactions", ""])
    if transactions:
        lines.append("| tx_id | proposal | ticker | shares | price | cash delta | equity | status |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for t in transactions:
            lines.append(
                f"| {t['id']} | {t['proposal_id']} | {t['ticker']} | {t['shares']} | "
                f"{t['price']} | {t['cash_delta']:,.2f} | {t['equity_after']:,.2f} | {t['status']} |"
            )
    else:
        lines.append("_none_")
    return "\n".join(lines)


def render_compare_report(baseline: dict, compact: dict) -> str:
    """Table rendering for a baseline/compact comparison (FR-003)."""
    lines = [
        "# Baseline / Compact Comparison",
        "",
        "Same graph, same frozen evidence; only the context assembly differs.",
        "",
        "| metric | baseline | compact | delta |",
        "|---|---|---|---|",
    ]

    def row(name: str, b, c, fmt="{:.1f}") -> str:
        return f"| {name} | {fmt.format(b)} | {fmt.format(c)} | {_delta(b, c)} |"

    lines.append(row("LLM calls", baseline["calls"], compact["calls"], "{:.0f}"))
    lines.append(row("input tokens", baseline["input_tokens"], compact["input_tokens"]))
    lines.append(row("output tokens", baseline["output_tokens"], compact["output_tokens"]))
    lines.append(row("total tokens", baseline["total_tokens"], compact["total_tokens"]))
    lines.append(row("wall time (s)", baseline["wall_seconds"], compact["wall_seconds"]))
    lines.append(f"| stop reason | {baseline['stop_reason']} | {compact['stop_reason']} | — |")
    lines.append(f"| context chars | {baseline['context_chars']} | {compact['context_chars']} | {_delta(baseline['context_chars'], compact['context_chars'])} |")
    lines.append(f"| signal | {baseline['signal'] or 'n/a'} | {compact['signal'] or 'n/a'} | — |")
    return "\n".join(lines)


def _delta(b: float, c: float) -> str:
    if b == 0:
        return "—"
    pct = (c - b) / b * 100
    return f"{pct:+.1f}%"
