# One local CI evidence runner

Create only `scripts/run_gates.py` in the project. It is a small orchestration convenience for the six already implemented real gate CLIs plus the AT-08 expected-rejection demonstration. Do not change any validator, source, test, fixture, workflow, configuration or approval.

Read the CLI signatures of `scripts/check_approval.py`, `check_static.py`, `check_requirements.py`, `check_semantic.py`, `check_regression.py`, `check_ai_use_log.py` and `check_gate_examples.py`. All six gates support `--base-ref` and `--head-ref` through the shared parser. The examples support `--output`.

Required behavior:

- Use Python standard library and the current interpreter (`sys.executable`). Locate the project from this script's own parent.
- Require explicit `--base-ref` and `--head-ref` arguments; accept `--output-dir`, default `evaluation/ci`. Resolve both revisions once with real `git rev-parse --verify` and preserve both supplied refs and resolved immutable commit provenance in the summary. Do not include environment variables or credentials.
- Sequentially run the six existing gate CLIs in their numeric order, with both resolved revisions, then `check_gate_examples.py --output <output-dir>/negative-examples.json`. Collect results for all gates even if one fails so the actual errors are actionable. Do not retry, modify files, install anything, call APIs, or turn a failed gate into a pass.
- For every invocation record the exact argument list, UTC start/end time, elapsed seconds, exit code, and separate complete stdout/stderr text files. Print a concise status as each invocation finishes. Write `summary.json` with these records and a boolean success that is true only if all seven command exit codes are zero. Exit nonzero otherwise. If a process cannot start, record the real error and mark it failed.
- This is just one reproducible runner, with no custom testing framework or abstraction layer. Use clear normal Python, around 100 lines if feasible.

Do not execute the gates now: source is still being finalized, and the coordinator will run once against the final committed scope. You may run `ruff check scripts/run_gates.py` and `python scripts/run_gates.py --help` only, then stop.
