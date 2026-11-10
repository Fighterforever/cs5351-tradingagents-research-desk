# Requirement trace matrix

| Requirement | Enforcing component | Test/evidence | Runtime monitor |
|---|---|---|---|
| FR-001 | research_desk.evidence, research_desk.replay, research_desk.cli | AT-01; Export, import and replay all six completed fixed cases; a missing required record must fail. | Run manifest/events and terminal outcome |
| NFR-001 | research_desk.replay | AT-01; Run six complete packs in new processes; compare signal and policy; assert zero external calls. | Run manifest/events and terminal outcome |
| SEC-001 | research_desk.evidence, research_desk.context, research_desk.graph_adapter | AT-02; Check evidence serialization and future-resolved memory; distinguish retrieval time from availability date. | Run manifest/events and terminal outcome |
| FR-002 | research_desk.review, research_desk.storage, research_desk.cli | AT-03, AT-05; Approve 100 shares at USD100 against USD100000; execute twice; final cash remains USD90000 and shares100. | Run manifest/events and terminal outcome |
| NFR-002 | research_desk.policy, research_desk.review | AT-04; Exercise approved and denied transactions; verify no LLM imports or calls on policy path. | Run manifest/events and terminal outcome |
| INV-001 | research_desk.review, research_desk.storage | AT-03, AT-05; Mutate approved quantity/evidence or current portfolio; require re-review with no partial write. | Approval reference, policy checks and transaction record |
| INV-002 | research_desk.policy, research_desk.review | AT-04; Negative cases include model text requesting a bypass; all balances and holdings stay unchanged. | Approval reference, policy checks and transaction record |
| FR-003 | research_desk.context, research_desk.graph_adapter, research_desk.cli | AT-07; Record input/output tokens, wall time, actual calls, outcome and independent quality for every arm. | Run manifest/events and terminal outcome |
| NFR-003 | research_desk.budget, research_desk.evidence, research_desk.graph_adapter | AT-06; A fake provider path attempts four calls with limit three; only three start, and no proposal is generated. | Run manifest/events and terminal outcome |
| QUALITY-001 | research_desk.graph_adapter, research_desk.replay | AT-07; Check mandatory fields deterministically for six paired runs; include failed/incomplete runs. | Run manifest/events and terminal outcome |
| QUALITY-002 | research_desk.graph_adapter | AT-07; Fixed rubric judge checks report claims against complete frozen sources; report uncited factual claims too. | Run manifest/events and terminal outcome |
| QUALITY-003 | research_desk.graph_adapter | AT-07; Score support and relevance separately with the same independent judge; retain raw judgments and failures. | Run manifest/events and terminal outcome |
| COST-001 | research_desk.context, research_desk.graph_adapter | AT-07; Same six cases and settings; quality mean drop <=0.05; judge tokens excluded and separately reported. | Run manifest/events and terminal outcome |
| PERF-001 | research_desk.graph_adapter | AT-07; Sum measured elapsed seconds of six runs per arm; disclose concurrency and all retries. | Run manifest/events and terminal outcome |
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
