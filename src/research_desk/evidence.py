"""Evidence capture, evidence packs, and offline replay primitives.

Two capture channels feed an evidence pack:

1. A LangChain callback handler (:class:`EvidenceRecorder`) attached to the
   graph's LLMs and tool calls. It records every LLM request/response with the
   provider-reported usage and every tool call/result.
2. Narrow adapter hooks for the *direct data paths* callbacks cannot see —
   the ticker-identity lookup and the realized-returns read that happen inside
   ``TradingAgentsGraph`` itself. Those are recorded via
   :func:`record_data_read` from the adapter.

An evidence pack is a self-contained directory (or ZIP of one) with a
manifest, the input snapshot, the event log, the final graph state, usage,
reports and optionally the proposal. Replay imports the pack and rebuilds the
report tree, signal and policy outputs deterministically with zero external
calls. A pack missing required material fails clearly instead of replaying a
silent partial.
"""

from __future__ import annotations

import json
import logging
import zipfile
from pathlib import Path
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage
from langchain_core.outputs import LLMResult
from pydantic import BaseModel

from .budget import BudgetTracker
from .models import (
    CallUsage,
    EvidenceEvent,
    EvidencePack,
    InputSnapshot,
    RunManifest,
    UsageSummary,
    utcnow_iso,
)

logger = logging.getLogger(__name__)

# Files that make up a complete evidence pack. ``complete`` is only set when all
# of them are present and parseable.
PACK_FILES = (
    "manifest.json",
    "input.json",
    "events.jsonl",
    "final_state.json",
    "usage.json",
    "calls.json",
)

_SECRET_KEY_FRAGMENTS = (
    "api_key",
    "apikey",
    "password",
    "secret",
    "credential",
    "authorization",
)


def _is_credential_key(key: str) -> bool:
    """Small explicit credential predicate (SEC-001).

    Matches real credential names -- ``api_key``, ``apikey``, ``*_token``
    (including a bare ``token``), ``password``, ``secret``, ``credential`` and
    ``authorization`` -- without classifying provider-reported usage, count,
    budget or ``token_limit`` fields as credentials. A substring rule for
    ``token`` would redact ``input_tokens``/``output_tokens``/``total_tokens``
    and destroy measured evidence, so only exact and ``_token``-suffixed keys
    count as token credentials.
    """
    kl = key.lower()
    if kl == "token" or kl.endswith("_token"):
        return True
    return any(frag in kl for frag in _SECRET_KEY_FRAGMENTS)


def sanitize_secrets(obj: Any, _key: str = "") -> Any:
    """Recursively redact credential-looking keys so packs never hold secrets (SEC-001).

    Actual Pydantic models -- including LangChain ``HumanMessage``,
    ``AIMessage`` and ``ToolMessage`` values nested in graph state -- are
    converted to JSON-native dicts via their ``model_dump(mode="json")`` API
    before redaction. Their type, content, tool calls, tool call id,
    additional kwargs, response metadata and usage metadata therefore survive
    export/import intact while any credential fields inside them are still
    redacted. Messages are never stringified.
    """
    if isinstance(obj, BaseModel):
        return sanitize_secrets(obj.model_dump(mode="json"), _key)
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if _is_credential_key(str(k)):
                out[k] = "**REDACTED**" if v not in (None, "") else v
            else:
                out[k] = sanitize_secrets(v, _key)
        return out
    if isinstance(obj, (list, tuple)):
        return [sanitize_secrets(v, _key) for v in obj]
    return obj


class EvidenceLog:
    """Ordered, sequence-numbered event log for one run."""

    def __init__(self) -> None:
        self.events: list[EvidenceEvent] = []

    def record(self, kind: str, node: str | None = None, **payload: Any) -> EvidenceEvent:
        event = EvidenceEvent(
            seq=len(self.events) + 1,
            kind=kind,
            ts=utcnow_iso(),
            node=node,
            payload=payload,
        )
        self.events.append(event)
        return event


def record_data_read(
    log: EvidenceLog, source: str, ticker: str, payload: Any, node: str | None = None
) -> None:
    """Record a direct data read (identity, realized returns) bypassing callbacks."""
    log.record(
        "data_read",
        node=node,
        source=source,
        ticker=ticker,
        payload=sanitize_secrets(payload),
    )


class EvidenceRecorder(BaseCallbackHandler):
    """Records LLM/tool activity and enforces the run's LLM call budget.

    ``on_chat_model_start`` both counts the call against the budget (raising
    :class:`~research_desk.budget.BudgetExhausted` once the limit is reached,
    which aborts the graph before a further request is started) and emits an
    ``llm_request`` event. ``on_llm_end`` records the provider-reported usage.
    """

    def __init__(self, log: EvidenceLog, budget: BudgetTracker):
        super().__init__()
        self.log = log
        self.budget = budget
        # LangChain swallows callback-handler exceptions unless the handler asks
        # to propagate them. The budget guard lives in ``on_chat_model_start``
        # and must really abort the next LLM request, so this handler must
        # re-raise BudgetExhausted instead of letting the manager swallow it.
        self.raise_error = True

    @staticmethod
    def _node_from_kwargs(kwargs: dict[str, Any]) -> str | None:
        metadata = kwargs.get("metadata") or {}
        node = metadata.get("langgraph_node")
        return node if isinstance(node, str) else None

    def on_chat_model_start(self, serialized, messages, **kwargs) -> None:
        self._start_llm(serialized, messages=messages, **kwargs)

    def on_llm_start(self, serialized, prompts, **kwargs) -> None:
        self._start_llm(serialized, prompts=prompts, **kwargs)

    def _start_llm(self, serialized, messages=None, prompts=None, **kwargs) -> None:
        # Enforce the budget BEFORE recording: a blocked call never starts.
        self.budget.start_call()
        node = self._node_from_kwargs(kwargs)
        name = kwargs.get("name")
        model = (serialized or {}).get("id") or (serialized or {}).get("name")
        payload: dict[str, Any] = {"model": model or name or "unknown"}
        if messages is not None:
            payload["prompt"] = self._serialize_messages(messages)
        if prompts is not None:
            payload["prompt"] = "\n\n---PROMPT---\n\n".join(str(p) for p in prompts)
        self.log.record("llm_request", node=node, **payload)

    @staticmethod
    def _serialize_messages(messages) -> str:
        if not messages:
            return ""
        if isinstance(messages, list):
            parts: list[str] = []
            for group in messages:
                if isinstance(group, list):
                    parts.extend(_msg_to_text(m) for m in group)
                else:
                    parts.append(_msg_to_text(group))
            return "\n\n".join(str(p) for p in parts if p)
        return str(messages)

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        usage = _extract_usage(response)
        self.budget.record_usage(usage)
        node = self._node_from_kwargs(kwargs)
        text = None
        try:
            generation = response.generations[0][0]
            if hasattr(generation, "text"):
                text = generation.text
        except (IndexError, TypeError, AttributeError):
            text = None
        self.log.record(
            "llm_response",
            node=node,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            response=text,
        )

    def on_llm_error(self, error, **kwargs) -> None:
        self.log.record("llm_response", node=self._node_from_kwargs(kwargs), error=str(error))

    def on_tool_start(self, serialized, input_str, **kwargs) -> None:
        name = kwargs.get("name") or (serialized or {}).get("name")
        node = self._node_from_kwargs(kwargs)
        try:
            args = json.loads(input_str) if input_str else {}
        except (TypeError, ValueError):
            args = {"raw": input_str}
        self.log.record("tool_call", node=node, name=name, args=args)

    def on_tool_end(self, output, **kwargs) -> None:
        self.log.record(
            "tool_result",
            node=self._node_from_kwargs(kwargs),
            name=kwargs.get("name"),
            result=_safe_str(output),
        )

    def on_tool_error(self, error, **kwargs) -> None:
        self.log.record(
            "tool_result",
            node=self._node_from_kwargs(kwargs),
            name=kwargs.get("name"),
            error=str(error),
        )


def _msg_to_text(msg: Any) -> str:
    if hasattr(msg, "content"):
        return _safe_str(msg.content)
    return str(msg)


def _safe_str(value: Any, limit: int = 200_000) -> str:
    s = value if isinstance(value, str) else str(value)
    return s[:limit]


def _extract_usage(response: LLMResult) -> CallUsage:
    try:
        generation = response.generations[0][0]
    except (IndexError, TypeError):
        return CallUsage()
    if hasattr(generation, "message") and isinstance(generation.message, AIMessage):
        meta = getattr(generation.message, "usage_metadata", None) or {}
        return CallUsage(
            input_tokens=meta.get("input_tokens", 0) or 0,
            output_tokens=meta.get("output_tokens", 0) or 0,
        )
    return CallUsage()


# ---------------------------------------------------------------------------
# Evidence pack IO
# ---------------------------------------------------------------------------


class EvidencePackError(Exception):
    """Raised when an evidence pack is missing required material or malformed."""


def _data_snapshot_from_events(events: list[EvidenceEvent]) -> dict[str, dict[str, str]]:
    """Rebuild the frozen tool-data snapshot from the tool_call/tool_result events.

    Keys are the canonical JSON of the tool arguments; values are the recorded
    result strings. This is the material a controlled rerun (``data_mode=frozen``)
    feeds back into the graph's tool nodes.
    """
    snapshot: dict[str, dict[str, str]] = {}
    pending: dict[int, tuple[str, str]] = {}  # seq -> (name, args_key)
    for ev in events:
        if ev.kind == "tool_call":
            name = ev.payload.get("name") or "unknown"
            args = ev.payload.get("args") or {}
            args_key = json.dumps(args, sort_keys=True, default=str)
            pending[ev.seq] = (name, args_key)
        elif ev.kind == "tool_result":
            name = ev.payload.get("name")
            result = ev.payload.get("result")
            if result is None:
                continue
            source = pending.pop(ev.seq, None)
            if source is not None:
                _, args_key = source
                snapshot.setdefault(source[0], {})[args_key] = result
            elif name:
                snapshot.setdefault(name, {})["__fallback__"] = result
    return snapshot


def build_pack(
    manifest: RunManifest,
    input_snapshot: InputSnapshot,
    events: list[EvidenceEvent],
    final_state: dict[str, Any],
    usage: UsageSummary,
    calls: list[Any] | None = None,
    proposal: Any = None,
    reports_written: list[str] | None = None,
) -> EvidencePack:
    return EvidencePack(
        manifest=manifest,
        input=input_snapshot,
        events=events,
        final_state=final_state,
        usage=usage,
        calls=calls or [],
        proposal=proposal,
        reports_written=reports_written or [],
        complete=False,
    )


class EvidencePackIO:
    """Writes and reads evidence packs as directories or ZIP archives."""

    def export(self, pack: EvidencePack, out_dir: str | Path) -> Path:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "manifest.json").write_text(
            json.dumps(sanitize_secrets(pack.manifest.model_dump()), indent=2), encoding="utf-8"
        )
        (out / "input.json").write_text(
            json.dumps(sanitize_secrets(pack.input.model_dump()), indent=2), encoding="utf-8"
        )
        with (out / "events.jsonl").open("w", encoding="utf-8") as fh:
            for ev in pack.events:
                fh.write(json.dumps(sanitize_secrets(ev.model_dump())) + "\n")
        (out / "final_state.json").write_text(
            json.dumps(sanitize_secrets(pack.final_state), indent=2), encoding="utf-8"
        )
        (out / "usage.json").write_text(
            json.dumps(pack.usage.model_dump(), indent=2), encoding="utf-8"
        )
        (out / "calls.json").write_text(
            json.dumps(sanitize_secrets([c.model_dump() for c in pack.calls]), indent=2),
            encoding="utf-8",
        )
        if pack.proposal is not None:
            (out / "proposal.json").write_text(
                json.dumps(pack.proposal.model_dump(), indent=2), encoding="utf-8"
            )
        meta = {"files": sorted(p.name for p in out.iterdir()), "complete": True}
        (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        pack.complete = True
        return out

    def export_zip(self, pack: EvidencePack, zip_path: str | Path) -> Path:
        zpath = Path(zip_path)
        zpath.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
            for name, data in self._flatten(pack).items():
                zf.writestr(name, data)
        return zpath

    @staticmethod
    def _flatten(pack: EvidencePack) -> dict[str, str]:
        files: dict[str, str] = {
            "manifest.json": json.dumps(sanitize_secrets(pack.manifest.model_dump()), indent=2),
            "input.json": json.dumps(sanitize_secrets(pack.input.model_dump()), indent=2),
            "events.jsonl": "\n".join(
                json.dumps(sanitize_secrets(ev.model_dump())) for ev in pack.events
            ),
            "final_state.json": json.dumps(sanitize_secrets(pack.final_state), indent=2),
            "usage.json": json.dumps(pack.usage.model_dump(), indent=2),
            "calls.json": json.dumps(
                sanitize_secrets([c.model_dump() for c in pack.calls]), indent=2
            ),
        }
        if pack.proposal is not None:
            files["proposal.json"] = json.dumps(pack.proposal.model_dump(), indent=2)
        return files

    def import_pack(self, source: str | Path) -> EvidencePack:
        """Load a complete evidence pack from a directory or ZIP.

        Raises :class:`EvidencePackError` with a clear message when required
        material is missing, so a partial pack can never silently replay.
        """
        src = Path(source)
        if src.is_dir():
            return self._load_dir(src)
        if zipfile.is_zipfile(src):
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                with zipfile.ZipFile(src) as zf:
                    zf.extractall(tmp)
                return self._load_dir(Path(tmp))
        raise EvidencePackError(f"Evidence source is neither a directory nor a ZIP: {src}")

    def _load_dir(self, d: Path) -> EvidencePack:
        missing = [name for name in PACK_FILES if not (d / name).exists()]
        if missing:
            raise EvidencePackError(
                f"Incomplete evidence pack at {d}: missing required files {missing}. "
                "A complete pack must include manifest, input snapshot, events, "
                "final state, usage and calls."
            )
        manifest = RunManifest(**json.loads((d / "manifest.json").read_text(encoding="utf-8")))
        input_snapshot = InputSnapshot(
            **json.loads((d / "input.json").read_text(encoding="utf-8"))
        )
        events = [
            EvidenceEvent(**json.loads(line))
            for line in (d / "events.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        final_state = json.loads((d / "final_state.json").read_text(encoding="utf-8"))
        usage = UsageSummary(**json.loads((d / "usage.json").read_text(encoding="utf-8")))
        calls = json.loads((d / "calls.json").read_text(encoding="utf-8"))
        proposal = None
        if (d / "proposal.json").exists():
            from .models import ProposalRecord

            proposal = ProposalRecord(**json.loads((d / "proposal.json").read_text(encoding="utf-8")))
        pack = EvidencePack(
            manifest=manifest,
            input=input_snapshot,
            events=events,
            final_state=final_state,
            usage=usage,
            calls=calls,
            proposal=proposal,
            complete=True,
        )
        if manifest.outcome == "completed" and not final_state:
            raise EvidencePackError(
                f"Evidence pack {d} claims a completed run but has an empty final_state."
            )
        return pack

    def load_external_proposal(self, d: Path) -> Any:
        """Load proposal.json from a pack directory without requiring a full pack."""
        if not (d / "proposal.json").exists():
            return None
        from .models import ProposalRecord

        return ProposalRecord(**json.loads((d / "proposal.json").read_text(encoding="utf-8")))
