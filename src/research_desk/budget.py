"""LLM call budget and usage accounting for a research run.

The budget counts *started* LLM calls and the actual token usage reported by
the provider. Enforcement happens in the evidence recorder's
``on_chat_model_start``: once the configured call limit is reached, the next
call raises :class:`BudgetExhausted` so the graph aborts and no further LLM
request is started (NFR-003). A budget-stopped run returns incomplete research
and is never turned into an approvable recommendation.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field

from .models import CallUsage, UsageSummary


class BudgetExhausted(Exception):
    """Raised when the configured LLM call budget is exhausted."""

    def __init__(self, limit: int):
        self.limit = limit
        super().__init__(f"LLM call budget exhausted (limit={limit}); refusing to start next call")


@dataclass
class BudgetTracker:
    """Thread-safe per-run call budget + usage accumulator.

    ``stop_reason`` distinguishes an *actually blocked* next call (a request was
    refused with :class:`BudgetExhausted`) from a normal completion that simply
    used at most ``max_calls`` calls. A run that reaches the limit on its final
    allowed call without ever requesting another is ``completed``; only a run
    whose next call was refused is ``budget_exhausted``.
    """

    max_calls: int | None = None
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    calls_started: int = 0
    blocked: bool = False  # a call was actually refused (BudgetExhausted raised)
    usage: UsageSummary = field(default_factory=UsageSummary)

    def can_start(self) -> bool:
        """Whether a new LLM call is permitted under the budget."""
        if self.max_calls is None:
            return True
        return self.calls_started < self.max_calls

    def start_call(self) -> None:
        """Register the start of an LLM call; raise when budget exhausted."""
        with self._lock:
            limit = self.max_calls
            if limit is not None and self.calls_started >= limit:
                self.blocked = True
                raise BudgetExhausted(limit)
            self.calls_started += 1

    def record_usage(self, usage: CallUsage) -> None:
        with self._lock:
            self.usage.add(usage)

    def stop_reason(self) -> str:
        if self.blocked:
            return "budget_exhausted"
        return "completed"

    def summary(self) -> UsageSummary:
        with self._lock:
            return UsageSummary(
                calls=self.calls_started,
                input_tokens=self.usage.input_tokens,
                output_tokens=self.usage.output_tokens,
                total_tokens=self.usage.total_tokens,
                stop_reason=self.stop_reason(),
            )

    def merge(self, other: BudgetTracker) -> None:
        """Merge another tracker's counts (used to aggregate baseline/compact arms)."""
        with self._lock:
            self.calls_started += other.calls_started
            self.blocked = self.blocked or other.blocked
            self.usage.calls += other.usage.calls
            self.usage.input_tokens += other.usage.input_tokens
            self.usage.output_tokens += other.usage.output_tokens
            self.usage.total_tokens += other.usage.total_tokens
