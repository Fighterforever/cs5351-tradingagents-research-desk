"""Context assembly for research runs: baseline vs compact.

The upstream graph already injects a ``past_context`` (memory lessons) and an
``instrument_context`` (resolved identity) into the initial state. This module
owns the *assembly of that context string* so a compact configuration can
genuinely shrink the prompt while preserving the invariants the task requires:

- stock identity, analysis date, key prices,
- standing constraints (the simulated policy numbers), current task,
- de-duplicated repeated text,
- bounded earlier history.

Compaction never removes agents or the graph; it only changes the text that is
assembled into the initial ``past_context``. The honest size metric recorded
offline is the number of characters assembled; actual LLM token usage comes
from provider ``usage_metadata`` during a run.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .models import ContextMode


@dataclass
class StandingConstraints:
    """Identity/date/price/policy facts that must survive compaction."""

    ticker: str = ""
    trade_date: str = ""
    identity: dict[str, str] = field(default_factory=dict)
    prices: dict[str, float] = field(default_factory=dict)  # label -> last price
    policy: dict[str, Any] = field(default_factory=dict)  # teaching policy numbers
    current_task: str = ""

    def header_text(self) -> str:
        lines = ["STANDING ANALYSIS CONSTRAINTS (always true for this run):"]
        lines.append(f"- Instrument identity: {self.ticker}")
        if self.identity.get("company_name"):
            lines.append(f"- Company: {self.identity['company_name']}")
        if self.identity.get("sector"):
            lines.append(f"- Sector/industry: {self.identity['sector']} / {self.identity.get('industry', '')}")
        lines.append(f"- Analysis date: {self.trade_date}")
        for label, price in self.prices.items():
            lines.append(f"- Key price ({label}): {price}")
        for key, value in self.policy.items():
            lines.append(f"- Standing constraint - {key}: {value}")
        if self.current_task:
            lines.append(f"- Current task: {self.current_task}")
        return "\n".join(lines)


def _extract_news_notes(news: str) -> list[str]:
    """Pull the factual earnings notes (``- `` bullets) out of the provider's
    official news output so every role can cite them against their source ID."""
    notes: list[str] = []
    for line in str(news or "").splitlines():
        line = line.strip()
        if line.startswith("- "):
            notes.append(line[2:].strip())
    return notes


def market_source_id(ticker: str) -> str:
    """Stable source ID for the market CSV / technical-computation evidence."""
    return f"market-{ticker.lower()}"


def build_common_grounding(
    ticker: str,
    trade_date: str,
    available_sources: dict[str, Any] | None,
) -> str:
    """The COMMON grounding layer injected into every real LLM request.

    Built only from the actual per-case provider / ``available_sources`` — the
    real ticker, legal company identity, analysis date, frozen close, official
    news notes and their real source IDs. Nothing is fabricated and no source
    is claimed to exist that the evidence does not actually provide:

    - The official earnings source (``src-<ticker>``, the one the judge uses)
      is registered ONLY when an actual ``source_id`` with news notes is present.
    - The market source (``market-<ticker>``) is registered ONLY when market
      CSV / verified evidence actually exists.
    - With no frozen registry (ordinary live analyze path), the rules instruct
      attribution to the actual observed tool results and require unknown facts
      to be reported as unknown — never a hard-coded ``src-<ticker>`` claim.

    Both arms (baseline and compact) receive the identical text so every role
    can cite facts accurately.
    """
    src = available_sources or {}
    identity = src.get("identity") or {}
    source_id = src.get("source_id") or ""
    notes = _extract_news_notes(str(src.get("news") or ""))
    has_earnings = bool(source_id) and bool(notes)

    market = str(src.get("market", "") or "")
    verified = str(src.get("verified_snapshot", "") or "")
    has_market = bool(market.strip() or verified.strip())

    eff_ticker = (ticker or "").upper()
    if not eff_ticker and source_id:
        eff_ticker = source_id.removeprefix("src-").upper()
    market_id = market_source_id(eff_ticker) if eff_ticker else ""
    analysis_date = src.get("analysis_date") or trade_date or ""
    announcement_date = src.get("announcement_date") or ""
    as_of = src.get("as_of") or ""
    latest_close = src.get("latest_close")

    company = identity.get("company_name") or ""
    sector = identity.get("sector") or ""
    industry = identity.get("industry") or ""

    lines = ["COMMON GROUNDING LAYER (the factual basis for this analysis; every role receives this)"]
    if eff_ticker:
        lines.append(f"- Ticker: {eff_ticker}")
    if company:
        qualifier = f" ({sector} / {industry})" if sector else ""
        lines.append(f"- Company (legal identity): {company}{qualifier}")
    if analysis_date:
        suffix = f" (announcement date {announcement_date})" if announcement_date else ""
        lines.append(f"- Analysis date: {analysis_date}{suffix}")
    if latest_close is not None and market_id:
        if as_of:
            lines.append(
                f"- Frozen latest close: {latest_close} USD [source: {market_id}, market CSV as-of {as_of}]"
            )
        else:
            lines.append(f"- Frozen latest close: {latest_close} USD [source: {market_id}]")

    if has_earnings or has_market:
        lines.append("")
        lines.append("SOURCE-ID REGISTRY (cite the matching ID inline for every factual claim):")
        if has_earnings:
            lines.append(f"- {source_id} = official earnings news (the only earnings source)")
        if has_market and market_id:
            lines.append(
                f"- {market_id} = market price/volume and technical indicator computations "
                "from the frozen market CSV"
            )
    if notes:
        lines.append("")
        lines.append(f"OFFICIAL EARNINGS NOTES [{source_id or 'news source'}]:")
        for note in notes:
            lines.append(f"  - {note}")

    lines.append("")
    lines.append("CITATION & GROUNDING RULES (apply to every claim you make):")
    if has_earnings or has_market:
        lines.append(
            "1. Cite the source ID inline for every factual claim using the format: "
            "<supported claim> [<actual source ID>]."
        )
    else:
        lines.append(
            "1. Cite the actual tool result that supports each factual claim (e.g. the "
            "get_stock_data / get_indicators / get_verified_market_snapshot output you "
            "observed during this analysis)."
        )
    lines.append(
        "2. A derived number (growth %, ratio, multiple) is a CALCULATION: show its actual "
        "operands and cite each operand's source, without presenting the result as a "
        "sourced fact."
    )
    lines.append(
        "3. Any valuation ratio, multiple, target, or estimate NOT present in the observed "
        "sources is UNKNOWN. Never state it as a fact."
    )
    lines.append(
        "4. Price targets, entry prices, stop-loss levels and position sizes are "
        "ASSUMPTIONS or analyst judgments - label them as such, never as sourced facts."
    )
    lines.append(
        "5. State which research role you are (market analyst, bull/bear researcher, "
        "research manager, trader, risk analyst, or portfolio manager)."
    )
    lines.append(
        "6. Only the final Portfolio Manager may label its output FINAL TRANSACTION "
        "PROPOSAL; all earlier output is nonbinding role analysis."
    )
    lines.append(
        "7. Use only facts present in the sources (the grounding above OR the actual tool "
        "results observed during this analysis) and known by the analysis date."
    )
    lines.append(
        "8. In the final research/recommendation rationale, when the ticker, analysis date "
        "and frozen latest close are present, restate them with market attribution "
        "(e.g. ticker <T>, analysis date <D>, latest close <P> [market-<T>])."
    )
    return "\n".join(lines)


def dedup_repeated_blocks(text: str) -> str:
    """Remove exact duplicate paragraph blocks, keeping first occurrence order.

    Operates on blank-line-separated blocks so repeated analyst reports in a
    long history collapse to one copy instead of being sent N times.
    """
    if not text:
        return text
    blocks = list(text.split("\n\n"))
    seen: set[str] = set()
    kept: list[str] = []
    for block in blocks:
        key = block.strip()
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        kept.append(block)
    return "\n\n".join(kept)


def bound_history(text: str, max_chars: int = 6000) -> str:
    """Bound total assembled history length by truncating from the tail."""
    if not text:
        return text
    if len(text) <= max_chars:
        return text
    # Cut at a block boundary near the limit so we never split mid-paragraph.
    cut = text.rfind("\n\n", 0, max_chars)
    if cut == -1:
        cut = max_chars
    return text[:cut].rstrip() + "\n\n[... earlier history truncated ...]"


def estimate_token_heuristic(text: str) -> int:
    """Deterministic English-token heuristic for offline comparisons.

    This is a *character-based heuristic*, explicitly NOT claimed as provider
    token counts; real token numbers come from LLM usage metadata. It exists so
    offline tests can assert that compact genuinely assembles less context.
    """
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


@dataclass
class AssemblyResult:
    text: str
    mode: str
    chars: int
    blocks: int
    token_heuristic: int
    deduplicated: int = 0
    truncated: bool = False


class ContextAssembler:
    """Assembles the injected ``past_context`` for baseline or compact runs.

    Baseline preserves the *original* input verbatim: the raw memory text is
    injected unchanged (plus the standing constraints), with only a hard safety
    ceiling that never normally fires. Compact genuinely differs: it de-
    duplicates repeated blocks, bounds earlier history at a tighter cap, and
    re-appends the constraints. The same assembler, same source material, and
    same graph are used for both arms — only the assembly differs.
    """

    # Baseline keeps history whole (hard ceiling is only a safety net that does
    # not normally fire); compact applies a tighter cap so older discussion is
    # genuinely compressed.
    DEFAULT_HARD_MAX_CHARS = 20000
    DEFAULT_COMPACT_MAX_CHARS = 6000
    DEFAULT_MAX_ENTRIES = 5

    def __init__(self, constraints: StandingConstraints | None = None, **kwargs):
        self.constraints = constraints or StandingConstraints()
        self.hard_max_chars = kwargs.get("hard_max_chars", self.DEFAULT_HARD_MAX_CHARS)
        self.compact_max_chars = kwargs.get(
            "compact_max_chars", self.DEFAULT_COMPACT_MAX_CHARS
        )
        self.max_entries = kwargs.get("max_entries", self.DEFAULT_MAX_ENTRIES)

    def assemble(self, memory_text: str, mode: str | ContextMode) -> AssemblyResult:
        mode = ContextMode(mode)
        constraints = self.constraints.header_text()
        if mode == ContextMode.BASELINE:
            # Preserve the original input verbatim; do not de-duplicate or
            # rewrite it. The hard ceiling is a pure safety net.
            body = memory_text or ""
            truncated = len(body) > self.hard_max_chars
            body = bound_history(body, self.hard_max_chars)
            deduped = 0
        else:
            body = dedup_repeated_blocks(memory_text)
            deduped = (
                len([b for b in memory_text.split("\n\n") if b.strip()])
                - len([b for b in body.split("\n\n") if b.strip()])
                if memory_text
                else 0
            )
            truncated = len(body) > self.compact_max_chars
            body = bound_history(body, self.compact_max_chars)
        text = _join_parts(constraints, body)
        return AssemblyResult(
            text=text,
            mode=mode.value,
            chars=len(text),
            blocks=len([b for b in text.split("\n\n") if b.strip()]),
            token_heuristic=estimate_token_heuristic(text),
            deduplicated=deduped,
            truncated=truncated,
        )

    def assemble_from_entries(
        self,
        entries: list[dict[str, Any]],
        mode: str | ContextMode,
        as_of: str | None = None,
    ) -> AssemblyResult:
        """Assemble from structured memory entries (TradingMemoryLog shape).

        When ``as_of`` (yyyy-mm-dd) is given, entries whose outcome was only
        resolved after that date are excluded, so a historical run cannot learn
        from the future (SEC-001/AT-02). Entries with no recorded resolution
        date are kept but explicitly marked as not suitable for historical
        evaluation.
        """
        if not entries:
            return self.assemble("", mode)
        parts = []
        seen_bodies: set[str] = set()
        deduplicated = 0
        for e in entries:
            resolved = e.get("resolved")
            if as_of is not None and resolved and resolved > as_of:
                continue  # outcome not known by the trade date — exclude
            decision = (e.get("decision") or "").strip()
            reflection = (e.get("reflection") or "").strip()
            # De-duplicate repeated report *bodies* regardless of the differing
            # tag date, keeping the first occurrence for traceability.
            body = f"{decision}\n{reflection}".strip()
            if body:
                if body in seen_bodies:
                    deduplicated += 1
                    continue
                seen_bodies.add(body)
            tag = (
                f"[{e.get('date', '')} | {e.get('ticker', '')} | "
                f"{e.get('rating', '')}]"
            )
            if as_of is not None and not resolved:
                tag += " [availability: unknown — not suitable for historical evaluation]"
            block = tag
            if decision:
                block += f"\nDECISION:\n{decision}"
            if reflection:
                block += f"\nREFLECTION:\n{reflection}"
            parts.append(block)
        recent = parts[-self.max_entries :]
        result = self.assemble("\n\n".join(recent), mode)
        result.deduplicated += deduplicated
        return result


def _join_parts(constraints: str, body: str) -> str:
    if not body:
        return constraints
    return constraints + "\n\n" + body
