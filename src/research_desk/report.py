"""Readable markdown reports for runs, proposals and the ledger.

Reports are the human-facing evidence/provenance view: run manifest + config +
input snapshot + event/usage summary + signal + proposal, the ledger state, and
the proposal review trail. They are pure rendering (no calls).
"""

from __future__ import annotations

from pathlib import Path

from .models import EvidencePack, LedgerState, ProposalRecord

RESEARCH_IDENTITY_TITLE = "# Research Desk Analysis Report"


def _identity_value(identity: dict, key: str) -> str:
    value = identity.get(key)
    return value.strip() if isinstance(value, str) else ""


def render_research_identity(pack: EvidencePack) -> str:
    """Render the deterministic identity/date/evidence-price report contract.

    Every value comes from the actual ``EvidencePack``: the legal company name
    from ``input.identity`` or the actual ``available_sources.identity``, the
    ticker/date from the manifest, the close from ``price_from_evidence`` over
    the pack's own snapshot/corpus, and source IDs from the actual registry.
    Missing facts are rendered as explicitly unavailable; no case registry is
    imported and no identity or price is invented.
    """
    manifest = pack.manifest
    identity = dict(pack.input.identity or {})
    sources = dict(pack.input.available_sources or {})
    source_identity = dict(sources.get("identity") or {})
    merged_identity = {
        **source_identity,
        **{key: value for key, value in identity.items() if value},
    }
    company = _identity_value(merged_identity, "company_name")
    ticker = (manifest.ticker or "").upper()
    trade_date = manifest.trade_date or ""

    from .graph_adapter import price_from_evidence

    price: float | None = price_from_evidence(
        pack.input.data_snapshot or {},
        ticker,
        available_sources=sources,
    )
    if price is None:
        candidate = sources.get("latest_close")
        if isinstance(candidate, (int, float)):
            price = float(candidate)

    source_id = _identity_value(sources, "source_id")
    market_id = _identity_value(sources, "market_source_id")
    as_of = _identity_value(sources, "as_of")

    # Only claim the canonical market-<ticker> ID when the pack actually carries
    # market/verified corpus. Otherwise name the actual recorded tool/evidence.
    attribution = market_id
    if not attribution:
        has_market_corpus = bool(
            str(sources.get("market", "")).strip()
            or str(sources.get("verified_snapshot", "")).strip()
        )
        if has_market_corpus and ticker:
            attribution = f"market-{ticker.lower()}"
        else:
            tool_names = [
                name
                for name, results in (pack.input.data_snapshot or {}).items()
                if name in ("get_stock_data", "get_verified_market_snapshot")
                and any(str(value).strip() for value in results.values())
            ]
            if tool_names:
                attribution = f"observed {'/'.join(sorted(tool_names))} tool result"
            elif price is not None:
                attribution = "pack case metadata"

    lines = [RESEARCH_IDENTITY_TITLE, ""]
    lines.append(f"- Company (legal identity): {company or 'unavailable'}")
    lines.append(f"- Ticker: {ticker or 'unavailable'}")
    lines.append(f"- Analysis date: {trade_date or 'unavailable'}")
    if price is not None:
        if attribution and as_of:
            lines.append(
                f"- Evidence latest close: {price:.2f} USD "
                f"[source: {attribution}, market CSV as-of {as_of}]"
            )
        elif attribution:
            lines.append(f"- Evidence latest close: {price:.2f} USD [source: {attribution}]")
        else:
            lines.append(f"- Evidence latest close: {price:.2f} USD [source: unavailable]")
    else:
        lines.append("- Evidence latest close: unavailable (no price evidence in this pack)")
    lines.append(f"- Official earnings source: {source_id or 'unavailable'}")
    lines.append(
        "- Contract: identity, date, evidence close and source above are rendered "
        "deterministically from the evidence pack; the generated narrative below is "
        "unmodified model output."
    )
    return "\n".join(lines)


def _strip_existing_header(text: str) -> str:
    """Drop a previous deterministic or upstream report header, keep the body."""
    marker = "\n## "
    idx = text.find(marker)
    if idx != -1:
        return text[idx + 1 :]
    lines = text.splitlines()
    start = 0
    while start < len(lines):
        line = lines[start]
        if not line.strip() or line.startswith("# ") or line.startswith("Generated:"):
            start += 1
            continue
        break
    return "\n".join(lines[start:])


def apply_research_identity_header(complete_report_path: str | Path, header: str) -> Path:
    """Write ``header`` ahead of the generated report body, never duplicating it."""
    path = Path(complete_report_path)
    body = _strip_existing_header(path.read_text(encoding="utf-8"))
    path.write_text(
        header + ("\n\n" + body if body.strip() else "") + "\n",
        encoding="utf-8",
    )
    return path


def render_run_report(pack: EvidencePack) -> str:
    m = pack.manifest
    lines = [
        render_research_identity(pack),
        "",
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
