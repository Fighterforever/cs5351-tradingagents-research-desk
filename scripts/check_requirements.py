"""Gate 3: requirements schema and traceability.

Validates ``docs/req/requirements.yaml`` against ``docs/req/req-schema.json``,
rejects missing/duplicate IDs, unmeasurable fit criteria and broken
source/component/test links, and cross-checks every ID and acceptance test
against the actual trace matrix. Requirement-to-test mapping is validated per
row of the trace matrix, so a test missing from a requirement's own row fails
even if the AT identifier appears elsewhere in prose.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import jsonschema
import yaml
from _gate_lib import add_change_args, fail, resolve_root

FIT_OPERATORS = {"==", "!=", "<", "<=", ">", ">="}
AT_RE = re.compile(r"^AT-(\d{2})$")
TRACE_MATRIX_CANDIDATES = (
    "docs/architecture/trace-matrix.md",
    "docs/architecture/trace-matrix.yaml",
    "docs/architecture/trace-matrix.yml",
    "docs/process/trace-matrix.md",
)


def _at_test_targets(root: Path, at_id: str) -> list[Path] | None:
    """Return the files that must exist for an AT id, or None if malformed."""
    m = AT_RE.match(at_id)
    if not m:
        return None
    n = int(m.group(1))
    if 1 <= n <= 6:
        return sorted((root / "test/offline").glob(f"test_at{n:02d}_*.py"))
    if n == 7:
        return [root / "src/research_desk/eval"]
    if n == 8:
        return sorted((root / "scripts").glob("check_*.py"))
    return None


def _resolve_component(root: Path, comp: str) -> tuple[Path, bool]:
    if comp.startswith("research_desk."):
        p = root / "src" / (comp.replace(".", "/") + ".py")
        return p, p.exists()
    if comp.startswith("tradingagents."):
        p = root / comp.replace(".", "/")
        return p, (p.with_suffix(".py").exists() or p.is_dir())
    if comp == "scripts":
        p = root / "scripts"
        return p, p.is_dir()
    if comp.startswith(".github/"):
        p = root / comp
        return p, p.exists()
    p = root / comp
    return p, p.exists()


def _is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def _matrix_rows(matrix_text: str) -> dict[str, str]:
    """Map requirement id -> concatenated row text (all cells after the id)."""
    rows: dict[str, str] = {}
    for line in matrix_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        rid = cells[0]
        if re.fullmatch(r"[A-Z]+-\d{3}", rid):
            rows[rid] = " ".join(cells[1:])
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 3: requirements schema + traceability.")
    add_change_args(parser)
    args = parser.parse_args()

    root: Path = resolve_root(args.root)
    checks: list[str] = []
    failures: list[str] = []

    schema_path = root / "docs/req/req-schema.json"
    reg_path = root / "docs/req/requirements.yaml"

    if not schema_path.exists():
        fail(checks, [f"missing schema: {schema_path}"])
    if not reg_path.exists():
        fail(checks, [f"missing registry: {reg_path}"])

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    registry = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
    checks.append(f"read {reg_path}")

    if not isinstance(registry, dict):
        fail(checks, ["requirements.yaml is not a YAML mapping"])
    if not isinstance(schema, dict):
        fail(checks, ["req-schema.json is not a JSON object"])

    if "schema_version" not in registry:
        failures.append("registry missing top-level schema_version")
    if "product" not in registry:
        failures.append("registry missing top-level product")
    reqs = registry.get("requirements")
    if not isinstance(reqs, list) or not reqs:
        failures.append("registry requirements must be a non-empty list")
        reqs = []

    try:
        jsonschema.validate(instance=registry, schema=schema)
        checks.append("registry validates against req-schema.json")
    except jsonschema.ValidationError as exc:
        failures.append(f"registry does not match req-schema.json: {exc.message}")

    ids: list[str] = []
    seen: set[str] = set()
    for i, req in enumerate(reqs):
        if not isinstance(req, dict):
            failures.append(f"requirements[{i}] is not a mapping")
            continue
        rid = req.get("id")
        if not isinstance(rid, str):
            failures.append(f"requirements[{i}] missing id")
            continue
        ids.append(rid)
        if rid in seen:
            failures.append(f"duplicate requirement id: {rid}")
        seen.add(rid)

        fit = req.get("fit") or {}
        if not isinstance(fit, dict):
            failures.append(f"{rid}: fit must be a mapping")
        else:
            metric = fit.get("metric")
            operator = fit.get("operator")
            threshold = fit.get("threshold")
            verification = fit.get("verification")
            if not metric:
                failures.append(f"{rid}: fit.metric is empty")
            if operator not in FIT_OPERATORS:
                failures.append(f"{rid}: fit.operator {operator!r} not in {sorted(FIT_OPERATORS)}")
            try:
                float(str(threshold))
            except (TypeError, ValueError):
                failures.append(f"{rid}: fit.threshold {threshold!r} is not numeric")
            if not verification:
                failures.append(f"{rid}: fit.verification is empty")

        for source in req.get("source") or []:
            if not isinstance(source, str) or not source:
                failures.append(f"{rid}: empty source entry")
                continue
            if _is_url(source):
                checks.append(f"{rid}: external source accepted -> {source[:80]}...")
                continue
            sp = root / source
            if not sp.exists():
                failures.append(f"{rid}: source link broken -> {source}")

        for comp in req.get("components") or []:
            _, ok = _resolve_component(root, comp)
            if not ok:
                failures.append(f"{rid}: component link broken -> {comp}")

        for tid in req.get("tests") or []:
            if tid == "upstream-regression":
                if not (root / "tests").is_dir():
                    failures.append(f"{rid}: upstream-regression target tests/ missing")
                continue
            targets = _at_test_targets(root, tid)
            if targets is None:
                failures.append(f"{rid}: malformed test id {tid!r}")
                continue
            if not targets or not any(t.exists() for t in targets):
                failures.append(f"{rid}: test link broken -> {tid} ({targets})")

    matrix_path = None
    for cand in TRACE_MATRIX_CANDIDATES:
        if (root / cand).exists():
            matrix_path = root / cand
            break
    if matrix_path is None:
        failures.append(
            "trace matrix not found (expected docs/architecture/trace-matrix.md); "
            "cannot verify full requirement->test traceability"
        )
    else:
        matrix_text = matrix_path.read_text(encoding="utf-8")
        rows = _matrix_rows(matrix_text)
        checks.append(f"trace matrix rows: {len(rows)}")
        matrix_ids = set(rows.keys())
        missing_from_matrix = sorted(set(ids) - matrix_ids)
        if missing_from_matrix:
            failures.append(f"requirement IDs absent from trace matrix: {missing_from_matrix}")
        extra_in_matrix = sorted(matrix_ids - set(ids))
        if extra_in_matrix:
            failures.append(f"trace matrix lists unknown requirement IDs: {extra_in_matrix}")
        for req in reqs:
            if not isinstance(req, dict):
                continue
            rid = req.get("id")
            row_text = rows.get(rid, "")
            if not row_text:
                continue  # id absence already reported above
            for tid in req.get("tests") or []:
                if str(tid) not in row_text:
                    failures.append(
                        f"{rid}: test {tid} is missing from this requirement's own "
                        "trace-matrix row"
                    )

    checks.append(f"requirement count: {len(reqs)}")
    fail(checks, failures)


if __name__ == "__main__":
    main()
