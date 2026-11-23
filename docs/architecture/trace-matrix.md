# Requirement trace matrix

| Requirement | Enforcing component | Test/evidence | Runtime monitor |
|---|---|---|---|
| FR-001 | research_desk.evidence, research_desk.replay, research_desk.cli | AT-01; Export, import and replay all six completed fixed cases; a missing required record must fail. | Run manifest/events and terminal outcome |
| NFR-001 | research_desk.replay | AT-01; Run six complete packs in new processes; compare signal and policy; assert zero external calls. | CLI replay result and process duration in evaluation/submission-verification/replay.json (max 0.7922s; prior release in evaluation/replay-release) |
| SEC-001 | research_desk.evidence, research_desk.context, research_desk.graph_adapter | AT-02; Check evidence serialization and future-resolved memory; distinguish retrieval time from availability date. | Run manifest/events and terminal outcome |
| FR-002 | research_desk.review, research_desk.storage, research_desk.cli | AT-03, AT-05; Approve 100 shares at USD100 against USD100000; execute twice; final cash remains USD90000 and shares100. | Proposal status, approval version and stored transaction |
| FR-004 | research_desk.evidence, research_desk.storage, research_desk.cli | AT-03, AT-05. [Registration, terminal states and evidence changes](../../test/offline/test_submission_runtime.py). [Operator CLI](../../test/offline/test_cli_slice.py). | The propose command reports the ledger status. Proposal records retain the material evidence identity and any completed transaction reference. |
| NFR-002 | research_desk.policy, research_desk.review | AT-04; Exercise approved and denied transactions; verify no LLM imports or calls on policy path. | Stored execution result and named policy checks |
| INV-001 | research_desk.review, research_desk.storage | AT-03, AT-05; Mutate approved quantity/evidence or current portfolio; require re-review with no partial write. | Approval reference, policy checks and transaction record |
| INV-002 | research_desk.policy, research_desk.review | AT-04; Negative cases include model text requesting a bypass; all balances and holdings stay unchanged. | Approval reference, policy checks and transaction record |
| FR-003 | research_desk.context, research_desk.graph_adapter, research_desk.cli | AT-07; Record input/output tokens, wall time, actual calls, outcome and independent quality for every arm. | Run manifest/events and terminal outcome |
| NFR-003 | research_desk.budget, research_desk.evidence, research_desk.graph_adapter | AT-06; A fake provider path attempts four calls with limit three; only three start, and no proposal is generated. | Run manifest/events and terminal outcome |
| QUALITY-001 | research_desk.report, research_desk.graph_adapter, research_desk.replay, research_desk.eval.live, research_desk.eval.quality | AT-07; Check mandatory fields deterministically for six paired runs; include failed/incomplete runs. | Per-arm deterministic checks in each case judgment |
| QUALITY-002 | research_desk.graph_adapter, research_desk.eval.live, research_desk.eval.quality | AT-07; Fixed rubric judge checks report claims against complete frozen sources; report uncited factual claims too. | Citation counts and validity rate in each case judgment |
| QUALITY-003 | research_desk.graph_adapter, research_desk.eval.live, research_desk.eval.quality | AT-07; Score support and relevance separately with the same independent judge; retain raw judgments and failures. | Per-arm support, relevance and semantic-validity fields |
| COST-001 | research_desk.context, research_desk.graph_adapter, research_desk.eval.live, research_desk.eval.quality | AT-07; Same six cases and settings; quality mean drop <=0.05; judge tokens excluded and separately reported. | Provider input and output usage in each run and aggregate |
| PERF-001 | research_desk.graph_adapter, research_desk.eval.live, research_desk.eval.quality | AT-07; Sum measured elapsed seconds of six runs per arm; disclose concurrency and all retries. | Elapsed seconds in each run summary and the aggregate ratio |
| GOV-001 | .github/workflows/ci.yml, scripts | AT-08; Validate approval timestamps and eight test IDs; changed safety paths require decision evidence. | CI job result |
| GOV-002 | .github/workflows/ci.yml, scripts | AT-08; Run lint/type/dependency/schema checks and both tests/ and test/offline/ in CI. | CI job result |
| GOV-003 | .github/workflows/ci.yml, scripts | AT-08; Compare changed paths to the log; recompute fixed evidence quality rather than trusting a hand-written PASS. | CI job result |
| GOV-004 | .github/workflows/ci.yml, .github/CODEOWNERS | AT-08; Inspect actual branch protection and pull-request check results; require an approved review before merge. | CI job result |
| CTX-001 | research_desk.context, research_desk.eval.compact_delegate, research_desk.budget | AT-06; context budget unit tests | Per-request budget observations and context stop event |
| INH-001 | tradingagents.graph | upstream-regression, AT-07; Run the complete original tests/ directory; frozen integration preserves public graph contracts. | Run manifest/events and terminal outcome |
| INH-002 | tradingagents.agents.utils.memory | upstream-regression, AT-07; Run the complete original tests/ directory; frozen integration preserves public graph contracts. | Run manifest/events and terminal outcome |
| INH-003 | tradingagents.graph | upstream-regression, AT-07; Run the complete original tests/ directory; frozen integration preserves public graph contracts. | Run manifest/events and terminal outcome |
| INH-004 | tradingagents.dataflows | upstream-regression, AT-07; Run the complete original tests/ directory; frozen integration preserves public graph contracts. | Run manifest/events and terminal outcome |
| INH-005 | research_desk.evidence | upstream-regression, AT-07; Run the complete original tests/ directory; frozen integration preserves public graph contracts. | Run manifest/events and terminal outcome |

AT-01: test/offline/test_at01_replay.py. AT-02: test_at02_context_ptc.py. AT-03: test_at03_ledger_approve.py. AT-04: test_at04_reject_boundaries.py. AT-05: test_at05_version_recheck.py. AT-06: test_at06_budget_context.py. AT-07: fixed six-case live evaluation plus its saved artifacts. AT-08: the six CI checks and their actual negative/repaired evidence. All original tests/ are retained.

## Submission repair acceptance

The submission revision registered package-based proposal recovery as FR-004 under [ADR-005](adr/005-submission-contracts.md). AT-03 and AT-05 cover material evidence identity and repeat registration. FR-002 continues to govern operator approval and execution. AT-01 covers CLI rebuild failures. AT-07 checks complete six-case pairs and upstream source provenance. AT-08 compares scoped approvals and the changed AI-use entries against the reviewed diff. The corresponding unit cases are under `test/offline/`.
