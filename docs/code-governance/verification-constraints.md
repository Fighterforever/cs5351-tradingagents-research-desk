# Verification constraints

All fit criteria have named evidence in the trace matrix. All zero-tolerance invariants need a negative example that would fail if the invariant were removed. Tests refer to requirement or AT identifiers. Tests should assert externally meaningful behavior instead of restating a function's implementation.

Tier1 is structural: package/import health, ownership boundaries, effective permissions, requirement schema, lint, type and dependency checks. Tier2 is regression: run the original unit suites plus test/offline after each completed implementation round. Live, integration and smoke markers are excluded from these unit runs; the full research benchmark is recorded separately. Tier3 is behavioral: replay equivalence, policy safety, request-budget enforcement and fixed-corpus factual quality. Passing one tier does not substitute for another.

Offline fixture evidence is deliberately constructed and labeled. Live evidence comes only from actual requests. Fixed evaluation inputs contain six real equity cases, with AAPL/MSFT used for development and four other companies reserved before tuning. Both arms preserve graph roles and use identical model settings. Record retries and failed cases. Report actual provider input/output usage; judge calls remain separate.

The live quality assessment verifies mandatory numeric fields deterministically and uses the predeclared support/relevance/citation rubric. The semantic gate combines deterministic replay with source-bound live evidence. It loads each of the twelve current runs and judgments, recomputes mandatory checks, and rejects missing, stale or below-threshold results. Provider calls occur during the release experiment, while CI validates the saved evidence without credentials.

The approved tests precede implementation in docs/process/test-approval.yaml. CI must check timestamps, scope and test IDs, not merely accept the word APPROVED. All six gates have negative examples and repaired outcomes when exercised. External branch protection is reported separately from local checks.
