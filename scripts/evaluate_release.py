"""User-invoked release evaluation runner.

Runs the canonical six cases through the real ``research_desk`` CLI, baseline
then compact for each case, in bounded parallel case workers. Every case uses
separate subprocesses so no global graph state can leak between runs. The runner
then judges each case, aggregates the actual outputs and validates the release
gate against the current source.

Credentials are inherited from the host environment only. CLI output logs live
outside the evidence root in the sibling ``<out>-logs`` directory, and failed
attempts are archived under ``<out>-attempts`` instead of being overwritten.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODES = ("baseline", "compact")
MAX_WORKERS = 6


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _read_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str) + "\n", encoding="utf-8")


def _archive(path: Path, attempts: Path, ticker: str, label: str) -> None:
    """Move an existing attempt aside so a rerun never overwrites it."""
    if not path.exists():
        return
    stamp = _now()
    dest = attempts / ticker / f"{label}-{stamp}"
    suffix = 1
    while dest.exists():
        dest = attempts / ticker / f"{label}-{stamp}-{suffix}"
        suffix += 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(dest))


def _arm_complete(arm: Path, current: str) -> bool:
    summary = _read_json(arm / "summary.json")
    provenance = _read_json(arm / "provenance.json")
    return (
        isinstance(summary, dict)
        and summary.get("outcome") == "completed"
        and summary.get("pack_complete") is True
        and not summary.get("error")
        and isinstance(provenance, dict)
        and provenance.get("source_fingerprint") == current
    )


def _judge_complete(out: Path, ticker: str, current: str) -> bool:
    for mode in MODES:
        arm = out / "judge" / ticker / mode
        judge = _read_json(arm / "judge.json")
        provenance = _read_json(arm / "provenance.json")
        if not (
            isinstance(judge, dict)
            and judge.get("error") is False
            and judge.get("semantic_valid") is True
            and isinstance(provenance, dict)
            and provenance.get("source_fingerprint") == current
        ):
            return False
    return True


def _run_cli(
    command: list[str], logs: Path, ticker: str, label: str
) -> dict:
    """Run one CLI command, retaining its complete output outside the evidence root."""
    log_path = logs / ticker / f"{label}-{_now()}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )
    log_path.write_text(
        f"$ {' '.join(command)}\n\n[exit {proc.returncode}]\n\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}\n",
        encoding="utf-8",
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "log": str(log_path),
    }


def _run_case(
    case: dict,
    out: Path,
    logs: Path,
    attempts: Path,
    current: str,
    resume: bool,
) -> dict:
    ticker = str(case["ticker"]).upper()
    result: dict = {
        "ticker": ticker,
        "resumed_arms": [],
        "resumed_judge": False,
        "commands": [],
        "problems": [],
    }
    rerun_arm = False

    for mode in MODES:
        arm = out / ticker / mode
        if resume and _arm_complete(arm, current):
            result["resumed_arms"].append(mode)
            continue
        if resume:
            _archive(arm, attempts, ticker, mode)
        command = [
            sys.executable,
            "-m",
            "research_desk.cli",
            "evaluate-case",
            ticker,
            "--mode",
            mode,
            "--out",
            str(out),
            "--max-calls",
            "32",
        ]
        run = _run_cli(command, logs, ticker, f"{mode}-evaluate")
        result["commands"].append(run)
        rerun_arm = True
        if run["returncode"] != 0:
            result["problems"].append(
                f"{ticker}/{mode}: evaluate-case exited {run['returncode']}"
            )
        summary = _read_json(out / ticker / mode / "summary.json")
        if not (
            isinstance(summary, dict)
            and summary.get("outcome") == "completed"
            and summary.get("pack_complete") is True
            and not summary.get("error")
        ):
            result["problems"].append(
                f"{ticker}/{mode}: run is incomplete or did not complete"
            )

    if resume and not rerun_arm and _judge_complete(out, ticker, current):
        result["resumed_judge"] = True
        return result
    if resume:
        _archive(out / "judge" / ticker, attempts, ticker, "judge")

    command = [
        sys.executable,
        "-m",
        "research_desk.cli",
        "judge-case",
        ticker,
        "--out",
        str(out),
    ]
    run = _run_cli(command, logs, ticker, "judge")
    result["commands"].append(run)
    if run["returncode"] != 0:
        result["problems"].append(f"{ticker}: judge-case exited {run['returncode']}")

    for mode in MODES:
        judge = _read_json(out / "judge" / ticker / mode / "judge.json")
        if not (
            isinstance(judge, dict)
            and judge.get("error") is False
            and judge.get("semantic_valid") is True
        ):
            result["problems"].append(
                f"{ticker}/{mode}: judge is missing, errored, or semantically invalid"
            )
    return result


def _prepare_output(out: Path, resume: bool) -> str | None:
    if out.exists():
        if not out.is_dir():
            return f"output path exists and is not a directory: {out}"
        if any(out.iterdir()) and not resume:
            return f"output directory is not empty; pass --resume to continue: {out}"
    else:
        out.mkdir(parents=True)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run and validate the six-case release evaluation."
    )
    parser.add_argument("--out", required=True, help="Evidence output root directory")
    parser.add_argument(
        "--workers",
        type=int,
        default=3,
        help=f"Parallel case workers (1..{MAX_WORKERS}, default 3)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse completed current-source runs and archive failed attempts",
    )
    args = parser.parse_args()

    if not 1 <= args.workers <= MAX_WORKERS:
        print(f"--workers must be between 1 and {MAX_WORKERS}")
        return 2

    out = Path(args.out).resolve()
    logs = out.parent / f"{out.name}-logs"
    attempts = out.parent / f"{out.name}-attempts"

    problem = _prepare_output(out, args.resume)
    if problem:
        print(problem)
        return 2
    logs.mkdir(parents=True, exist_ok=True)

    try:
        from research_desk.eval.case_registry import all_cases
        from research_desk.eval.quality import source_fingerprint

        current = source_fingerprint(PROJECT_ROOT)
    except Exception as exc:  # noqa: BLE001 - fail visibly instead of guessing
        print(f"cannot compute the current source fingerprint: {exc}")
        return 1

    cases = all_cases()
    results: list[dict] = []
    problems: list[str] = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [
            pool.submit(
                _run_case, case, out, logs, attempts, current, args.resume
            )
            for case in cases
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            problems.extend(result["problems"])

    aggregate_command = [
        sys.executable,
        "-m",
        "research_desk.cli",
        "aggregate",
        str(out),
    ]
    aggregate_run = _run_cli(aggregate_command, logs, "aggregate", "aggregate")
    if aggregate_run["returncode"] != 0:
        problems.append(f"aggregate exited {aggregate_run['returncode']}")

    try:
        from research_desk.eval.quality import validate_release

        gate = validate_release(PROJECT_ROOT, out)
    except Exception as exc:  # noqa: BLE001 - record the failure, keep the evidence
        gate = {
            "failures": [f"release validation raised: {exc}"],
            "checks": [],
            "warnings": [],
            "metrics": {},
        }
    problems.extend(gate.get("failures", []))

    passed = not problems and not gate.get("failures")
    summary = {
        "out": str(out),
        "logs": str(logs),
        "attempts": str(attempts),
        "source_fingerprint": current,
        "workers": args.workers,
        "resume": args.resume,
        "cases": results,
        "aggregate": aggregate_run,
        "gate": gate,
        "problems": problems,
        "passed": passed,
    }
    _write_json(logs / "release-run.json", summary)
    _write_json(out / "aggregate" / "release-gate.json", summary)

    print(
        json.dumps(
            {
                "passed": passed,
                "problems": problems,
                "gate_failures": gate.get("failures", []),
                "metrics": gate.get("metrics", {}),
            },
            indent=2,
            default=str,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
