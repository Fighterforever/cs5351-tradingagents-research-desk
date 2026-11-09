# Research Desk CI gates

The public repository runs .github/workflows/ci.yml. Branch protection requires the six checks below and one approving review. Code-owner review applies to safety paths; stale approvals are dismissed and unresolved conversations block merge. The same policy applies to administrators.

| Gate | Blocking condition | Local command |
|---|---|---|
| Prior approval | Original and revision approvals precede implementation; changed tests carry an approval update | python scripts/check_approval.py |
| Static and authority | Lint, types, dependencies, permission projection and accepted safety-change ADR pass | python scripts/check_static.py |
| Requirements | The 24-entry registry validates and every requirement maps to components and tests | python scripts/check_requirements.py |
| Semantic quality | Fixed offline replay passes; current-source live evidence satisfies each declared threshold | python scripts/check_semantic.py |
| Regression | Preserved upstream tests and all extension unit tests pass | python scripts/check_regression.py |
| AI-use log | Changed code/prompts have real session evidence covering their paths | python scripts/check_ai_use_log.py |

The workflow uses Python 3.12 and the existing requirements-lock.txt constraints. Routine CI has no provider credentials. Gate 4 reads each saved run and judgment under evaluation/release, checks source provenance, recomputes mandatory fields, and enforces support, relevance and citation thresholds. Must quality and retention failures block the gate. COST-001 token reduction and PERF-001 wall time are Should targets; a miss is logged as a non-blocking warning. Both targets pass in the current release. Fresh research runs use scripts/evaluate_release.py with host-supplied credentials.

PR checks use the real base/head diff. Safety-path changes require an accepted ADR naming the affected files and an updated approval artifact. The effective root OpenCode configuration must agree with the permissions manifest. The temporary revision role was removed after implementation.

## Execution evidence

The initial local gate records remain in evaluation/ci-initial and evaluation/ci. The first real cloud run after publication passed all six jobs: [cloud execution](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42633305097). Its original JSON is evaluation/github/first-cloud-run.json.

The current release evidence is evaluation/release. All twelve research runs and judgments passed, including 60/60 mandatory fields. Compact reduced tokens by 43.00%, with an elapsed-time ratio of 0.5652. The independently measured replay commands are under evaluation/replay-release. All six revision PR jobs passed in [run 42645314153](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42645314153); the actual job metadata is evaluation/github/revision-cloud-run.json.

The earlier account-limit and private-protection responses remain archived. The repository is now public and the required protection is active. Merging the source pull request still requires an independent authorized review.

The current complete local regression passed 790 tests and 71 subtests, with one optional AWS-dependency skip and one live-test deselection. The six local gate results and portable unit log are under evaluation/ci-release.
