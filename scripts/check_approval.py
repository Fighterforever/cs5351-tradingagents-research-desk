"""Gate 1 retains original AT-01 through AT-08 and revision records, requiring fresh
scoped approvals for changed execution files in the current Git comparison. It checks
written test and evidence files and compares approval time against the first matching
implementation commit.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml
from _gate_lib import (
    add_change_args,
    changed_files,
    fail,
    first_change_time,
    read_base_text,
    resolve_root,
)

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

REVISION_KEYS = (
    "decision",
    "approver",
    "authorization",
    "architecture_decision",
    "tests",
    "scope",
    "approved_at",
    "implementation_started_at",
    "evidence",
)
EDIT_WRITE_TOOLS = ("edit", "write")
IMPLEMENTATION_START_TOLERANCE_SECONDS = 1.0


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


def _earliest_edit_write_event(path: Path) -> datetime | None:
    """Earliest ``edit``/``write`` tool event in a raw JSONL transcript."""
    earliest: datetime | None = None
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "tool_use":
            continue
        part = event.get("part")
        if not isinstance(part, dict) or part.get("tool") not in EDIT_WRITE_TOOLS:
            continue
        timestamp = event.get("timestamp")
        if not isinstance(timestamp, (int, float)):
            continue
        event_at = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        if earliest is None or event_at < earliest:
            earliest = event_at
    return earliest


def _validate_revision(root: Path, data: dict) -> list[str]:
    """Validate the optional revision approval block against its raw evidence."""
    revision = data.get("revision")
    if revision is None:
        return []  # the original historical approval record stays valid
    failures: list[str] = []
    if not isinstance(revision, dict):
        return ["revision must be a YAML mapping"]

    for key in REVISION_KEYS:
        if key not in revision:
            failures.append(f"revision missing required key: {key}")

    if revision.get("decision") != "APPROVED":
        failures.append(
            f"revision decision must be APPROVED, got {revision.get('decision')!r}"
        )
    if revision.get("approver") != APPROVER:
        failures.append(
            f"revision approver must be {APPROVER!r}, got {revision.get('approver')!r}"
        )

    approved_at: datetime | None = None
    implemented_at: datetime | None = None
    try:
        approved_at = _parse_iso(revision["approved_at"])
        implemented_at = _parse_iso(revision["implementation_started_at"])
        if not (approved_at < implemented_at):
            failures.append(
                "revision approval must predate implementation start: "
                f"approved_at={approved_at.isoformat()} !< "
                f"implementation_started_at={implemented_at.isoformat()}"
            )
    except KeyError:
        failures.append("revision timestamps are missing")
    except ValueError as exc:
        failures.append(f"revision timestamp parse error: {exc}")

    for name in ("authorization", "architecture_decision", "evidence"):
        ref = revision.get(name)
        if not isinstance(ref, str) or not ref:
            failures.append(f"revision {name} reference is empty")
            continue
        if not (root / ref).exists():
            failures.append(f"revision {name} artifact does not exist: {ref}")

    if not revision.get("scope"):
        failures.append("revision scope is empty")
    tests = revision.get("tests")
    if not isinstance(tests, list) or not tests:
        failures.append("revision tests must be a non-empty list")
    else:
        for test in tests:
            if not isinstance(test, str) or not test.strip():
                failures.append(f"revision test entry is malformed: {test!r}")

    evidence_ref = revision.get("evidence")
    if isinstance(evidence_ref, str) and evidence_ref and (root / evidence_ref).exists():
        earliest = _earliest_edit_write_event(root / evidence_ref)
        if earliest is None:
            failures.append(
                f"revision evidence has no edit/write tool event: {evidence_ref}"
            )
        else:
            if approved_at is not None and earliest < approved_at:
                failures.append(
                    "revision implementation edit predates recorded approval: "
                    f"earliest_edit={earliest.isoformat()} < "
                    f"approved_at={approved_at.isoformat()}"
                )
            if implemented_at is not None:
                delta = abs((earliest - implemented_at).total_seconds())
                if delta > IMPLEMENTATION_START_TOLERANCE_SECONDS:
                    failures.append(
                        "revision earliest edit/write does not match declared "
                        "implementation start: "
                        f"earliest_edit={earliest.isoformat()} vs "
                        f"implementation_started_at={implemented_at.isoformat()}"
                    )
    return failures


def governed_path(path: str) -> bool:
    return (path in {'Prompt.md', 'pyproject.toml', 'opencode.json', '.opencode/permissions.jsonc'}
            or path.startswith(('.github/workflows/', 'prompts/'))
            or (path.endswith('.py') and ('/' not in path or path.startswith(('src/', 'cli/', 'tradingagents/', 'scripts/', 'test/', 'tests/')))))


def _safe_relpath(root, value):
    if not isinstance(value, str) or not value:
        return None
    p = Path(value)
    if p.is_absolute() or '..' in p.parts or p == Path('.'):
        return None
    r = (Path(root) / p).resolve()
    root = Path(root).resolve()
    return r if r != root and root in r.parents else None


def _entry_covers(scope: list[str], change: str) -> bool:
    for entry in scope:
        if not isinstance(entry, str):
            continue
        entry = entry.rstrip("/")
        if not entry:
            continue
        if entry == change or change.startswith(entry + "/"):
            return True
    return False


def validate_change_approvals(root, data, changed, base_ref, head_ref):
    governed = [path for path in changed if governed_path(path)]
    if not governed:
        return []

    base = base_ref or 'HEAD'
    baseline_text = read_base_text(root, base, APPROVAL_DOC)
    old = yaml.safe_load(baseline_text) if baseline_text is not None else {}
    if not isinstance(old, dict):
        return ['approval document must be a mapping']

    old_rows = old.get('change_approvals', [])
    if not isinstance(old_rows, list):
        return ['change_approvals must be a list']

    errors = []
    previous_ids = set()
    for row in old_rows:
        if not isinstance(row, dict):
            errors.append('previous change_approvals entry must be a mapping')
            continue
        old_id = row.get('id')
        if isinstance(old_id, str) and old_id:
            previous_ids.add(old_id)

    current = data.get('change_approvals', [])
    if not isinstance(current, list):
        return ['change_approvals must be a list']

    covered = set()
    current_ids = set()
    for row in current:
        if not isinstance(row, dict):
            errors.append('change_approvals entry must be a mapping')
            continue
        row_id = row.get('id')
        if not isinstance(row_id, str) or not row_id:
            errors.append('change_approvals entry requires a nonempty string id')
            continue
        if row_id in previous_ids:
            continue
        if row_id in current_ids:
            errors.append(f'duplicate change_approvals id {row_id!r}')
            continue
        current_ids.add(row_id)

        if not isinstance(row.get('authority'), str) or not row['authority'].strip():
            errors.append(f'{row_id}: authority must be a nonempty string')
        if row.get('decision') != 'APPROVED':
            errors.append(f'{row_id}: decision must be APPROVED')

        tests = row.get('tests')
        if not isinstance(tests, list) or not tests:
            errors.append(f'{row_id}: tests must be a nonempty list')
        else:
            for case in tests:
                if not isinstance(case, str):
                    errors.append(f'{row_id}: test case must be a string')
                    continue
                test_path = case.split('::', 1)[0]
                resolved = _safe_relpath(root, test_path)
                if resolved is None or not resolved.is_file():
                    errors.append(f'{row_id}: test path {test_path!r} is not a file')

        evidence = row.get('evidence')
        if evidence is None:
            errors.append(f'{row_id}: evidence is required')
        else:
            resolved = _safe_relpath(root, evidence)
            if resolved is None or not resolved.is_file():
                errors.append(f'{row_id}: evidence path {evidence!r} is not a file')

        scope = row.get('scope')
        if not isinstance(scope, list) or not scope:
            errors.append(f'{row_id}: scope must be a nonempty list')
            scope = []
        else:
            for entry in scope:
                if not isinstance(entry, str) or not entry.strip():
                    errors.append(f'{row_id}: scope entry must be a nonempty string')
                elif _safe_relpath(root, entry.rstrip('/')) is None:
                    errors.append(f'{row_id}: scope entry {entry!r} is not repo-relative')

        matched = [path for path in governed if _entry_covers(scope, path)]

        approved_at = row.get('approved_at')
        approved = None
        if isinstance(approved_at, str):
            try:
                approved = datetime.fromisoformat(approved_at)
            except ValueError:
                errors.append(f'{row_id}: approved_at is not a valid ISO timestamp')
        elif isinstance(approved_at, datetime):
            approved = approved_at
        else:
            errors.append(f'{row_id}: approved_at is required')

        if approved is not None:
            if approved.tzinfo is None:
                errors.append(f'{row_id}: approved_at must include a timezone')
            else:
                if approved > datetime.now(timezone.utc):
                    errors.append(f'{row_id}: approved_at must not be in the future')
                if matched:
                    first = first_change_time(root, base, head_ref, matched)
                    if first is not None and approved >= first:
                        errors.append(f'{row_id}: approval must predate implementation commit')
                        continue
                covered.update(matched)

    for path in governed:
        if path not in covered:
            errors.append(f'governed path {path!r} is not covered by an approval')

    return errors


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

    if data.get("revision") is not None:
        checks.append("revision approval record present and validated")
        failures.extend(_validate_revision(root, data))

    changed = _resolve_changes(root, args)
    failures.extend(validate_change_approvals(
        root, data, changed, args.base_ref, args.head_ref))
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
                "no test specification or test file changed"
            )

    fail(checks, failures)


if __name__ == "__main__":
    main()
