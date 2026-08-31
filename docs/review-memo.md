# Review memo

## Initial implementation review

Reviewer: leo. Scope: FR-001/002/003 and AT-01 through AT-08. Verdict: CHANGES REQUIRED for live delivery after the offline slice.

Specification alignment: evidence packaging and the operator workflow were runnable. Forty-seven extension tests passed. The code review found that the total-holdings cap, valid-sell contract and exact approval quantity binding still needed correction. These are substantive semantics rather than style findings.

Architecture alignment: the extension kept the upstream graph and placed source in src/research_desk. Direct identity/history data needed explicit observation. Exact recorded tool-argument lookup was inadequate for a fair controlled rerun because valid requests can differ between the two context modes.

Code/test quality: package installation and recovery-state failures were corrected during the first session. The next tests target real omitted boundaries. Baseline/compact must be exercised through full model inputs, not only a local empty-memory transform.

Operational metadata: original upstream suite recorded 649 passed, 2 skipped and 71 subtests passed. Skips concerned an optional AWS dependency and an upstream live DeepSeek test with no key in that test invocation. The extension suite recorded47 passed before the semantic follow-up. No live result was claimed at this checkpoint. Source edits were made by OpenCode; the review supplied concrete corrections. Final release/PR evidence is appended after actual CI and live evaluation.

## Final frozen-result review

Reviewer: leo. Recorded at 2026-08-31T13:34:52.198947+00:00. Scope: the three application features, AT-01 through AT-08, the final six-case matrix and its complete evidence.

Specification alignment: all 12 real research runs completed and exported complete packages. All 12 independent CLI replays reproduced their original signal, reported zero external calls and finished within 0.812 seconds, including process startup. The paper-ledger workflow passed approval, denial, exact-term recheck, legitimate-sale and idempotent execution tests. Compact used 45.73% fewer application tokens; its elapsed-time sum was 40.42% of baseline. Support/relevance and counted-citation thresholds passed. Mandatory report fields passed 59/60 checks: META compact omitted the required full legal company name. QUALITY-001 therefore remains unmet for one report.

Architecture alignment: the selected v0.4.0 research graph and original upstream code remain. The common evidence layer reaches actual plain, tool-bound and structured-output requests in both arms. Approval and deterministic portfolio policy remain outside model authority. The final judge reads all original tool observations from the canonical event stream, without modifying research outputs or the rubric.

Code and test quality: the unified local gates recorded 649 upstream tests passed, 2 skipped and 71 subtests passed, together with 98 application tests passed. All six gate programs passed, and all six isolated rejection examples triggered their intended failures. The final run and initial failures are separately retained under evaluation/ci and evaluation/ci-initial. This review does not replace a live result with a fixture score.

Security and efficiency: a real OpenCode --auto probe rejected a protected-file write, and the accepted role configuration was installed after application implementation. Complete native session records were checked for the exact configured credential; large records use lossless gzip. No broker is connected. The live one-call budget run stopped before a second request and produced no tradeable signal. Token measurements come from provider usage, with development and judge costs separately reported.

Operational metadata: evaluation/final contains the frozen application runs and uniform final judgments; earlier judgments remain in judge-before-observation-recovery. evaluation/replay-final records every measured command. GitHub checks and branch-policy responses are release evidence, reported separately from local CI. The META rating difference between modes and the quarterly-EPS valuation interpretation error remain visible in Report.md.

Verdict: **CHANGES REQUIRED for complete requirements acceptance**. The executable submission and its evidence are ready for review, but the strict legal-name presentation requirement has one real held-out failure. A future change should enforce the general company-identity output contract and evaluate it on a newly reserved set. The frozen result must not be retroactively rewritten or passed with a ticker-specific exception.

GitHub release evidence: main and the actual signed upstream v0.4.0 tag were pushed to the private repository. Both Actions runs were blocked before any step by the account payment/spending-limit condition. Private branch protection returned HTTP403 with a plan/public-repository requirement. No account billing or visibility setting was changed. GOV-004/D7 remains incomplete; the desired server policy and actual responses are under evaluation/github. This external gap is additional to the frozen META legal-name omission and does not invalidate the recorded local gate executions.
