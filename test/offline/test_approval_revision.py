"""Focused revision-approval checks for ``scripts/check_approval.py``.

These are isolated unit cases over the revision block validator: one missing
evidence artifact and one approval recorded after the earliest edit/write event.
They do not read or modify the real approval record.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_approval.py"


def _load_check_approval():
    sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location("check_approval_revision_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_CHECK_APPROVAL = _load_check_approval()


def _write(path: Path, text: str = "evidence") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _revision(*, evidence: str, approved_at: str, started_at: str) -> dict:
    return {
        "decision": "APPROVED",
        "approver": "leo",
        "authorization": "docs/process/revision-authorization.md",
        "architecture_decision": "docs/architecture/adr/004-release-quality-and-context-budget.md",
        "tests": ["AT-04 rejection terminal-state unit cases"],
        "scope": "User-requested completion revision",
        "approved_at": approved_at,
        "implementation_started_at": started_at,
        "evidence": evidence,
    }


def _write_supporting_docs(root: Path) -> None:
    _write(root / "docs/process/revision-authorization.md", "Decision: APPROVED")
    _write(
        root / "docs/architecture/adr/004-release-quality-and-context-budget.md",
        "Status: accepted by leo",
    )


def test_revision_missing_evidence_artifact_fails(tmp_path):
    _write_supporting_docs(tmp_path)
    started = datetime(2026, 11, 9, 14, 22, 11, 409000, tzinfo=timezone.utc)
    approved = started - timedelta(minutes=8)
    revision = _revision(
        evidence="transcripts/missing-revision.raw.jsonl",
        approved_at=approved.isoformat(),
        started_at=started.isoformat(),
    )

    failures = _CHECK_APPROVAL._validate_revision(tmp_path, {"revision": revision})

    assert any(
        "revision evidence artifact does not exist" in failure for failure in failures
    )


def test_revision_late_approval_fails_against_earliest_edit(tmp_path):
    _write_supporting_docs(tmp_path)
    edit_ms = 1_800_000_000_000
    started = datetime.fromtimestamp(edit_ms / 1000, tz=timezone.utc)
    approved = started + timedelta(minutes=1)
    evidence = tmp_path / "transcripts/revision-late.raw.jsonl"
    _write(
        evidence,
        json.dumps(
            {
                "type": "tool_use",
                "timestamp": edit_ms,
                "part": {"tool": "edit", "state": {"status": "completed"}},
            }
        )
        + "\n",
    )
    revision = _revision(
        evidence="transcripts/revision-late.raw.jsonl",
        approved_at=approved.isoformat(),
        started_at=started.isoformat(),
    )

    failures = _CHECK_APPROVAL._validate_revision(tmp_path, {"revision": revision})

    assert any(
        "revision approval must predate implementation start" in failure
        for failure in failures
    )
    assert any(
        "revision implementation edit predates recorded approval" in failure
        for failure in failures
    )
