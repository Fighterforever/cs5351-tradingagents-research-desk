"""Research Desk settings and paths.

The desk keeps its own home (separate from upstream TradingAgents' cache and
results) for the SQLite ledger, run evidence packs and run records. Everything
is overridable through ``RESEARCH_DESK_HOME`` so tests can point at a temp dir
without touching the user's data.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_HOME = os.path.join(os.path.expanduser("~"), ".research_desk")

# Simulated teaching policy (deterministic, decided by leo, enforced by code).
INITIAL_CASH = 100000.0
MAX_POSITION_PCT = 0.10  # single stock market value <= 10% of equity after buy
INTEGER_SHARES_ONLY = True
NO_SHORTING = True


@dataclass
class ResearchDeskSettings:
    home: str = field(default_factory=lambda: os.environ.get("RESEARCH_DESK_HOME", DEFAULT_HOME))
    prompt_version: str = "research-desk-0.1.1"
    analysts: tuple[str, ...] = ("market", "news")
    max_calls: int | None = None  # None = no LLM call budget
    policy_version: str = "teaching-v1"

    def __post_init__(self) -> None:
        self.home = os.path.expanduser(self.home)

    @property
    def home_path(self) -> Path:
        return Path(self.home)

    @property
    def db_path(self) -> Path:
        return self.home_path / "research_desk.db"

    @property
    def runs_dir(self) -> Path:
        return self.home_path / "runs"

    @property
    def reports_dir(self) -> Path:
        return self.home_path / "reports"

    def ensure_dirs(self) -> None:
        self.home_path.mkdir(parents=True, exist_ok=True)
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def config_snapshot(self) -> dict:
        """Sanitised, credential-free config recorded in evidence manifests."""
        return {
            "home": self.home,
            "prompt_version": self.prompt_version,
            "analysts": list(self.analysts),
            "max_calls": self.max_calls,
            "policy_version": self.policy_version,
            "initial_cash": INITIAL_CASH,
            "max_position_pct": MAX_POSITION_PCT,
            "integer_shares_only": INTEGER_SHARES_ONLY,
            "no_shorting": NO_SHORTING,
        }
