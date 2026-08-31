"""SQLite persistence for the simulated ledger and proposals, plus JSON pack IO.

The simulated ledger is deliberately separate from upstream TradingAgents'
research memory: research memory records decisions for reflection, while this
ledger records executable, operator-approved transactions. Both live in the
desk home, and neither stores credentials.

SQLite is used with ``PRAGMA journal_mode=WAL`` and a single writer so the
approve/execute re-read is atomic; every ledger change is written inside a
transaction and references the approved proposal version and the deterministic
policy checks that passed (INV-001).
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .config import INITIAL_CASH
from .models import (
    ExecutionRecord,
    LedgerPosition,
    LedgerState,
    ProposalRecord,
    ProposalStatus,
    TransactionRecord,
    utcnow_iso,
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS ledger_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    cash REAL NOT NULL,
    last_updated TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS positions (
    ticker TEXT PRIMARY KEY,
    shares INTEGER NOT NULL,
    avg_price REAL
);

CREATE TABLE IF NOT EXISTS proposals (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    ticker TEXT NOT NULL,
    trade_date TEXT NOT NULL,
    signal TEXT NOT NULL,
    rating TEXT,
    side TEXT NOT NULL DEFAULT 'buy',
    price REAL,
    shares INTEGER,
    evidence_id TEXT,
    status TEXT NOT NULL,
    proposal_version TEXT NOT NULL,
    operator TEXT,
    created_at TEXT NOT NULL,
    approved_at TEXT,
    approved_version TEXT,
    reason TEXT,
    execution_json TEXT
);

CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    proposal_id TEXT NOT NULL,
    ticker TEXT NOT NULL,
    side TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price REAL NOT NULL,
    cash_delta REAL NOT NULL,
    equity_before REAL NOT NULL,
    equity_after REAL NOT NULL,
    status TEXT NOT NULL,
    policy_json TEXT NOT NULL,
    operator TEXT,
    created_at TEXT NOT NULL
);
"""


class ResearchDeskStore:
    """Thin SQLite wrapper for ledger + proposals.

    Not an ORM: methods are few and map directly to the review/ledger commands
    so the deterministic policy logic stays readable and testable.
    """

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()
        self._migrate()
        # Seed the single ledger row on first use.
        if self.get_ledger() is None:
            self._conn.execute(
                "INSERT INTO ledger_state (id, cash, last_updated) VALUES (1, ?, ?)",
                (INITIAL_CASH, utcnow_iso()),
            )
            self._conn.commit()

    # ------------------------------------------------------------------
    # Ledger
    # ------------------------------------------------------------------

    def _migrate(self) -> None:
        """Add columns introduced after the initial schema on pre-existing DBs."""
        cols = {r["name"] for r in self._conn.execute("PRAGMA table_info(proposals)").fetchall()}
        if "side" not in cols:
            self._conn.execute("ALTER TABLE proposals ADD COLUMN side TEXT NOT NULL DEFAULT 'buy'")
        if "evidence_id" not in cols:
            self._conn.execute("ALTER TABLE proposals ADD COLUMN evidence_id TEXT")
        self._conn.commit()

    def get_ledger(self) -> LedgerState | None:
        row = self._conn.execute("SELECT cash, last_updated FROM ledger_state WHERE id=1").fetchone()
        if row is None:
            return None
        positions: dict[str, LedgerPosition] = {}
        for p in self._conn.execute("SELECT ticker, shares, avg_price FROM positions").fetchall():
            positions[p["ticker"]] = LedgerPosition(
                ticker=p["ticker"], shares=p["shares"], avg_price=p["avg_price"]
            )
        return LedgerState(cash=row["cash"], positions=positions, last_updated=row["last_updated"])

    def apply_transaction(self, tx: TransactionRecord, execution: ExecutionRecord) -> None:
        """Atomically apply a simulated buy transaction and record it.

        Re-reads the current ledger inside the write transaction so a concurrent
        approve/execute cannot double-apply a stale balance. The caller (review
        policy) has already re-evaluated the ledger; this is the commit step.
        """
        with self._conn:
            row = self._conn.execute(
                "SELECT cash FROM ledger_state WHERE id=1"
            ).fetchone()
            new_cash = row["cash"] + tx.cash_delta
            self._conn.execute(
                "UPDATE ledger_state SET cash=?, last_updated=? WHERE id=1",
                (new_cash, utcnow_iso()),
            )
            pos = self._conn.execute(
                "SELECT shares, avg_price FROM positions WHERE ticker=?", (tx.ticker,)
            ).fetchone()
            if tx.side == "sell":
                if pos is None:
                    raise ValueError(
                        f"cannot sell {tx.ticker}: no position held in the ledger"
                    )
                new_shares = pos["shares"] - tx.shares
                if new_shares < 0:
                    raise ValueError(
                        f"cannot sell {tx.shares} of {pos['shares']} owned {tx.ticker} (no shorting)"
                    )
                # Average price is unchanged by a sale; shares only decrease.
                self._conn.execute(
                    "UPDATE positions SET shares=?, avg_price=? WHERE ticker=?",
                    (new_shares, pos["avg_price"], tx.ticker),
                )
            elif pos is None:
                self._conn.execute(
                    "INSERT INTO positions (ticker, shares, avg_price) VALUES (?, ?, ?)",
                    (tx.ticker, tx.shares, tx.price),
                )
            else:
                new_shares = pos["shares"] + tx.shares
                total_cost = (pos["shares"] * (pos["avg_price"] or 0.0)) + (tx.shares * tx.price)
                new_avg = total_cost / new_shares if new_shares else 0.0
                self._conn.execute(
                    "UPDATE positions SET shares=?, avg_price=? WHERE ticker=?",
                    (new_shares, new_avg, tx.ticker),
                )
            self._conn.execute(
                """INSERT INTO transactions
                   (id, proposal_id, ticker, side, shares, price, cash_delta,
                    equity_before, equity_after, status, policy_json, operator, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    tx.tx_id, tx.proposal_id, tx.ticker, tx.side, tx.shares, tx.price,
                    tx.cash_delta, tx.equity_before, tx.equity_after, tx.status.value,
                    json.dumps(tx.policy_checks), tx.operator, tx.created_at,
                ),
            )
            self._conn.execute(
                "UPDATE proposals SET status=?, execution_json=? WHERE id=?",
                (
                    ProposalStatus.SIMULATED.value,
                    json.dumps(execution.model_dump()),
                    tx.proposal_id,
                ),
            )

    def list_transactions(self) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            "SELECT * FROM transactions ORDER BY created_at"
        ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Proposals
    # ------------------------------------------------------------------

    def save_proposal(self, proposal: ProposalRecord) -> None:
        # Carry over a prior approval binding when content is re-saved: an
        # approved proposal whose run inputs later change keeps its approved
        # version so execution detects the stale approval (AT-05). Fresh
        # (PENDING_REVIEW) proposals keep None.
        prior = self._conn.execute(
            "SELECT approved_at, approved_version, operator FROM proposals WHERE id=?",
            (proposal.proposal_id,),
        ).fetchone()
        carry_approved_at = proposal.approved_at
        carry_approved_version = proposal.approved_version
        carry_operator = proposal.operator
        if prior is not None and (prior["approved_version"] is not None):
            carry_approved_at = proposal.approved_at or prior["approved_at"]
            carry_approved_version = proposal.approved_version or prior["approved_version"]
            carry_operator = proposal.operator or prior["operator"]
        with self._conn:
            self._conn.execute(
                """INSERT OR REPLACE INTO proposals
                   (id, run_id, ticker, trade_date, signal, rating, side, price,
                    shares, evidence_id, status, proposal_version, operator,
                    created_at, approved_at, approved_version, reason, execution_json)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    proposal.proposal_id, proposal.run_id, proposal.ticker,
                    proposal.trade_date, proposal.signal, proposal.rating,
                    proposal.side, proposal.price, proposal.shares,
                    proposal.evidence_id, proposal.status.value,
                    proposal.proposal_version, carry_operator,
                    proposal.created_at, carry_approved_at,
                    carry_approved_version, proposal.reason,
                    json.dumps(proposal.execution.model_dump()) if proposal.execution else None,
                ),
            )

    def get_proposal(self, proposal_id: str) -> ProposalRecord | None:
        row = self._conn.execute(
            "SELECT * FROM proposals WHERE id=?", (proposal_id,)
        ).fetchone()
        if row is None:
            return None
        return self._row_to_proposal(row)

    def list_proposals(self, status: str | None = None) -> list[ProposalRecord]:
        if status:
            rows = self._conn.execute(
                "SELECT * FROM proposals WHERE status=? ORDER BY created_at", (status,)
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM proposals ORDER BY created_at"
            ).fetchall()
        return [self._row_to_proposal(r) for r in rows]

    def update_proposal_status(
        self,
        proposal_id: str,
        status: ProposalStatus,
        operator: str | None = None,
        approved_version: str | None = None,
        reason: str | None = None,
    ) -> None:
        with self._conn:
            now = utcnow_iso()
            if status == ProposalStatus.APPROVED:
                self._conn.execute(
                    """UPDATE proposals SET status=?, operator=?, approved_at=?,
                       approved_version=?, reason=? WHERE id=?""",
                    (status.value, operator, now, approved_version, reason, proposal_id),
                )
            else:
                self._conn.execute(
                    """UPDATE proposals SET status=?, operator=?, reason=? WHERE id=?""",
                    (status.value, operator, reason, proposal_id),
                )

    def _row_to_proposal(self, row: sqlite3.Row) -> ProposalRecord:
        execution = None
        if row["execution_json"]:
            execution = ExecutionRecord(**json.loads(row["execution_json"]))
        return ProposalRecord(
            proposal_id=row["id"],
            run_id=row["run_id"],
            ticker=row["ticker"],
            trade_date=row["trade_date"],
            signal=row["signal"],
            rating=row["rating"],
            side=row["side"],
            price=row["price"],
            shares=row["shares"],
            evidence_id=row["evidence_id"],
            status=ProposalStatus(row["status"]),
            proposal_version=row["proposal_version"],
            operator=row["operator"],
            created_at=row["created_at"],
            approved_at=row["approved_at"],
            approved_version=row["approved_version"],
            reason=row["reason"],
            execution=execution,
        )

    def close(self) -> None:
        self._conn.close()


def _json_default(o):
    if hasattr(o, "model_dump"):
        return o.model_dump()
    if hasattr(o, "isoformat"):
        return o.isoformat()
    return str(o)


def write_json(path: str | Path, data: Any) -> None:
    Path(path).write_text(json.dumps(data, indent=2, default=_json_default), encoding="utf-8")


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
