"""Source-bound release evidence validation (ADR-004).

Provenance lives at <evidence>/<TICKER>/<mode>/provenance.json and
<evidence>/judge/<TICKER>/<mode>/provenance.json as
{"source_fingerprint","model","provider"}. Aggregate PASS is ignored.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, TypeGuard

from ..config import DEFAULT_MODEL, DEFAULT_PROVIDER

MODES = ("baseline", "compact")
PROVENANCE = "provenance.json"
MANDATORY = ("instrument_identity", "analysis_date", "final_decision_present", "frozen_price_in_report", "source_id_referenced")
SETTINGS = ("llm_provider", "quick_think_llm", "deep_think_llm", "max_tokens", "temperature", "llm_max_retries", "max_debate_rounds", "max_risk_discuss_rounds", "extra_body", "backend_url", "checkpoint_enabled")
MIN_SUPPORT = MIN_RELEVANCE = 0.8
MIN_CITATION = 0.95
COST_MIN, QUALITY_DROP_MAX, WALL_MAX = 0.20, 0.05, 1.10


def _source_paths(root: Path) -> list[Path]:
    root = Path(root)
    python_sources = [p for p in root.glob("src/research_desk/**/*.py") if p.is_file()]
    prompts = [
        p
        for pattern in ("prompts/**/*.yaml", "prompts/**/*.yml")
        for p in root.glob(pattern)
        if p.is_file()
    ]
    groups = [python_sources, prompts]
    required = [root / r for r in ("pyproject.toml", "requirements-lock.txt", "test/fixtures/market/orchestration-manifest.json")]
    market = [p for p in (root / "test/fixtures/market").glob("*.csv") if p.is_file()]
    if any(not g for g in groups + [market]) or not all(p.is_file() for p in required):
        raise FileNotFoundError(f"required runtime source files missing under {root}")
    return sorted([p for g in groups + [market] for p in g] + required, key=lambda p: p.relative_to(root).as_posix())


def source_fingerprint(root: Path) -> str:
    """SHA-256 of sorted relative runtime filenames plus contents."""
    root = Path(root).resolve()
    digest = hashlib.sha256()
    for path in _source_paths(root):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return "sha256:" + digest.hexdigest()


def _json(path: Path, label: str, failures: list[str]) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{label}: cannot read {Path(path).name}: {exc}")
        return None


def _num(value: Any) -> TypeGuard[int | float]:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _provenance(rec: Any, current: str | None, label: str, kind: str, failures: list[str]) -> None:
    if not isinstance(rec, dict):
        failures.append(f"{label}: {kind} provenance is not an object")
        return
    if current is None or rec.get("source_fingerprint") != current:
        failures.append(f"{label}: {kind} provenance has a stale or incorrect source fingerprint")
    for key, expected in (("model", DEFAULT_MODEL), ("provider", DEFAULT_PROVIDER)):
        if rec.get(key) != expected:
            failures.append(f"{label}: {kind} provenance {key} {rec.get(key)!r} != {expected!r}")


def _summary(summary: dict[str, Any], ticker: str, mode: str, label: str, failures: list[str]) -> None:
    for key, expected in (("ticker", ticker), ("context_mode", mode), ("outcome", "completed"), ("pack_complete", True)):
        got = summary.get(key)
        if (str(got).upper() if key == "ticker" else got) != expected:
            failures.append(f"{label}: summary {key} mismatch")
    if summary.get("error") not in (None, "", False):
        failures.append(f"{label}: summary records an error")
    calls = summary.get("calls")
    input_tokens = summary.get("input_tokens")
    output_tokens = summary.get("output_tokens")
    total_tokens = summary.get("total_tokens")
    if (
        not _num(calls)
        or not _num(input_tokens)
        or not _num(output_tokens)
        or not _num(total_tokens)
        or calls <= 0
        or input_tokens <= 0
        or output_tokens <= 0
        or total_tokens <= 0
        or total_tokens != input_tokens + output_tokens
    ):
        failures.append(f"{label}: usage is not positive or total_tokens != input + output")
    if not _num(summary.get("wall_seconds")) or summary["wall_seconds"] < 0:
        failures.append(f"{label}: wall_seconds is missing or negative")


def _pack(pack: Any, summary: dict[str, Any], ticker: str, mode: str, case: dict, label: str, failures: list[str]) -> dict[str, dict[str, Any]]:
    if not pack.complete or pack.manifest.outcome != "completed":
        failures.append(f"{label}: saved actual pack is incomplete or not completed")
    if str(pack.manifest.ticker).upper() != ticker or pack.manifest.context_mode != mode:
        failures.append(f"{label}: saved actual pack identity/mode mismatch")
    usage = pack.usage
    values = {k: getattr(usage, k) for k in ("calls", "input_tokens", "output_tokens", "total_tokens")}
    if any(not _num(v) or v <= 0 for v in values.values()) or usage.total_tokens != usage.input_tokens + usage.output_tokens:
        failures.append(f"{label}: saved pack usage is not positive or total_tokens != input + output")
    for key, value in values.items():
        if summary.get(key) != value:
            failures.append(f"{label}: summary {key} does not match the saved actual pack")
    try:
        from .live import _deterministic_checks
        return {c["check"]: c for c in _deterministic_checks(case, pack, ticker) if isinstance(c, dict) and isinstance(c.get("check"), str)}
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{label}: cannot recompute checks from saved actual pack: {exc}")
        return {}


def _judge(judge: dict[str, Any], recomputed: dict[str, dict[str, Any]], label: str, failures: list[str]) -> None:
    for key, expected, message in (("error", False, "judge error is not false"), ("semantic_valid", True, "semantic_valid is not true")):
        if judge.get(key) is not expected:
            failures.append(f"{label}: {message}")
    for key, minimum in (("support", MIN_SUPPORT), ("relevance", MIN_RELEVANCE), ("valid_citation_rate", MIN_CITATION)):
        if not _num(judge.get(key)) or judge[key] < minimum:
            failures.append(f"{label}: {key} below {minimum}")
    if judge.get("semantic_errors") != []:
        failures.append(f"{label}: semantic_errors is not empty")
    saved = {c["check"]: c for c in (judge.get("deterministic_checks") or []) if isinstance(c, dict) and isinstance(c.get("check"), str)}
    for name in MANDATORY:
        saved_check = saved.get(name)
        if saved_check is None:
            failures.append(f"{label}: mandatory deterministic check missing: {name}")
        elif saved_check.get("passed") is not True:
            failures.append(f"{label}: deterministic check failed: {name}")
        if recomputed and (recomputed.get(name) is None or recomputed[name].get("passed") is not True):
            failures.append(f"{label}: recomputed pack check failed: {name}")
        elif recomputed and saved_check is not None and saved_check.get("passed") != recomputed[name].get("passed"):
            failures.append(f"{label}: saved check disagrees with saved actual pack: {name}")


def validate_release(root: Path, evidence_dir: Path) -> dict[str, Any]:
    """Validate current-source release evidence; returns failures and metrics."""
    root = Path(root).resolve()
    evidence = Path(evidence_dir)
    if not evidence.is_absolute():
        evidence = root / evidence
    failures: list[str] = []
    checks: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, Any] = {"cases": {}}
    try:
        current: str | None = source_fingerprint(root)
        checks.append(f"RELEASE_SOURCE_FINGERPRINT={current}")
    except Exception as exc:  # noqa: BLE001
        current = None
        failures.append(f"source fingerprint unavailable: {exc}")
    from .case_registry import all_cases
    cases = {c["ticker"].upper(): c for c in all_cases()}
    expected = set(cases)
    if not evidence.is_dir():
        failures.append(f"release evidence directory missing: {evidence}")
        return {"failures": failures, "checks": checks, "warnings": warnings, "metrics": metrics}
    present = {p.name.upper() for p in evidence.iterdir() if p.is_dir() and p.name not in {"judge", "aggregate"}}
    for ticker in sorted(expected - present):
        failures.append(f"missing expected case: {ticker}")
    for ticker in sorted(present - expected):
        failures.append(f"unexpected case identity: {ticker}")
    checks.append(f"RELEASE_CASES={len(expected)}")
    arms: dict[str, dict[str, Any]] = {}
    for ticker, case in cases.items():
        arms[ticker] = {}
        for mode in MODES:
            label = f"{ticker}/{mode}"
            arm = evidence / ticker / mode
            if not arm.is_dir():
                failures.append(f"{label}: arm missing")
                continue
            summary = _json(arm / "summary.json", label, failures)
            config = _json(arm / "config.json", label, failures)
            prov = _json(arm / PROVENANCE, label, failures)
            judge = _json(evidence / "judge" / ticker / mode / "judge.json", label, failures)
            jprov = _json(evidence / "judge" / ticker / mode / PROVENANCE, label, failures)
            if not all(isinstance(x, dict) for x in (summary, config, prov, judge, jprov)):
                continue
            _provenance(prov, current, label, "run", failures)
            _provenance(jprov, current, label, "judge", failures)
            _summary(summary, ticker, mode, label, failures)
            for key, expected_value in (("llm_provider", prov.get("provider")), ("quick_think_llm", prov.get("model")), ("deep_think_llm", prov.get("model"))):
                if not config.get(key) or config.get(key) != expected_value:
                    failures.append(f"{label}: config {key} != run provenance")
            if any(config.get(k) != DEFAULT_MODEL for k in ("quick_think_llm", "deep_think_llm")):
                failures.append(f"{label}: config model is not current {DEFAULT_MODEL!r}")
            recomputed: dict[str, dict[str, Any]] = {}
            try:
                from ..evidence import EvidencePackIO
                pack = EvidencePackIO().import_pack(arm / "run")
                recomputed = _pack(pack, summary, ticker, mode, case, label, failures)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{label}: saved actual pack cannot be loaded: {exc}")
            _judge(judge, recomputed, label, failures)
            arms[ticker][mode] = {"summary": summary, "config": config, "prov": prov, "judge": judge, "jprov": jprov}
        baseline = arms[ticker].get("baseline")
        compact = arms[ticker].get("compact")
        if not baseline or not compact:
            continue
        run_pair = (baseline["prov"].get("model"), baseline["prov"].get("provider"))
        if run_pair != (compact["prov"].get("model"), compact["prov"].get("provider")):
            failures.append(f"{ticker}: run model/provider differ across arms")
        if {k: baseline["config"].get(k) for k in SETTINGS} != {k: compact["config"].get(k) for k in SETTINGS}:
            failures.append(f"{ticker}: settings differ across arms")
        if (baseline["jprov"].get("model"), baseline["jprov"].get("provider")) != (compact["jprov"].get("model"), compact["jprov"].get("provider")):
            failures.append(f"{ticker}: judge model/provider differ across arms")
        if run_pair != (baseline["jprov"].get("model"), baseline["jprov"].get("provider")):
            failures.append(f"{ticker}: judge provenance does not match run provenance")
        metrics["cases"][ticker] = {
            "baseline_tokens": baseline["summary"].get("total_tokens"),
            "compact_tokens": compact["summary"].get("total_tokens"),
            "baseline_wall_seconds": baseline["summary"].get("wall_seconds"),
            "compact_wall_seconds": compact["summary"].get("wall_seconds"),
            "baseline_support": baseline["judge"].get("support"),
            "compact_support": compact["judge"].get("support"),
            "baseline_relevance": baseline["judge"].get("relevance"),
            "compact_relevance": compact["judge"].get("relevance"),
        }
    paired = [
        m
        for m in metrics["cases"].values()
        if None not in (
            m["baseline_tokens"],
            m["compact_tokens"],
            m["baseline_wall_seconds"],
            m["compact_wall_seconds"],
            m["baseline_support"],
            m["compact_support"],
            m["baseline_relevance"],
            m["compact_relevance"],
        )
    ]
    if paired:
        bt, ct, bw, cw = (
            sum(m[k] for m in paired)
            for k in (
                "baseline_tokens",
                "compact_tokens",
                "baseline_wall_seconds",
                "compact_wall_seconds",
            )
        )
        reduction = 1 - ct / bt if bt > 0 else None
        ratio = cw / bw if bw > 0 else None
        mean_support_baseline = sum(m["baseline_support"] for m in paired) / len(paired)
        mean_support_compact = sum(m["compact_support"] for m in paired) / len(paired)
        support_drop = mean_support_baseline - mean_support_compact
        mean_relevance_baseline = sum(m["baseline_relevance"] for m in paired) / len(paired)
        mean_relevance_compact = sum(m["compact_relevance"] for m in paired) / len(paired)
        relevance_drop = mean_relevance_baseline - mean_relevance_compact
        metrics["aggregate"] = {
            "token_reduction": reduction,
            "mean_support_baseline": mean_support_baseline,
            "mean_support_compact": mean_support_compact,
            "mean_support_drop": support_drop,
            "mean_relevance_baseline": mean_relevance_baseline,
            "mean_relevance_compact": mean_relevance_compact,
            "mean_relevance_drop": relevance_drop,
            "wall_ratio": ratio,
        }
        metrics["should_targets"] = {
            "token_reduction": {
                "value": reduction,
                "target": f">={COST_MIN}",
                "passed": reduction is not None and reduction >= COST_MIN,
            },
            "mean_support_drop": {
                "value": support_drop,
                "target": f"<={QUALITY_DROP_MAX}",
                "passed": support_drop <= QUALITY_DROP_MAX,
            },
            "mean_relevance_drop": {
                "value": relevance_drop,
                "target": f"<={QUALITY_DROP_MAX}",
                "passed": relevance_drop <= QUALITY_DROP_MAX,
            },
            "wall_ratio": {
                "value": ratio,
                "target": f"<={WALL_MAX}",
                "passed": ratio is not None and ratio <= WALL_MAX,
            },
        }
        for name, target in metrics["should_targets"].items():
            status = "PASS" if target["passed"] else "FAIL"
            checks.append(
                f"RELEASE_SHOULD {name}={target['value']} target {target['target']} {status}"
            )
            if not target["passed"] and name not in ("mean_support_drop", "mean_relevance_drop"):
                warnings.append(
                    f"Should target missed: {name}={target['value']} target {target['target']}"
                )
        if support_drop > QUALITY_DROP_MAX:
            failures.append(
                f"quality retention failed: mean support drop {support_drop:.4f} > {QUALITY_DROP_MAX}"
            )
        if relevance_drop > QUALITY_DROP_MAX:
            failures.append(
                f"quality retention failed: mean relevance drop {relevance_drop:.4f} > {QUALITY_DROP_MAX}"
            )
    return {"failures": failures, "checks": checks, "warnings": warnings, "metrics": metrics, "source_fingerprint": current}
