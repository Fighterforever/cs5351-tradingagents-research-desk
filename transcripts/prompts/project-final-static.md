Finish ONLY the following narrow fixes, then stop. Read actual declarations before editing; do not re-explore governance (current ADR004 and revision authorization cover these fixes). Full unit suite already passes 789 tests.
1. Ruff: compact_delegate.py:215 SIM103 direct return; test_context_budget.py:95 zip strict; test_report_contract.py imports sorted.
2. mypy quality.py line85 usage list can contain None: narrow valid numeric usage into properly typed locals before positive/count consistency checks, preserving rejection of missing/boolean/zero/invalid usage.
3. scripts/evaluate_release.py evaluate-case command must explicitly pass --max-calls 32, as evaluation plan requires. Keep both arms same.
Do not change any other runtime behavior. No shell commands, no new tests, no broad refactor. Report exact edited paths then stop.
