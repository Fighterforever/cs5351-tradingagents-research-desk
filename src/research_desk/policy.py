"""Deterministic teaching-policy engine for the simulated ledger.

The deterministic policy constants are defined in ``research_desk.config``;
policy is never decided by an LLM. Every check returns a plain list of
human-readable results; the review layer turns a non-empty list of failures into
a business rejection and leaves the ledger untouched (INV-002). Boundary
behaviour is explicit: a position value exactly equal to 10% of equity is
allowed (<=), one share more is rejected.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import INITIAL_CASH, MAX_POSITION_PCT, NO_SHORTING
from .models import LedgerState


@dataclass
class PolicyVerdict:
    allowed: bool
    checks: list[dict]  # each: {"check": str, "passed": bool, "detail": str}
    equity: float | None = None
    position_value: float | None = None
    cash_after: float | None = None
    shares_after: int | None = None


def _owned_shares(ledger: LedgerState, ticker: str) -> int:
    pos = ledger.positions.get(ticker.upper())
    return pos.shares if pos is not None else 0


def _revalue_equity(ledger: LedgerState, ticker: str, mark_price: float) -> float:
    """Equity with the target ticker's holdings re-marked at the evidence price.

    The position cap is expressed as a fraction of equity, so the equity base
    must mark the ticker under review at the same (frozen evidence) price used
    for the trade. Other positions keep their recorded average mark, which is
    made explicit in the check detail rather than silently revalued.
    """
    ticker = ticker.upper()
    total = ledger.cash
    for t, pos in ledger.positions.items():
        if t == ticker and mark_price is not None and mark_price > 0:
            total += pos.shares * mark_price
        else:
            total += pos.shares * (pos.avg_price or 0.0)
    return total


class PolicyViolation(Exception):
    def __init__(self, reasons: list[str]):
        self.reasons = reasons
        super().__init__("; ".join(reasons))


def evaluate_buy(
    ledger: LedgerState,
    ticker: str,
    shares: int,
    price: float,
    *,
    initial_cash: float = INITIAL_CASH,
    max_position_pct: float = MAX_POSITION_PCT,
) -> PolicyVerdict:
    """Evaluate a buy proposal against the current ledger.

    Rules (v1 teaching policy):
    1. shares must be a positive integer.
    2. price must be positive and present (it always comes from evidence).
    3. cost (shares * price) must not exceed available cash.
    4. after the buy, the *total* position in this ticker (existing holdings at
       the evidence price plus the new shares) must be <= 10% of equity.
    5. no shorting (buys only increase a long position; never negative).

    ``initial_cash`` is recorded for the ledger seed; the effective cash check
    uses the current ledger's cash, which is ``initial_cash`` plus the sum of
    prior cash deltas. The position cap is against *total holdings after the
    purchase*, re-marking this ticker's existing shares at ``price``.
    """
    ticker = ticker.upper()
    checks: list[dict] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "passed": passed, "detail": detail})

    if not isinstance(shares, int) or shares <= 0:
        check("integer_positive_shares", False, f"shares must be a positive integer, got {shares!r}")
        return PolicyVerdict(False, checks)

    if price is None or not isinstance(price, (int, float)) or price <= 0:
        check("price_from_evidence", False, f"price must be a positive number from evidence, got {price!r}")
        return PolicyVerdict(False, checks)

    equity = _revalue_equity(ledger, ticker, price)
    owned = _owned_shares(ledger, ticker)
    shares_after = owned + shares
    position_value = shares_after * price
    cash_after = ledger.cash - shares * price

    check("cash_sufficient", cash_after >= -1e-9, f"cost={shares * price:.2f}, cash={ledger.cash:.2f}")

    cap_value = max_position_pct * equity
    check(
        "position_cap_10pct",
        position_value <= cap_value + 1e-9,
        f"total holdings after buy ({owned} existing + {shares} new = {shares_after} sh "
        f"@ {price:.2f} = {position_value:.2f}) <= {max_position_pct:.0%} * equity={cap_value:.2f}",
    )

    check("no_shorting", NO_SHORTING, "v1 policy is buy-only; sell proposals use evaluate_sell")

    return PolicyVerdict(
        allowed=all(c["passed"] for c in checks),
        checks=checks,
        equity=equity,
        position_value=position_value,
        cash_after=cash_after,
        shares_after=shares_after,
    )


def evaluate_sell(
    ledger: LedgerState,
    ticker: str,
    shares: int,
    price: float,
    *,
    max_position_pct: float = MAX_POSITION_PCT,
) -> PolicyVerdict:
    """Evaluate a sell proposal against the current ledger.

    Sells are allowed only up to the shares actually owned (no shorting means
    a position can never go negative). The 10% concentration cap applies after a
    BUY; a valid SELL that reduces an owned position is permitted even if price
    appreciation means the remaining holding still exceeds 10% of equity.
    ``price`` comes from evidence; cash increases by ``shares * price``.
    """
    ticker = ticker.upper()
    checks: list[dict] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "passed": passed, "detail": detail})

    if not isinstance(shares, int) or shares <= 0:
        check("integer_positive_shares", False, f"shares must be a positive integer, got {shares!r}")
        return PolicyVerdict(False, checks)

    if price is None or not isinstance(price, (int, float)) or price <= 0:
        check("price_from_evidence", False, f"price must be a positive number from evidence, got {price!r}")
        return PolicyVerdict(False, checks)

    owned = _owned_shares(ledger, ticker)
    equity = _revalue_equity(ledger, ticker, price)
    shares_after = owned - shares
    position_value = shares_after * price
    cash_after = ledger.cash + shares * price

    check(
        "sell_not_exceeding_owned",
        shares_after >= 0,
        f"cannot sell {shares} sh when {owned} sh are owned (no shorting); "
        f"sell at most {owned} sh",
    )

    return PolicyVerdict(
        allowed=all(c["passed"] for c in checks),
        checks=checks,
        equity=equity,
        position_value=position_value,
        cash_after=cash_after,
        shares_after=shares_after,
    )


def raise_for_violations(verdict: PolicyVerdict) -> None:
    """Raise a PolicyViolation listing every failed check (no partial writes)."""
    if not verdict.allowed:
        reasons = [f"{c['check']}: {c['detail']}" for c in verdict.checks if not c["passed"]]
        raise PolicyViolation(reasons)


def reject_reasons(verdict: PolicyVerdict) -> list[str]:
    return [f"{c['check']}: {c['detail']}" for c in verdict.checks if not c["passed"]]


def policy_bounds(
    ledger: LedgerState,
    ticker: str,
    price: float | None,
    *,
    max_position_pct: float = MAX_POSITION_PCT,
) -> dict:
    """Deterministic policy limits for a proposal price against a ledger.

    Reported by offline replay so the *policy output* (the largest integer
    share count the teaching policy would allow) is reproduced without needing
    the operator's eventual share choice. ``max_by_cap`` is the additional
    shares a *buy* may add given existing holdings must stay within the total
    position cap.
    """
    if price is None or price <= 0:
        return {
            "price_present": False,
            "max_by_cap": None,
            "max_by_cash": None,
            "owned": _owned_shares(ledger, ticker),
            "equity": ledger.equity,
            "cash": ledger.cash,
        }
    cap_value = max_position_pct * _revalue_equity(ledger, ticker, price)
    owned = _owned_shares(ledger, ticker)
    max_total = int(cap_value // price)
    return {
        "price_present": True,
        "max_by_cap": max_total - owned,  # additional shares still within total cap
        "max_by_cash": int(ledger.cash // price),
        "owned": owned,
        "equity": _revalue_equity(ledger, ticker, price),
        "cash": ledger.cash,
    }
