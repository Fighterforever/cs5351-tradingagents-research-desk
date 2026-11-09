"""Per-agent COMMON grounding + prompt compaction on the real LLM inputs.

Fresh evaluation runs have essentially no past memory, so compressing only
``past_context`` has almost no effect, and that header is not even read by many
downstream upstream roles. This module fixes the shared grounding/citation
failure by wrapping the real LangChain chat model with a small plain delegate
(exposing ``invoke``, ``bind_tools`` and ``with_structured_output``) that
injects the identical COMMON grounding layer into *every* request in BOTH modes
(baseline and compact), while retaining the real LangChain client and the
upstream ``GraphSetup``.

- The common grounding layer carries the real per-case ticker, legal company
  identity, analysis date, frozen close, the source-ID registry
  (``src-<ticker>`` = official earnings news, ``market-<ticker>`` = market
  CSV/technical computations), the short official earnings notes and citation
  rules. It is the shared correctness fix applied to both arms.
- For ``context_mode == "baseline"`` the delegate only prepends the common
  grounding layer; the substantive prompt/history is left uncompressed (no
  artificial padding, no rewrite).
- For ``compact`` the delegate additionally trims redundant message text,
  de-duplicates, and appends a concise-output instruction, while preserving key
  quoted facts (the standing-constraints and source markers) in every prompt.

Message integrity rules (review finding #1):

- A message is rebuilt with the declared model-copy/update API, changing only
  ``content``. ``AIMessage.tool_calls``, ``ToolMessage.tool_call_id``,
  ``id``/``name`` and every other field are preserved — never re-created.
- A ``ToolMessage`` that answers an assistant tool call is never de-duplicated
  away and never truncated: dropping or merging it would break the assistant's
  pending tool call.
- An ``AIMessage`` that carries ``tool_calls`` (typically with empty ``content``)
  is kept, never dropped, even though its text is empty.
- Evidence messages (messages carrying a ``_FACT_MARKERS`` token) are not
  truncated. Trimming only verbose, non-fact prose is allowed; discarding
  numbers, identity, dates or sources is not.
- The concise-output instruction targets ~600 tokens for compact roles while
  the provider ``max_tokens`` stays 1800 in both arms (set in the graph config).
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage

from ..budget import ContextBudgetExceeded, estimate_input_units
from ..config import DEFAULT_CONTEXT_MAX_TOKENS, DEFAULT_CONTEXT_TRIGGER_TOKENS

logger = logging.getLogger(__name__)


class BudgetObservation(TypedDict):
    """Conservative whole-input budget observation emitted per request."""

    before_units: int
    after_units: int
    trigger: int
    cap: int
    compacted: bool
    metric: str


BudgetObserver = Callable[[BudgetObservation], None]

# Content markers that carry the facts which must survive compaction. A message
# containing any marker is kept (not trimmed below the fact floor).
_FACT_MARKERS = (
    "STANDING ANALYSIS CONSTRAINTS",
    "last_close",
    "NO_DATA_AVAILABLE",
    "source_id",
    "src-",
    "USD",
    "% of equity",
    "integer_shares",
    "no_shorting",
    "Analysis date",
    "Company:",
    "Instrument identity",
    "trade_date",
    "past_context",
)

# Concise-output target for the compact arm (~600 tokens) while the provider
# ``max_tokens`` cap stays 1800 in both arms.
_OUTPUT_INSTRUCTION = (
    "Respond concisely: keep your entire answer within {max_tokens} tokens. "
    "Do not repeat the input; only output the requested analysis."
)


def _tuple_to_message(role: str, content: Any) -> BaseMessage | None:
    """Map a ``(role, content)`` pair to a message, or None for an unknown role."""
    role = (role or "").lower()
    if role == "system":
        return SystemMessage(content=content)
    if role in ("human", "user"):
        return HumanMessage(content=content)
    if role in ("ai", "assistant"):
        return AIMessage(content=content)
    return None


def _to_messages(input: Any) -> list[BaseMessage] | None:
    """Normalise a model input to a list of messages, or None if not list-like."""
    if isinstance(input, list) and all(isinstance(m, BaseMessage) for m in input):
        return list(input)
    if isinstance(input, str):
        return [HumanMessage(content=input)]
    if isinstance(input, (list, tuple)) and input and all(
        isinstance(p, (list, tuple)) and len(p) == 2 for p in input
    ):
        mapped = [_tuple_to_message(role, content) for role, content in input]
        if all(m is not None for m in mapped):
            return [m for m in mapped if m is not None]
        return None  # unknown role: pass through unchanged rather than drop content
    if hasattr(input, "to_messages"):
        try:
            return input.to_messages()
        except Exception:  # noqa: BLE001 - PromptValue edge cases
            return None
    return None


def _content_of(msg: BaseMessage) -> str:
    c = msg.content
    return c if isinstance(c, str) else str(c)


def _has_fact_marker(text: str) -> bool:
    low = text.lower()
    return any(marker.lower() in low for marker in _FACT_MARKERS)


def _rebuild(msg: BaseMessage, content: str) -> BaseMessage:
    """Rebuild a message with only ``content`` changed; preserve every other field.

    ``model_copy(update=...)`` keeps ``type``, ``id``, ``name``, ``tool_calls``,
    ``tool_call_id``, ``additional_kwargs`` and any subclass state intact, so an
    ``AIMessage`` keeps its tool calls and a ``ToolMessage`` keeps the
    ``tool_call_id`` the assistant is waiting on.
    """
    return msg.model_copy(update={"content": content})


def compact_transform(
    input: Any,
    *,
    max_output_tokens: int = 600,
    max_msg_chars: int = 1500,
    fact_floor_chars: int = 6000,
) -> Any:
    """Transform a per-agent prompt for the compact arm.

    Keeps message roles, trims verbose non-fact prose to ``max_msg_chars``,
    removes exact duplicate messages (never a tool response), and appends a
    concise-output instruction. Messages carrying key facts are preserved so no
    grounding marker is dropped. Every message is rebuilt via
    :func:`_rebuild`, so tool-call state survives unchanged.
    """
    messages = _to_messages(input)
    if messages is None:
        return input  # cannot transform; pass through unchanged

    seen: set[str] = set()
    kept: list[BaseMessage] = []
    for msg in messages:
        content = _content_of(msg)
        if isinstance(msg, ToolMessage):
            # A tool response answers an assistant tool call: never dedupe,
            # never truncate, never drop — the assistant is waiting on it.
            kept.append(msg)
            continue
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            # An assistant message that issued tool calls (text may be empty);
            # keep it whole so the tool_calls survive to the next turn.
            kept.append(_rebuild(msg, content))
            continue
        if not content:
            continue
        if content in seen:
            continue  # drop exact duplicate prose messages only
        seen.add(content)
        if not _has_fact_marker(content) and len(content) > max_msg_chars:
            content = content[:max_msg_chars].rstrip() + "\n[... compacted ...]"
        kept.append(_rebuild(msg, content))

    kept.append(
        SystemMessage(content=_OUTPUT_INSTRUCTION.format(max_tokens=max_output_tokens))
    )
    return kept


_COMPACTED_MARKER = "\n[... context compacted ...]"
_BUDGET_PROSE_CHARS = 240


def _is_expendable_old_prose(
    msg: BaseMessage, index: int, latest_human: int
) -> bool:
    """Whether an old, non-fact plain prose message may be compacted/removed.

    System constraints, the latest user/task, fact-bearing evidence and every
    assistant/tool-call group member are never expendable.
    """
    if index == latest_human:
        return False
    if not isinstance(msg, (HumanMessage, AIMessage)):
        return False
    if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
        return False
    return not _has_fact_marker(_content_of(msg))


def enforce_context_budget(
    messages: list[BaseMessage],
    *,
    trigger_tokens: int,
    max_tokens: int,
    prose_chars: int = _BUDGET_PROSE_CHARS,
) -> tuple[list[BaseMessage], bool, int]:
    """Bound a complete message list, preserving mandatory material.

    Below ``trigger_tokens`` the input is returned unchanged. Above it, older
    expendable non-fact prose is first shortened and then dropped oldest-first.
    System constraints, the latest user/task, fact-bearing evidence and entire
    assistant tool-call / ToolMessage groups are never removed. If the required
    material still exceeds ``max_tokens``, raise :class:`ContextBudgetExceeded`
    before the provider is invoked.

    Returns ``(messages, compacted, before_units)``.
    """
    before = estimate_input_units(messages)
    if before <= trigger_tokens and before <= max_tokens:
        return list(messages), False, before

    latest_human = max(
        (i for i, m in enumerate(messages) if isinstance(m, HumanMessage)),
        default=-1,
    )
    expendable = [
        i
        for i, m in enumerate(messages)
        if _is_expendable_old_prose(m, i, latest_human)
    ]

    compacted_messages: list[BaseMessage] = []
    for i, msg in enumerate(messages):
        if i in expendable:
            content = _content_of(msg)
            if len(content) > prose_chars:
                content = content[:prose_chars].rstrip() + _COMPACTED_MARKER
            compacted_messages.append(_rebuild(msg, content))
        else:
            compacted_messages.append(msg)

    after = estimate_input_units(compacted_messages)
    if after > max_tokens:
        dropped: set[int] = set()
        for i in expendable:
            dropped.add(i)
            candidate = [m for j, m in enumerate(compacted_messages) if j not in dropped]
            after = estimate_input_units(candidate)
            if after <= max_tokens:
                compacted_messages = candidate
                break
        else:
            compacted_messages = [
                m for j, m in enumerate(compacted_messages) if j not in dropped
            ]
            after = estimate_input_units(compacted_messages)

    if after > max_tokens:
        raise ContextBudgetExceeded(after, max_tokens)
    return compacted_messages, True, before


def delegate_transform(
    input: Any,
    *,
    context_mode: str,
    common_grounding: str,
    max_output_tokens: int = 600,
    max_msg_chars: int = 1500,
) -> Any:
    """Inject the COMMON grounding layer into a request, then compact if needed.

    Both modes prepend the identical ``common_grounding`` SystemMessage so every
    request (analyst, researcher, trader, risk, portfolio manager, reflection)
    sees the same source registry, facts and citation rules.

    - baseline: substantive history is left untouched (grounding is the only
      addition, the shared correctness fix).
    - compact: the original substantive messages are then de-duplicated/trimmed
      and a concise-output instruction appended (unchanged 600-token target;
      provider ``max_tokens`` cap stays 1800 in both arms).

    Un-transformable inputs (None / unknown shapes) pass through unchanged.
    """
    messages = _to_messages(input)
    if messages is None:
        return input
    if context_mode == "compact":
        body = compact_transform(
            messages,
            max_output_tokens=max_output_tokens,
            max_msg_chars=max_msg_chars,
        )
    else:
        body = list(messages)
    return [SystemMessage(content=common_grounding)] + list(body)


class GroundingDelegate:
    """A small plain delegate around the real LangChain client.

    ``invoke`` transforms and delegates; ``bind_tools`` and
    ``with_structured_output`` delegate to the *real* client's binding and then
    compose a ``RunnableLambda`` preprocessor with the returned Runnable, so the
    common grounding layer reaches every invocation through every path. There is
    no dynamic ``__class__`` mutation and no dropped tool responses: the real
    client's returned ``AIMessage.tool_calls`` and ``ToolMessage.tool_call_id``
    are preserved exactly because the composed runnables hand them through
    untouched.
    """

    def __init__(
        self,
        llm: Any,
        *,
        context_mode: str,
        common_grounding: str,
        max_output_tokens: int = 600,
        max_msg_chars: int = 1500,
        context_max_tokens: int = DEFAULT_CONTEXT_MAX_TOKENS,
        context_trigger_tokens: int = DEFAULT_CONTEXT_TRIGGER_TOKENS,
        budget_observer: BudgetObserver | None = None,
    ):
        from langchain_core.runnables import RunnableLambda

        self.llm = llm
        self.context_mode = context_mode
        self.common_grounding = common_grounding
        self.max_output_tokens = max_output_tokens
        self.max_msg_chars = max_msg_chars
        self.context_max_tokens = context_max_tokens
        self.context_trigger_tokens = context_trigger_tokens
        self.budget_observer = budget_observer
        self._pre = RunnableLambda(self._transform)

    def _transform(self, input: Any) -> Any:
        transformed = delegate_transform(
            input,
            context_mode=self.context_mode,
            common_grounding=self.common_grounding,
            max_output_tokens=self.max_output_tokens,
            max_msg_chars=self.max_msg_chars,
        )
        complete = _to_messages(transformed)
        if complete is None:
            return transformed

        bounded, compacted, before = enforce_context_budget(
            complete,
            trigger_tokens=self.context_trigger_tokens,
            max_tokens=self.context_max_tokens,
        )
        after = estimate_input_units(bounded)
        logger.info(
            "context budget conservative_units before=%d after=%d trigger=%d cap=%d "
            "compacted=%s mode=%s",
            before,
            after,
            self.context_trigger_tokens,
            self.context_max_tokens,
            compacted,
            self.context_mode,
        )
        if self.budget_observer is not None:
            self.budget_observer(
                {
                    "before_units": before,
                    "after_units": after,
                    "trigger": self.context_trigger_tokens,
                    "cap": self.context_max_tokens,
                    "compacted": compacted,
                    "metric": "utf8_upper_bound",
                }
            )
        return bounded

    def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> Any:
        return self.llm.invoke(self._pre.invoke(input, config), config, **kwargs)

    def bind_tools(self, tools: Any, **kwargs: Any) -> Any:
        bound = self.llm.bind_tools(tools, **kwargs)
        return self._pre | bound

    def with_structured_output(self, schema: Any, **kwargs: Any) -> Any:
        structured = self.llm.with_structured_output(schema, **kwargs)
        return self._pre | structured


def wrap_for_mode(
    llm: Any,
    context_mode: str,
    *,
    common_grounding: str,
    max_output_tokens: int = 600,
    max_msg_chars: int = 1500,
    context_max_tokens: int = DEFAULT_CONTEXT_MAX_TOKENS,
    context_trigger_tokens: int = DEFAULT_CONTEXT_TRIGGER_TOKENS,
    budget_observer: BudgetObserver | None = None,
) -> Any:
    """Wrap ``llm`` with a :class:`GroundingDelegate` for BOTH modes.

    The delegate injects the identical COMMON grounding layer into every
    request; baseline leaves the substantive history untouched while compact
    also trims/de-duplicates and appends the concise-output instruction. Every
    request is then bounded by the whole-input context budget, and an optional
    observer receives the conservative before/after units.
    """
    return GroundingDelegate(
        llm,
        context_mode=context_mode,
        common_grounding=common_grounding,
        max_output_tokens=max_output_tokens,
        max_msg_chars=max_msg_chars,
        context_max_tokens=context_max_tokens,
        context_trigger_tokens=context_trigger_tokens,
        budget_observer=budget_observer,
    )
