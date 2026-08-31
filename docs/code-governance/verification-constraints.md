# Verification constraints

All fit criteria have named evidence in the trace matrix. All zero-tolerance invariants need a negative example that would fail if the invariant were removed. Tests refer to requirement or AT identifiers. Tests should assert externally meaningful behavior instead of restating a function's implementation.

Tier1 is structural: package/import health, ownership boundaries, effective permissions, requirement schema, lint, type and dependency checks. Tier2 is regression: run all original tests/ plus test/offline/ after each completed implementation round. Tier3 is behavioral: replay equivalence, policy safety, request-budget enforcement and fixed-corpus factual quality. Passing one tier does not substitute for another.

Offline fixture evidence is deliberately constructed and labeled. Live evidence comes only from actual requests. Fixed evaluation inputs contain six real equity cases, with AAPL/MSFT used for development and four other companies reserved before tuning. Both arms preserve graph roles and use identical model settings. Record retries and failed cases. Report actual provider input/output usage; judge calls remain separate.

The live quality assessment verifies mandatory numeric fields deterministically and uses the predeclared support/relevance/citation rubric. CI's offline semantic gate recomputes fixed captured-output properties and cannot claim it establishes new live model quality. Model/prompt changes additionally need fresh saved live evidence before a release quality claim.

The approved tests precede implementation in docs/process/test-approval.yaml. CI must check timestamps, scope and test IDs, not merely accept the word APPROVED. All six gates have negative examples and repaired outcomes when exercised. External branch protection is reported separately from local checks.
