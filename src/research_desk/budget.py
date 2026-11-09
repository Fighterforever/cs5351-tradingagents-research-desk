"""LLM call budget and usage accounting for a research run.

The budget counts *started* LLM calls and the actual token usage reported by
the provider. Enforcement happens in the evidence recorder's
``on_chat_model_start``: once the configured call limit is reached, the next
call raises :class:`BudgetExhausted` so the graph aborts and no further LLM
request is started (NFR-003). A budget-stopped run returns incomplete research
and is never turned into an approvable recommendation.

This module also owns the whole-input context bound (ADR-004): a conservative
UTF-8 byte-based token upper bound estimates the complete request; when the
mandatory material still exceeds the cap the caller raises
:class:`ContextBudgetExceeded` before the provider is invoked.
"""

from __future__ import annotations

import json
import threading
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from langchain_core.messages import BaseMessage

from .models import CallUsage, UsageSummary

# Conservative fixed per-message/per-tool-call overhead added to the UTF-8 byte
# count. This keeps the estimate an *upper bound* on provider tokens; it is not
# measured token usage (provider usage remains the measured-cost source).
CONTEXT_MESSAGE_OVERHEAD = 8
CONTEXT_TOOL_CALL_OVERHEAD = 16


class BudgetExhausted(Exception):
    """Raised when the configured LLM call budget is exhausted."""

    def __init__(self, limit: int):
        self.limit = limit
        super().__init__(f"LLM call budget exhausted (limit={limit}); refusing to start next call")


class ContextBudgetExceeded(Exception):
    """Raised when the complete model input cannot fit under the context cap.

    Raised at the request boundary *before* the provider is invoked, so the run
    stops with an incomplete, non-approvable outcome while evidence remains
    inspectable.
    """

    stop_reason = "context_budget_exhausted"

    def __init__(self, estimated_tokens: int, limit: int):
        self.estimated_tokens = estimated_tokens
        self.limit = limit
        super().__init__(
            f"context budget exhausted (estimated={estimated_tokens} > limit={limit}); "
            "refusing to start LLM call"
        )


def _content_units(content: Any) -> int:
    """Conservative UTF-8 byte count for a message content value."""
    if content is None:
        return 0
    if isinstance(content, str):
        return len(content.encode("utf-8"))
    if isinstance(content, (list, tuple)):
        total = 0
        for part in content:
            if isinstance(part, str):
                total += len(part.encode("utf-8"))
            elif isinstance(part, dict):
                total += len(
                    json.dumps(part, ensure_ascii=False, default=str).encode("utf-8")
                )
            else:
                total += len(str(part).encode("utf-8"))
        return total
    return len(str(content).encode("utf-8"))


def estimate_input_units(messages: Sequence[BaseMessage]) -> int:
    """Conservative token upper bound for a complete message list.

    Counts every message's role/type, content, name, tool-call structure and
    ``tool_call_id`` as UTF-8 bytes plus fixed overhead. This deliberately does
    not call a provider tokenizer and must not be reported as measured usage.
    """
    total = 0
    for msg in messages:
        total += CONTEXT_MESSAGE_OVERHEAD
        total += len(str(getattr(msg, "type", "")).encode("utf-8"))
        total += _content_units(getattr(msg, "content", None))
        name = getattr(msg, "name", None)
        if name:
            total += len(str(name).encode("utf-8"))
        tool_call_id = getattr(msg, "tool_call_id", None)
        if tool_call_id:
            total += len(str(tool_call_id).encode("utf-8"))
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            total += CONTEXT_TOOL_CALL_OVERHEAD * len(tool_calls)
            total += len(
                json.dumps(tool_calls, ensure_ascii=False, default=str).encode("utf-8")
            )
    return total


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
