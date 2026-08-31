"""One local CI evidence runner.

Orchestration convenience that runs the six real gate CLIs plus the AT-08
expected-rejection demonstration sequentially, records evidence for every
invocation, and reports a single boolean success. It does not modify files,
retry, install anything, call APIs, or mask a real failure.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT = SCRIPT_DIR.parent

# Gate CLIs in their numeric order. All accept --base-ref and --head-ref.
GATES = (
    "check_approval.py",
    "check_static.py",
    "check_requirements.py",
    "check_semantic.py",
    "check_regression.py",
    "check_ai_use_log.py",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def invoke(cmd: list[str]) -> dict:
    """Run one command, capturing start/end, elapsed, exit code and output."""
    start = utc_now()
    started = datetime.now(timezone.utc)
    try:
        proc = subprocess.run(
            cmd, cwd=str(PROJECT), capture_output=True, text=True
        )
        error = None
    except Exception as exc:  # process could not start
        proc = None
        error = f"{type(exc).__name__}: {exc}"
    ended = datetime.now(timezone.utc)
    return {
        "command": list(proc.args) if proc is not None else cmd,
        "start_utc": start,
        "end_utc": utc_now(),
        "elapsed_seconds": round((ended - started).total_seconds(), 3),
        "exit_code": proc.returncode if proc is not None else None,
        "error": error,
        "proc": proc,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run all six CI gates plus AT-08.")
    parser.add_argument("--base-ref", required=True, help="Base revision to resolve.")
    parser.add_argument("--head-ref", required=True, help="Head revision to resolve.")
    parser.add_argument(
        "--output-dir", default="evaluation/ci", help="Where to write evidence."
    )
    args = parser.parse_args()

    base_sha = subprocess.run(
        ["git", "-C", str(PROJECT), "rev-parse", "--verify", args.base_ref],
        capture_output=True, text=True,
    )
    head_sha = subprocess.run(
        ["git", "-C", str(PROJECT), "rev-parse", "--verify", args.head_ref],
        capture_output=True, text=True,
    )
    if base_sha.returncode != 0 or head_sha.returncode != 0:
        print("ERROR: could not resolve a supplied ref with git rev-parse")
        print("base stderr:", base_sha.stderr.strip())
        print("head stderr:", head_sha.stderr.strip())
        sys.exit(1)

    resolved = {
        "base_ref": args.base_ref,
        "base_sha": base_sha.stdout.strip(),
        "head_ref": args.head_ref,
        "head_sha": head_sha.stdout.strip(),
    }

    output_dir = PROJECT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    records = []
    all_ok = True

    for gate in GATES:
        cmd = [sys.executable, str(SCRIPT_DIR / gate),
               "--base-ref", resolved["base_sha"],
               "--head-ref", resolved["head_sha"]]
        rec = invoke(cmd)
        name = gate[:-3]
        rec["gate"] = name
        if rec["proc"] is not None:
            (output_dir / f"{name}.stdout.txt").write_text(
                rec["proc"].stdout or "", encoding="utf-8")
            (output_dir / f"{name}.stderr.txt").write_text(
                rec["proc"].stderr or "", encoding="utf-8")
        exit_code = rec["exit_code"]
        ok = exit_code == 0
        all_ok = all_ok and ok
        status = "PASS" if ok else "FAIL"
        print(f"[{name}] {status} exit={exit_code} elapsed={rec['elapsed_seconds']}s")
        if rec["error"]:
            print(f"  could not start: {rec['error']}")
        records.append(_slim(rec))

    examples_cmd = [sys.executable, str(SCRIPT_DIR / "check_gate_examples.py"),
                    "--output", str(output_dir / "negative-examples.json")]
    rec = invoke(examples_cmd)
    rec["gate"] = "gate_examples"
    if rec["proc"] is not None:
        (output_dir / "gate_examples.stdout.txt").write_text(
            rec["proc"].stdout or "", encoding="utf-8")
        (output_dir / "gate_examples.stderr.txt").write_text(
            rec["proc"].stderr or "", encoding="utf-8")
    exit_code = rec["exit_code"]
    ok = exit_code == 0
    all_ok = all_ok and ok
    status = "PASS" if ok else "FAIL"
    print(f"[gate_examples] {status} exit={exit_code} elapsed={rec['elapsed_seconds']}s")
    if rec["error"]:
        print(f"  could not start: {rec['error']}")
    records.append(_slim(rec))

    summary = {
        "runner": "scripts/run_gates.py",
        "resolved": resolved,
        "success": all_ok,
        "records": records,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(f"\nSUMMARY: {'PASS' if all_ok else 'FAIL'} -> {output_dir / 'summary.json'}")
    sys.exit(0 if all_ok else 1)


def _slim(rec: dict) -> dict:
    """Project a record into its serializable evidence fields."""
    rec.pop("proc", None)
    return {
        "gate": rec["gate"],
        "args": rec["command"],
        "start_utc": rec["start_utc"],
        "end_utc": rec["end_utc"],
        "elapsed_seconds": rec["elapsed_seconds"],
        "exit_code": rec["exit_code"],
        "error": rec["error"],
    }


if __name__ == "__main__":
    main()
