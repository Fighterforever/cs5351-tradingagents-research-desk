"""AT-08: one reproducible expected-rejection demonstration per CI gate.

This is NOT six product checks. It deliberately violates each of the six real
CI gates and requires the intended rejection to occur for its named reason.
Each case invokes the actual gate CLI (``scripts/check_*.py``) against either
the real project or a temporary isolated root; no application source, existing
test, document, fixture, workflow or permission file is modified. All temporary
roots are created under a system temp dir and removed on exit.

Exit is 0 only when all six intended rejections are observed; otherwise 1. With
``--output PATH`` a machine-readable JSON report is written. No environment
variables or credentials are logged.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from _gate_lib import project_root

PROJECT = project_root()
VENV_PY = sys.executable
TIMEOUT_SECONDS = 600

# (gate id, named expected-rejection message).
EXPECTED = (
    ("gate1_temporal_order", "approval must predate implementation start"),
    ("gate2_safety_path_without_decision", "requires an ADR accepted by leo"),
    ("gate3_requirements_fit_missing", "fit.metric is empty"),
    ("gate4_missing_fixed_pack", "required fixed pack missing: aapl_buy_complete"),
    ("gate5_regression_pytest_failure", "regression suite failed: tests"),
    ("gate6_ai_log_not_updated", "was not updated in this change"),
)


def _base_env() -> dict:
    env = dict(os.environ)
    env["PATH"] = str(Path(VENV_PY).parent) + os.pathsep + env.get("PATH", "")
    return env


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True,
            env=_base_env(), timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, 124, stdout="", stderr="timed out")


def _link(tmp: Path, rel: str, real: Path) -> None:
    """Symlink a real (read-only) project path into the temp root."""
    target = tmp / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() and not target.is_symlink():
        target.symlink_to(real)


# ---------------------------------------------------------------------------
# Examples (each returns a CompletedProcess for one gate CLI invocation)
# ---------------------------------------------------------------------------


def _example_gate1() -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix="gate1-") as td:
        tmp = Path(td)
        proc_dir = tmp / "docs/process"
        proc_dir.mkdir(parents=True, exist_ok=True)
        data = yaml.safe_load((PROJECT / "docs/process/test-approval.yaml").read_text(encoding="utf-8"))
        start = datetime.fromisoformat(data["implementation_started_at"])
        data["approved_at"] = (start + timedelta(seconds=1)).isoformat()  # approval after start
        (proc_dir / "test-approval.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
        )
        for name in ("PROJECT_PLAN.md", "TEST_PLAN.md", "APPROVAL_PACKET.md"):
            _link(tmp, f"docs/process/{name}", PROJECT / "docs/process" / name)
        _link(tmp, "transcripts", PROJECT / "transcripts")
        return _run(
            [
                VENV_PY, "scripts/check_approval.py",
                "--root", str(tmp),
                "--changed-files", "docs/process/test-approval.yaml",
            ],
            PROJECT,
        )


def _example_gate2() -> subprocess.CompletedProcess:
    return _run(
        [VENV_PY, "scripts/check_static.py", "--changed-files", "src/research_desk/policy.py"],
        PROJECT,
    )


def _example_gate3() -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix="gate3-") as td:
        tmp = Path(td)
        req_dir = tmp / "docs/req"
        req_dir.mkdir(parents=True, exist_ok=True)
        data = yaml.safe_load((PROJECT / "docs/req/requirements.yaml").read_text(encoding="utf-8"))
        data["requirements"][0]["fit"].pop("metric", None)
        (req_dir / "requirements.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
        )
        _link(tmp, "docs/req/req-schema.json", PROJECT / "docs/req/req-schema.json")
        _link(tmp, "docs/process", PROJECT / "docs/process")
        _link(tmp, "docs/architecture", PROJECT / "docs/architecture")
        for rel in ("src", "scripts", "test", "tests", "tradingagents", ".github"):
            _link(tmp, rel, PROJECT / rel)
        return _run([VENV_PY, "scripts/check_requirements.py", "--root", str(tmp)], PROJECT)


def _example_gate4() -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix="gate4-") as td:
        tmp = Path(td)
        packs = tmp / "test/fixtures/packs"
        packs.mkdir(parents=True, exist_ok=True)
        src_packs = PROJECT / "test/fixtures/packs"
        for name in ("msft_review", "tsla_hold", "nvda_compact_memory"):
            shutil.copytree(src_packs / name, packs / name)  # omit aapl_buy_complete
        _link(tmp, "src", PROJECT / "src")
        return _run(
            [
                VENV_PY, "scripts/check_semantic.py",
                "--root", str(tmp), "--packs-dir", "test/fixtures/packs",
                "--changed-files", "docs/ci-gates.md",  # temp root has no .git
            ],
            PROJECT,
        )


def _example_gate5() -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix="gate5-") as td:
        tmp = Path(td)
        (tmp / "tests").mkdir(parents=True, exist_ok=True)
        (tmp / "tests/test_expected_failure.py").write_text(
            "def test_expected_failure():\n    assert 1 == 2\n", encoding="utf-8"
        )
        (tmp / "test/offline").mkdir(parents=True, exist_ok=True)
        (tmp / "test/offline/test_ok.py").write_text(
            "def test_ok():\n    assert True\n", encoding="utf-8"
        )
        return _run(
            [VENV_PY, "scripts/check_regression.py", "--root", str(tmp)], PROJECT
        )


def _example_gate6() -> subprocess.CompletedProcess:
    return _run(
        [VENV_PY, "scripts/check_ai_use_log.py", "--changed-files", "scripts/check_ai_use_log.py"],
        PROJECT,
    )


_EXAMPLES = {
    "gate1_temporal_order": _example_gate1,
    "gate2_safety_path_without_decision": _example_gate2,
    "gate3_requirements_fit_missing": _example_gate3,
    "gate4_missing_fixed_pack": _example_gate4,
    "gate5_regression_pytest_failure": _example_gate5,
    "gate6_ai_log_not_updated": _example_gate6,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AT-08: expected-rejection demonstration (one per gate)."
    )
    parser.add_argument("--output", default=None, help="Write a machine-readable JSON report here.")
    args = parser.parse_args()

    results = []
    all_ok = True
    for gate_id, expected in EXPECTED:
        proc = _EXAMPLES[gate_id]()
        output = (proc.stdout or "") + (proc.stderr or "")
        matched = expected in output
        ok = proc.returncode != 0 and matched
        all_ok = all_ok and ok
        print(f"[{gate_id}] exit={proc.returncode} expected_rejection={'OK' if ok else 'MISSING'}")
        if not ok:
            print(f"  expected message: {expected!r}")
            tail = "\n".join((proc.stdout or "").strip().splitlines()[-4:])
            if tail:
                print(f"  stdout tail:\n{tail}")
            err_tail = "\n".join((proc.stderr or "").strip().splitlines()[-4:])
            if err_tail:
                print(f"  stderr tail:\n{err_tail}")
        results.append(
            {
                "gate": gate_id,
                "expected_message": expected,
                "exit": proc.returncode,
                "matched": matched,
                "args": list(proc.args),
                "stdout": proc.stdout,
                "stderr": proc.stderr,
            }
        )

    print("\n" + ("ALL_SIX_EXPECTED_REJECTIONS_OK" if all_ok else "DEMONSTRATION_INCOMPLETE"))
    if args.output:
        report = {
            "demonstration": "AT-08 expected-rejection demonstration",
            "all_rejections_observed": all_ok,
            "expected_rejections": results,
        }
        Path(args.output).write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
