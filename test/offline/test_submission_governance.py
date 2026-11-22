import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from check_ai_use_log import validate_entries  # noqa: E402
from check_approval import validate_change_approvals  # noqa: E402


def _git(root, *args, env=None):
    subprocess.run(["git", *args], cwd=root, check=True,
                   env=env or os.environ.copy(), capture_output=True, text=True)


def _init_repo(root):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    _git(root, "init", "-q", env=env)
    _git(root, "config", "user.name", "t", env=env)
    _git(root, "config", "user.email", "t@t", env=env)
    return env


def _commit(env, root, when, msg):
    e = {**env, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
    _git(root, "add", "-A", env=e)
    _git(root, "commit", "-q", "-m", msg, env=e)


def _entry(**over):
    entry = {
        "id": "accept",
        "authority": "project owner",
        "decision": "APPROVED",
        "approved_at": "2021-01-01T00:00:00+00:00",
        "scope": ["src/app.py"],
        "tests": ["tests/test_app.py"],
        "evidence": "docs/approval.md",
    }
    entry.update(over)
    return entry


@pytest.mark.parametrize("case", ["valid", "stale", "uncovered", "late", "empty-tests"])
def test_change_approvals(tmp_path, case):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "tests").mkdir()
    (root / "docs").mkdir()
    (root / "docs" / "process").mkdir()
    (root / "tests" / "test_app.py").write_text("def test_x():\n    assert True\n")
    (root / "docs" / "approval.md").write_text("# Approval\n")

    base_entry = _entry()
    if case == "stale":
        base_entry = _entry(id="accept")
    data = {"change_approvals": [base_entry] if case == "stale" else []}
    (root / "docs" / "process" / "test-approval.yaml").write_text(
        yaml.safe_dump(data))

    env = _init_repo(root)
    _commit(env, root, "2021-01-02T00:00:00+00:00", "base")

    entry = _entry()
    if case == "uncovered":
        entry = _entry(scope=["src/other.py"])
    if case == "late":
        entry = _entry(approved_at="2021-01-03T00:00:00+00:00")
    if case == "empty-tests":
        entry = _entry(tests=[])
    (root / "docs" / "process" / "test-approval.yaml").write_text(
        yaml.safe_dump({"change_approvals": [entry]}))

    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("x = 1\n")
    _commit(env, root, "2021-01-02T00:00:00+00:00", "code")

    data = yaml.safe_load((root / "docs" / "process" / "test-approval.yaml").read_text())
    changed = ["src/app.py"]
    errors = validate_change_approvals(
        root, data, changed, "HEAD~1", "HEAD")
    if case == "valid":
        assert errors == []
    else:
        assert errors


@pytest.mark.parametrize("case", ["valid", "duplicate", "missing-evidence"])
def test_ai_use_log(tmp_path, case):
    root = tmp_path / "repo"
    root.mkdir()
    for name in ("review.md", "prompt.md", "session.json"):
        (root / name).write_text("x")

    entry = {
        "date": "2021-01-01",
        "tool": "OpenCode CLI",
        "model": "DeepSeek",
        "purpose": "implement feature",
        "scope": ["src/app.py"],
        "review": "review.md",
        "outcome": "accepted",
        "session": "ses_test",
        "prompt": "prompt.md",
        "evidence": "session.json",
    }
    previous = [dict(entry)] if case == "duplicate" else []
    if case == "missing-evidence":
        entry = dict(entry, evidence="absent.json")

    errors = validate_entries(root, [entry], previous, ["src/app.py"])
    if case == "valid":
        assert errors == []
    else:
        assert errors
