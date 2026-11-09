"""Synthetic release-evidence gate tests.

All metadata here is explicitly synthetic. Only two boundaries are mocked:
``source_fingerprint`` and ``EvidencePackIO.import_pack``. No live files or
provider calls are used.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from research_desk.eval.case_registry import all_cases, case_for
from research_desk.eval.quality import (
    MANDATORY,
    PROVENANCE,
    source_fingerprint,
    validate_release,
)
from research_desk.models import InputSnapshot

MODEL = "deepseek-flash"
PROVIDER = "deepseek"


def _write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def _fake_pack(source: Path):
    arm = Path(source).parent
    summary = json.loads((arm / "summary.json").read_text(encoding="utf-8"))
    case = case_for(summary["ticker"])
    text = (
        f"{case['identity']['company_name']} {case['analysis_date']} "
        f"close {case['latest_close']:.2f} {case['source_id']}"
    )
    identity = dict(case["identity"])
    return SimpleNamespace(
        complete=True,
        manifest=SimpleNamespace(
            outcome="completed",
            ticker=summary["ticker"],
            trade_date=case["analysis_date"],
            context_mode=summary["context_mode"],
        ),
        usage=SimpleNamespace(
            calls=summary["calls"],
            input_tokens=summary["input_tokens"],
            output_tokens=summary["output_tokens"],
            total_tokens=summary["total_tokens"],
        ),
        final_state={"market_report": text, "final_trade_decision": text},
        input=InputSnapshot(
            identity=identity,
            data_snapshot={},
            available_sources={
                "identity": identity,
                "source_id": case["source_id"],
                "market_source_id": f"market-{case['ticker'].lower()}",
                "as_of": case["as_of"],
                "latest_close": case["latest_close"],
                "verified_snapshot": f"last_close: {case['latest_close']:.2f}",
            },
        ),
    )


@pytest.fixture()
def synthetic_release(tmp_path, monkeypatch):
    root = tmp_path / "root"
    root.mkdir()
    evidence = tmp_path / "evaluation" / "release"
    current = "sha256:synthetic-current"
    config = {
        "llm_provider": PROVIDER,
        "quick_think_llm": MODEL,
        "deep_think_llm": MODEL,
        "max_tokens": 1800,
        "temperature": 0,
        "llm_max_retries": 2,
        "max_debate_rounds": 1,
        "max_risk_discuss_rounds": 1,
        "extra_body": {"thinking": {"type": "disabled"}},
        "backend_url": "https://example.invalid/v1",
        "checkpoint_enabled": False,
    }
    for case in all_cases():
        ticker = case["ticker"]
        for mode in ("baseline", "compact"):
            if mode == "baseline":
                tokens, wall = (100, 50, 150), 10.0
            else:
                tokens, wall = (70, 30, 100), 9.0
            arm = evidence / ticker / mode
            summary = {
                "ticker": ticker,
                "context_mode": mode,
                "outcome": "completed",
                "pack_complete": True,
                "error": None,
                "calls": 2,
                "input_tokens": tokens[0],
                "output_tokens": tokens[1],
                "total_tokens": tokens[2],
                "wall_seconds": wall,
            }
            _write(arm / "summary.json", summary)
            _write(arm / "config.json", config)
            _write(arm / PROVENANCE, {
                "source_fingerprint": current, "model": MODEL, "provider": PROVIDER,
            })
            judge_dir = evidence / "judge" / ticker / mode
            _write(judge_dir / "judge.json", {
                "support": 0.9,
                "relevance": 0.9,
                "valid_citation_rate": 1.0,
                "semantic_valid": True,
                "semantic_errors": [],
                "error": False,
                "deterministic_checks": [
                    {"check": name, "passed": True, "detail": "synthetic"}
                    for name in MANDATORY
                ],
            })
            _write(judge_dir / PROVENANCE, {
                "source_fingerprint": current, "model": MODEL, "provider": PROVIDER,
            })

    monkeypatch.setattr(
        "research_desk.eval.quality.source_fingerprint", lambda _root: current
    )
    from research_desk.evidence import EvidencePackIO

    monkeypatch.setattr(EvidencePackIO, "import_pack", lambda _self, source: _fake_pack(source))
    return {"root": root, "evidence": evidence, "current": current}


def _mutate(path: Path, change) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    change(data)
    _write(path, data)


def _validate(fixture):
    return validate_release(fixture["root"], fixture["evidence"])


def test_source_fingerprint_accepts_yaml_only_prompt_tree(tmp_path):
    root = tmp_path / "tree"
    (root / "src/research_desk").mkdir(parents=True)
    (root / "src/research_desk/module.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "prompts").mkdir()
    prompt = root / "prompts/research.yaml"
    prompt.write_text("prompt: research\n", encoding="utf-8")
    (root / "test/fixtures/market").mkdir(parents=True)
    (root / "test/fixtures/market/AAPL.csv").write_text(
        "Date,Close\n2026-07-31,308.91\n", encoding="utf-8"
    )
    (root / "test/fixtures/market/orchestration-manifest.json").write_text(
        "{}\n", encoding="utf-8"
    )
    (root / "pyproject.toml").write_text("[project]\nname = 'minimal'\n", encoding="utf-8")
    (root / "requirements-lock.txt").write_text("pytest==9.1.1\n", encoding="utf-8")

    first = source_fingerprint(root)
    assert first.startswith("sha256:")

    prompt.write_text("prompt: changed\n", encoding="utf-8")
    assert source_fingerprint(root) != first


def test_complete_synthetic_release_passes_and_reports_targets(synthetic_release):
    result = _validate(synthetic_release)
    assert result["failures"] == []
    aggregate = result["metrics"]["aggregate"]
    assert aggregate["token_reduction"] == pytest.approx(1 / 3)
    assert aggregate["mean_support_drop"] == pytest.approx(0.0)
    assert aggregate["mean_relevance_drop"] == pytest.approx(0.0)
    assert aggregate["wall_ratio"] == pytest.approx(0.9)
    assert all(target["passed"] for target in result["metrics"]["should_targets"].values())


@pytest.mark.parametrize("metric", ["support", "relevance"])
def test_quality_metric_drop_over_limit_fails(synthetic_release, metric):
    for case in all_cases():
        _mutate(
            synthetic_release["evidence"]
            / "judge"
            / case["ticker"]
            / "compact"
            / "judge.json",
            lambda data, metric=metric: data.update({metric: 0.84}),
        )
    result = _validate(synthetic_release)
    failures = " ".join(result["failures"])
    assert f"mean {metric} drop" in failures
    assert result["metrics"]["aggregate"][f"mean_{metric}_drop"] > 0.05


def test_missing_arm_fails(synthetic_release):
    import shutil

    shutil.rmtree(synthetic_release["evidence"] / "AAPL" / "compact")
    result = _validate(synthetic_release)
    assert any("AAPL/compact: arm missing" in f for f in result["failures"])


def test_stale_fingerprint_fails(synthetic_release):
    _mutate(
        synthetic_release["evidence"] / "AAPL" / "baseline" / PROVENANCE,
        lambda d: d.update(source_fingerprint="sha256:stale"),
    )
    result = _validate(synthetic_release)
    assert any("stale or incorrect source fingerprint" in f for f in result["failures"])


def test_missing_named_deterministic_check_fails(synthetic_release):
    def drop(data):
        data["deterministic_checks"] = [
            c for c in data["deterministic_checks"] if c["check"] != "source_id_referenced"
        ]

    _mutate(
        synthetic_release["evidence"] / "judge" / "MSFT" / "compact" / "judge.json",
        drop,
    )
    result = _validate(synthetic_release)
    assert any(
        "mandatory deterministic check missing: source_id_referenced" in f
        for f in result["failures"]
    )


def test_model_mismatch_fails(synthetic_release):
    _mutate(
        synthetic_release["evidence"] / "NVDA" / "baseline" / PROVENANCE,
        lambda d: d.update(model="wrong-model"),
    )
    result = _validate(synthetic_release)
    assert any("NVDA/baseline: run provenance model" in f for f in result["failures"])


def test_failed_semantics_and_support_fail(synthetic_release):
    def degrade(data):
        data["semantic_valid"] = False
        data["semantic_errors"] = ["quarterly EPS labeled as TTM"]
        data["support"] = 0.5

    _mutate(
        synthetic_release["evidence"] / "judge" / "AMZN" / "baseline" / "judge.json",
        degrade,
    )
    result = _validate(synthetic_release)
    failures = " ".join(result["failures"])
    assert "semantic_valid is not true" in failures
    assert "semantic_errors is not empty" in failures
    assert "support below 0.8" in failures


def test_omitted_semantic_valid_is_not_a_pass(synthetic_release):
    _mutate(
        synthetic_release["evidence"] / "judge" / "META" / "compact" / "judge.json",
        lambda d: d.pop("semantic_valid"),
    )
    result = _validate(synthetic_release)
    assert any("semantic_valid is not true" in f for f in result["failures"])
