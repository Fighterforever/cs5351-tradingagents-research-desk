"""Gate 1: tests approved before implementation.

Validates ``docs/process/test-approval.yaml`` as real approval evidence rather
than a bare APPROVED word: the identified approver, timezone-aware temporal
ordering (approval must precede implementation start), the referenced plan /
test-plan / approval-record / evidence artifacts, declared-versus-document
version consistency, and coverage of AT-01 through AT-08.

In PR/base-ref mode, a change to a test specification or test file must update
``docs/process/test-approval.yaml`` in the same change; a source-only fix may
reuse the already-approved tests. Approval of arbitrary new tests is never
inferred from the existence of the old AT identifiers.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

import yaml
from _gate_lib import add_change_args, changed_files, fail, resolve_root

APPROVER = "leo"
REQUIRED_TESTS = {f"AT-{i:02d}" for i in range(1, 9)}
TEST_FILE_PREFIXES = ("test/", "tests/")
TEST_SPEC_DOCS = (
    "docs/process/test-approval.yaml",
    "docs/process/TEST_PLAN.md",
    "docs/req/requirements.yaml",
)
APPROVAL_DOC = "docs/process/test-approval.yaml"
VERSION_RE = re.compile(r"版本\s*[：:]\s*([0-9][0-9.]*[0-9]|[0-9])")

REQUIRED_KEYS = (
    "schema_version",
    "decision",
    "approver",
    "approved_at",
    "implementation_started_at",
    "plan",
    "plan_version",
    "test_plan",
    "test_plan_version",
    "tests",
    "scope",
    "evidence",
    "approval_record",
)


def _parse_iso(value: str) -> datetime:
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError(f"{value!r} is not timezone-aware")
    return dt


def _document_version(path: Path) -> str | None:
    """Extract the version declared on a referenced document (e.g. 版本：1.0.0)."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = VERSION_RE.search(text)
    return m.group(1) if m else None


def _resolve_changes(root: Path, args) -> list[str]:
    try:
        return changed_files(root, args.base_ref, args.head_ref, args.changed_files)
    except RuntimeError as exc:
        fail([], [f"could not resolve changed files: {exc}"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 1: tests approved before implementation.")
    add_change_args(parser)
    args = parser.parse_args()

    root: Path = resolve_root(args.root)
    approval_file = root / "docs/process/test-approval.yaml"
    checks: list[str] = []
    failures: list[str] = []

    if not approval_file.exists():
        fail(checks, [f"missing approval record: {approval_file}"])

    data = yaml.safe_load(approval_file.read_text(encoding="utf-8"))
    checks.append(f"read {approval_file}")

    if not isinstance(data, dict):
        fail(checks, ["test-approval.yaml is not a YAML mapping"])

    for key in REQUIRED_KEYS:
        if key not in data:
            failures.append(f"approval record missing required key: {key}")

    if data.get("decision") != "APPROVED":
        failures.append(f"decision must be APPROVED, got {data.get('decision')!r}")

    if data.get("approver") != APPROVER:
        failures.append(
            f"approver must be the identified reviewer {APPROVER!r}, "
            f"got {data.get('approver')!r}"
        )

    try:
        approved_at = _parse_iso(data["approved_at"])
        implemented_at = _parse_iso(data["implementation_started_at"])
        checks.append(f"approved_at={approved_at.isoformat()}")
        checks.append(f"implementation_started_at={implemented_at.isoformat()}")
        if not (approved_at < implemented_at):
            failures.append(
                "approval must predate implementation start: "
                f"approved_at={approved_at.isoformat()} !< "
                f"implementation_started_at={implemented_at.isoformat()}"
            )
    except KeyError:
        failures.append("approval timestamps are missing")
    except ValueError as exc:
        failures.append(f"timestamp parse error: {exc}")

    # Referenced artifacts must exist (plan, test plan, approval record, evidence).
    for name, ref in (
        ("plan", data.get("plan")),
        ("test_plan", data.get("test_plan")),
        ("approval_record", data.get("approval_record")),
        ("evidence", data.get("evidence")),
    ):
        if not isinstance(ref, str) or not ref:
            failures.append(f"{name} reference is empty")
            continue
        p = root / ref
        if not p.exists():
            failures.append(f"{name} artifact does not exist: {ref}")

    # Declared versions must match the versions in the referenced documents.
    for name, ref, declared in (
        ("plan", data.get("plan"), data.get("plan_version")),
        ("test_plan", data.get("test_plan"), data.get("test_plan_version")),
    ):
        if not declared:
            failures.append(f"{name}_version is empty")
            continue
        doc = root / ref if isinstance(ref, str) and ref else None
        if doc is not None and doc.exists():
            doc_version = _document_version(doc)
            checks.append(f"{name}: declared {declared!r}, document {doc_version!r}")
            if doc_version is None:
                failures.append(f"{name}: {ref} does not declare a version")
            elif doc_version != str(declared):
                failures.append(
                    f"{name} version mismatch: approval declares {declared!r} "
                    f"but {ref} declares {doc_version!r}"
                )

    if not data.get("evidence"):
        failures.append("evidence reference is empty")
    if not data.get("scope"):
        failures.append("scope is empty")

    tests = data.get("tests") or []
    if not isinstance(tests, list):
        failures.append("tests must be a list")
        tests = []
    test_set = set(tests)
    checks.append(f"approved tests: {sorted(test_set)}")
    for tid in tests:
        if not isinstance(tid, str) or not tid.startswith("AT-") or len(tid) != 5:
            failures.append(f"malformed test id: {tid!r}")
    missing = REQUIRED_TESTS - test_set
    if missing:
        failures.append(f"approval does not cover all acceptance tests; missing: {sorted(missing)}")

    changed = _resolve_changes(root, args)
    if changed:
        test_change = [
            c for c in changed
            if c.startswith(TEST_FILE_PREFIXES) or c in TEST_SPEC_DOCS
        ]
        if test_change:
            checks.append(f"PR changes test specifications/files: {len(test_change)} file(s)")
            if APPROVAL_DOC not in changed:
                failures.append(
                    "test specification or test file changed without updating "
                    "docs/process/test-approval.yaml in the same change"
                )
            else:
                checks.append("test approval updated in the same change")
        else:
            checks.append(
                "no test specification/file change; existing approved tests may be reused "
                "for this source-only change"
            )

    fail(checks, failures)


if __name__ == "__main__":
    main()
