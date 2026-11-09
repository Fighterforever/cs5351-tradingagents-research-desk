"""Gate 5: full regression.

Runs both the original upstream ``tests`` suite and the new ``test/offline``
suite. Tests marked ``integration``, ``live`` or ``smoke`` are excluded so CI
makes no external-service or runtime model calls. A silent pass or
continue-on-error is not permitted: any non-zero exit fails the gate.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _gate_lib import add_change_args, fail, resolve_root, run, tool_path

TARGETS = ("tests", "test/offline")
EXCLUDE_MARKERS = ("integration", "live", "smoke")
MARKER_EXPRESSION = " and ".join(f"not {marker}" for marker in EXCLUDE_MARKERS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 5: full regression.")
    add_change_args(parser)
    args = parser.parse_args()

    root: Path = resolve_root(args.root)
    checks: list[str] = []
    failures: list[str] = []

    py = tool_path(root, "python") or "python"
    for target in TARGETS:
        cmd = [py, "-m", "pytest", "-q", "-m", MARKER_EXPRESSION, target]
        proc = run(cmd, root)
        tail = "\n".join((proc.stdout or "").splitlines()[-6:])
        summary = _summary_line(proc.stdout)
        checks.append(f"pytest {target} -> exit {proc.returncode} ({summary})")
        if proc.returncode != 0:
            failures.append(f"regression suite failed: {target}")
            failures.append(f"  command: {' '.join(cmd)}")
            failures.append(f"  stderr tail:\n{(proc.stderr or '').strip()}")
            failures.append(f"  stdout tail:\n{tail}")

    fail(checks, failures)


def _summary_line(stdout: str) -> str:
    """Extract the pytest totals line (e.g. '49 passed in 0.77s') from output."""
    for line in reversed((stdout or "").splitlines()):
        stripped = line.strip()
        if stripped and ("passed" in stripped or "failed" in stripped):
            return stripped
    return "no summary line"


if __name__ == "__main__":
    main()
