"""Gate 5: full regression.

Runs both the original upstream ``tests`` suite and the new ``test/offline``
suite. Live API tests are excluded via the registered ``live`` marker. A silent
pass or continue-on-error is not permitted: any non-zero exit fails the gate.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _gate_lib import add_change_args, fail, resolve_root, run, tool_path

TARGETS = ("tests", "test/offline")
EXCLUDE_MARKER = "live"


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 5: full regression.")
    add_change_args(parser)
    args = parser.parse_args()

    root: Path = resolve_root(args.root)
    checks: list[str] = []
    failures: list[str] = []

    py = tool_path(root, "python") or "python"
    for target in TARGETS:
        cmd = [py, "-m", "pytest", "-q", "-m", f"not {EXCLUDE_MARKER}", target]
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
