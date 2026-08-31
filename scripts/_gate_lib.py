"""Shared helpers for the Research Desk CI gate scripts.

These scripts are CI glue and are intentionally small and free of live-service
dependencies. They only read the repository and run deterministic commands.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def project_root() -> Path:
    """Repo root: this file lives in ``<root>/scripts/``."""
    return Path(__file__).resolve().parent.parent


def resolve_root(root: str | None) -> Path:
    return Path(root).resolve() if root else project_root()


def tool_path(root: Path, name: str) -> str:
    """Prefer the isolated project venv, then the PATH executable."""
    local = root / ".venv" / "bin" / name
    if local.exists():
        return str(local)
    found = shutil.which(name)
    if found:
        return found
    return str(local)


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run a command, capturing output. Exit status is not masked here."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def _git(root: Path, args: list[str]) -> subprocess.CompletedProcess:
    return run(["git", "-C", str(root), *args], root)


def changed_files(
    root: Path,
    base_ref: str | None = None,
    head_ref: str | None = None,
    explicit: str | None = None,
) -> list[str]:
    """Resolve the set of changed file paths for a change gate.

    Priority: an explicit ``--changed-files`` list (enables reproducible
    negative examples without editing the repo), else a git base..head diff,
    else the working-tree changes (modified + staged + untracked) so initial /
    local work is handled honestly rather than pretending nothing changed.

    A git failure raises ``RuntimeError`` so it becomes a gate failure; an
    invalid diff can never silently be treated as "no change".
    """
    if explicit:
        return [f.strip() for f in explicit.split(",") if f.strip()]
    if base_ref:
        cmd = ["diff", "--name-only", base_ref]
        if head_ref:
            cmd.append(head_ref)
        proc = _git(root, cmd)
        if proc.returncode != 0:
            raise RuntimeError(
                f"git diff failed (base={base_ref!r}, head={head_ref!r}): "
                f"{proc.stderr.strip() or proc.stdout.strip()}"
            )
        return [line for line in proc.stdout.splitlines() if line.strip()]
    names: list[str] = []
    for args in (
        ["diff", "--name-only"],
        ["diff", "--cached", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        proc = _git(root, args)
        if proc.returncode != 0:
            raise RuntimeError(
                f"git change enumeration failed ({args!r}): "
                f"{proc.stderr.strip() or proc.stdout.strip()}"
            )
        names.extend(line for line in proc.stdout.splitlines() if line.strip())
    return list(dict.fromkeys(names))


def add_change_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=None, help="Repository root (defaults to project root).")
    parser.add_argument("--base-ref", default=None, help="Base ref for PR change detection.")
    parser.add_argument("--head-ref", default=None, help="Head ref for PR change detection.")
    parser.add_argument(
        "--changed-files",
        default=None,
        help="Comma-separated explicit changed file list (negative-test override).",
    )


def fail(checks: list[str], failures: list[str]) -> None:
    """Print a consolidated gate result and exit nonzero if any check failed."""
    for line in checks:
        print(line)
    print("RESULT: FAIL" if failures else "RESULT: PASS")
    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    sys.exit(0)
