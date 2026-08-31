"""CS5351 TradingAgents Research Desk.

Offline slice: research evidence packs + offline replay, an operator-approved
simulated ledger, and baseline/compact context assembly with an LLM call budget.
The live research run uses the real :class:`tradingagents.graph.trading_graph.TradingAgentsGraph`;
replay is the deterministic offline reproduction path (zero external calls).
"""

__version__ = "0.1.0"

from .budget import BudgetExhausted, BudgetTracker
from .context import ContextAssembler, StandingConstraints
from .evidence import EvidencePackIO, EvidenceRecorder
from .graph_adapter import ResearchRunner, price_from_evidence
from .models import EvidencePack, ProposalRecord, RunResult
from .policy import PolicyVerdict, evaluate_buy, evaluate_sell
from .replay import ReplayEngine
from .review import approve, create_proposal, execute, reject
from .storage import ResearchDeskStore

__all__ = [
    "BudgetExhausted",
    "BudgetTracker",
    "ContextAssembler",
    "StandingConstraints",
    "EvidencePackIO",
    "EvidenceRecorder",
    "ResearchRunner",
    "price_from_evidence",
    "EvidencePack",
    "ProposalRecord",
    "RunResult",
    "PolicyVerdict",
    "evaluate_buy",
    "evaluate_sell",
    "ReplayEngine",
    "approve",
    "create_proposal",
    "execute",
    "reject",
    "ResearchDeskStore",
]
