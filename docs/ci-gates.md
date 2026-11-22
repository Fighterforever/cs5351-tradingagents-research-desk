# Research Desk CI gates

The public repository runs .github/workflows/ci.yml. Branch protection requires the six checks below and one approving review. Code-owner review applies to safety paths; stale approvals are dismissed and unresolved conversations block merge. The same policy applies to administrators.

| Gate | Blocking condition | Local command |
|---|---|---|
| Prior approval | A new approval entry covers the changed behavior and names existing test evidence; the approval predates the implementation commit | python scripts/check_approval.py |
| Static and authority | Lint, types, dependencies and permission checks pass. Safety changes also undergo API compatibility and ADR checks | python scripts/check_static.py |
| Requirements | The 25-entry registry validates and every requirement maps to components and tests | python scripts/check_requirements.py |
| Semantic quality | Four fixtures replay, six frozen cases retain required prompt facts, and saved release results pass the checks implemented by the validator | python scripts/check_semantic.py |
| Regression | Preserved upstream tests and all extension unit tests pass | python scripts/check_regression.py |
| AI-use log | New or amended log entries cover the changed code and prompts and link to actual evidence | python scripts/check_ai_use_log.py |

The workflow uses Python 3.12 and the existing requirements-lock.txt constraints. Routine CI has no provider credentials. Gate 4 reads the twelve runs and judgments under evaluation/submission-release, checks source provenance, recomputes mandatory fields, and checks stored support, relevance and citation scores against thresholds. The [submission review](review-memo.md#submission-review) records which changes and inputs this validation covers. Must quality and retention failures block the gate. COST-001 token reduction and PERF-001 wall time are Should targets; a miss is logged as a non-blocking warning. The release summary records the measured values for both targets. Fresh research runs use scripts/evaluate_release.py with host-supplied credentials.

To reproduce a PR check, use a Git clone containing both revisions. Append `--base-ref <base> --head-ref <head>` to the commands for gates 1, 2, 4 and 6, replacing the placeholders with the PR revisions. From the ZIP, the unit suite and saved evidence can be inspected without Git history. Safety-path changes require an accepted ADR naming the affected files and an updated approval artifact. The effective root OpenCode configuration must agree with the permissions manifest. The temporary revision role was removed after implementation.

## Execution evidence

### Submission revision

All twelve research runs and their twelve judgments passed the source-bound release gate. The validator checked 60/60 mandatory fields. Compact used 345,309 application tokens against 600,576 for baseline, a 42.50% reduction. Its summed run time was 48.65% of baseline. Both quality retention measures and both cost and time targets passed. The validator recorded no warnings. [Release gate receipt](../evaluation/submission-release/aggregate/release-gate.json)

The local regression passed **832 tests and 71 subtests**. The upstream suite contributed 649 passing tests, one optional-dependency skip and one live-test deselection. All 183 extension tests passed. [Unit run record](../evaluation/submission-verification/unit-regression.txt)

### Earlier releases

The initial local gate records remain in evaluation/ci-initial and evaluation/ci. The first real cloud run after publication passed all six jobs: [cloud execution](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42633305097). Its original JSON is evaluation/github/first-cloud-run.json.

The release before ADR-005 is archived in evaluation/release. All twelve research runs and judgments passed, including 60/60 mandatory fields. Compact reduced tokens by 43.00%, with an elapsed-time ratio of 0.5652. The independently measured replay commands are under evaluation/replay-release. All six revision PR jobs passed in [run 42645314153](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42645314153); the actual job metadata is evaluation/github/revision-cloud-run.json.

The earlier account-limit and private-protection responses remain archived. The repository is now public and the required protection is active. Delta [approved the source pull request](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/1#pullrequestreview-5840085663) before it merged. All six jobs passed on [the merged source](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42798475065).

The release before ADR-005 passed 790 tests and 71 subtests, with one optional AWS-dependency skip and one live-test deselection. The submission review identified the gate changes incorporated in the current revision. [Earlier gate results and unit log](../evaluation/ci-release) · [Submission review](review-memo.md#submission-review)
