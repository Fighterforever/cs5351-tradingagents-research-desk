"""Focused provenance write/check tests for the live evaluation boundary.

No provider is called. The model boundary is replaced with a recording fake and
the source fingerprint is monkeypatched so these tests exercise the actual
provenance ordering and stale-source refusal logic.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from research_desk.eval import live
from research_desk.eval.live import (
    PROVENANCE_FILENAME,
    _provenance_payload,
    _read_source_fingerprint,
)


def _write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def _cfg() -> dict:
    return {
        "llm_provider": live.PROVIDER,
        "quick_think_llm": live.MODEL,
        "deep_think_llm": live.MODEL,
        "max_tokens": live.OUTPUT_CAP,
        "temperature": 0,
    }


def test_provenance_payload_uses_actual_model_provider_endpoint_and_config():
    payload = _provenance_payload(
        "sha256:abc", _cfg(), "https://example.invalid/v1"
    )

    assert PROVENANCE_FILENAME == "provenance.json"
    assert payload["source_fingerprint"] == "sha256:abc"
    assert payload["model"] == live.MODEL
    assert payload["provider"] == live.PROVIDER
    assert payload["endpoint"] == "https://example.invalid/v1"
    assert payload["deep_think_llm"] == live.MODEL
    assert payload["max_tokens"] == live.OUTPUT_CAP
    assert payload["temperature"] == 0


def test_read_source_fingerprint_handles_missing_and_invalid(tmp_path):
    path = tmp_path / PROVENANCE_FILENAME
    assert _read_source_fingerprint(path) is None
    _write(path, {"source_fingerprint": "sha256:current"})
    assert _read_source_fingerprint(path) == "sha256:current"
    path.write_text("not json", encoding="utf-8")
    assert _read_source_fingerprint(path) is None


class _FakeResult:
    def __init__(self) -> None:
        self.pack_path = None
        self.outcome = "completed"
        self.signal = "Hold"
        self.stop_reason = "completed"
        self.usage = SimpleNamespace(
            calls=0, input_tokens=0, output_tokens=0, total_tokens=0
        )
        self.error = None


def _install_fake_runner(monkeypatch, out: Path, seen: list):
    class _FakeRunner:
        def __init__(self, settings, **kwargs):
            self.settings = settings
            self.context_mode = kwargs.get("context_mode", "baseline")

        def run(self, ticker, trade_date):
            provenance_path = (
                Path(out) / ticker.upper() / self.context_mode / PROVENANCE_FILENAME
            )
            seen.append(json.loads(provenance_path.read_text(encoding="utf-8")))
            return _FakeResult()

    monkeypatch.setattr("research_desk.graph_adapter.ResearchRunner", _FakeRunner)


def test_run_writes_provenance_before_runner(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(live, "_current_source_fingerprint", lambda root: "sha256:before")
    out = tmp_path / "out"
    seen: list = []
    _install_fake_runner(monkeypatch, out, seen)

    summary = live.run_evaluate_case("AAPL", "baseline", out)

    assert seen == [{
        "source_fingerprint": "sha256:before",
        "model": live.MODEL,
        "provider": live.PROVIDER,
        "endpoint": live._base_url(),
        "deep_think_llm": live.MODEL,
        "max_tokens": live.OUTPUT_CAP,
        "temperature": 0,
    }]
    saved = json.loads(
        (out / "AAPL" / "baseline" / PROVENANCE_FILENAME).read_text(encoding="utf-8")
    )
    assert saved["source_fingerprint"] == "sha256:before"
    assert summary["outcome"] == "completed"


def test_run_fails_when_source_changes_during_run(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    fingerprints = iter(["sha256:before", "sha256:after"])
    monkeypatch.setattr(live, "_current_source_fingerprint", lambda root: next(fingerprints))
    out = tmp_path / "out"
    seen: list = []
    _install_fake_runner(monkeypatch, out, seen)

    with pytest.raises(RuntimeError, match="source changed during run"):
        live.run_evaluate_case("AAPL", "baseline", out)

    summary = json.loads(
        (out / "AAPL" / "baseline" / "summary.json").read_text(encoding="utf-8")
    )
    assert summary["source_changed"] is True
    assert "refusing to certify" in summary["error"]


def test_judge_refuses_stale_run_without_scoring(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(live, "_current_source_fingerprint", lambda root: "sha256:current")
    called: list = []

    def _must_not_judge(*args, **kwargs):
        called.append(True)
        raise AssertionError("judge must not run for a stale raw run")

    monkeypatch.setattr(live, "_llm_judge", _must_not_judge)

    out = tmp_path / "out"
    (out / "AAPL" / "baseline" / "run").mkdir(parents=True)
    _write(
        out / "AAPL" / "baseline" / PROVENANCE_FILENAME,
        {"source_fingerprint": "sha256:stale"},
    )

    with pytest.raises(RuntimeError, match="refusing to certify judge results"):
        live.run_judge_case("AAPL", out)

    assert called == []
    summary = json.loads(
        (out / "judge" / "AAPL" / "summary.json").read_text(encoding="utf-8")
    )
    assert "stale" in summary["arms"]["baseline"]["error"]
    assert not (out / "judge" / "AAPL" / "baseline" / "judge.json").exists()


def test_judge_writes_provenance_before_call_and_fails_on_change(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    fingerprints = iter(["sha256:current", "sha256:changed"])
    monkeypatch.setattr(live, "_current_source_fingerprint", lambda root: next(fingerprints))

    pack = SimpleNamespace(
        manifest=SimpleNamespace(outcome="completed"),
        final_state={"final_trade_decision": "decision"},
        input=SimpleNamespace(available_sources={}),
        events=[],
    )
    from research_desk.evidence import EvidencePackIO

    monkeypatch.setattr(EvidencePackIO, "import_pack", lambda self, source: pack)
    monkeypatch.setattr(live, "_report_text_with_identity", lambda pack: "report")
    monkeypatch.setattr(live, "_deterministic_checks", lambda case, pack, ticker: [])

    out = tmp_path / "out"
    (out / "AAPL" / "baseline" / "run").mkdir(parents=True)
    _write(
        out / "AAPL" / "baseline" / PROVENANCE_FILENAME,
        {"source_fingerprint": "sha256:current"},
    )
    judge_prov = out / "judge" / "AAPL" / "baseline" / PROVENANCE_FILENAME

    def _fake_judge(*args, **kwargs):
        assert judge_prov.exists(), "judge provenance must be written before invocation"
        saved = json.loads(judge_prov.read_text(encoding="utf-8"))
        assert saved["source_fingerprint"] == "sha256:current"
        return {}, {"support": 0.9, "error": False}

    monkeypatch.setattr(live, "_llm_judge", _fake_judge)

    with pytest.raises(RuntimeError, match="refusing to certify judge results"):
        live.run_judge_case("AAPL", out)

    saved = json.loads(judge_prov.read_text(encoding="utf-8"))
    assert saved["source_fingerprint"] == "sha256:current"
    summary = json.loads(
        (out / "judge" / "AAPL" / "summary.json").read_text(encoding="utf-8")
    )
    assert "changed during judge" in summary["arms"]["baseline"]["error"]
    assert not (out / "judge" / "AAPL" / "baseline" / "judge.json").exists()
