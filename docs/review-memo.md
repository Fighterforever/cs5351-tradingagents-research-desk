# Review memo

## Initial implementation review

Reviewer: leo. Scope: FR-001/002/003 and AT-01 through AT-08. Verdict: CHANGES REQUIRED for live delivery after the offline slice.

Specification alignment: evidence packaging and the operator workflow were runnable. Forty-seven extension tests passed. The code review found that the total-holdings cap, valid-sell contract and exact approval quantity binding still needed correction. These are substantive semantics rather than style findings.

Architecture alignment: the extension kept the upstream graph and placed source in src/research_desk. Direct identity/history data needed explicit observation. Exact recorded tool-argument lookup was inadequate for a fair controlled rerun because valid requests can differ between the two context modes.

Code/test quality: package installation and recovery-state failures were corrected during the first session. The next tests target real omitted boundaries. Baseline/compact must be exercised through full model inputs, not only a local empty-memory transform.

Operational metadata: original upstream suite recorded 649 passed, 2 skipped and 71 subtests passed. Skips concerned an optional AWS dependency and an upstream live DeepSeek test with no key in that test invocation. The extension suite recorded 47 passed before the semantic follow-up. No live result was claimed at this checkpoint. Source edits were made by OpenCode; the review supplied concrete corrections. Final release/PR evidence is appended after actual CI and live evaluation.

## First frozen-result review

Reviewer: leo. Recorded at 2026-08-31T13:34:52.198947+00:00. Scope: the three application features, AT-01 through AT-08, the final six-case matrix and its complete evidence.

Specification alignment: all 12 real research runs completed and exported complete packages. All 12 independent CLI replays reproduced their original signal, reported zero external calls and finished within 0.812 seconds, including process startup. The paper-ledger workflow passed approval, denial, exact-term recheck, legitimate-sale and idempotent execution tests. Compact used 45.73% fewer application tokens; its elapsed-time sum was 40.42% of baseline. Support/relevance and counted-citation thresholds passed. Mandatory report fields passed 59/60 checks: META compact omitted the required full legal company name. QUALITY-001 therefore remains unmet for one report.

Architecture alignment: the selected v0.4.0 research graph and original upstream code remain. The common evidence layer reaches actual plain, tool-bound and structured-output requests in both arms. Approval and deterministic portfolio policy remain outside model authority. The final judge reads all original tool observations from the canonical event stream, without modifying research outputs or the rubric.

Code and test quality: the unified local gates recorded 649 upstream tests passed, 2 skipped and 71 subtests passed, together with 98 application tests passed. All six gate programs passed, and all six isolated rejection examples triggered their intended failures. The final run and initial failures are separately retained under evaluation/ci and evaluation/ci-initial. This review does not replace a live result with a fixture score.

Security and efficiency: a real OpenCode --auto probe rejected a protected-file write, and the accepted role configuration was installed after application implementation. Complete native session records were checked for the exact configured credential; large records use lossless gzip. No broker is connected. The live one-call budget run stopped before a second request and produced no tradeable signal. Token measurements come from provider usage, with development and judge costs separately reported.

Operational metadata: evaluation/final contains the frozen application runs and uniform final judgments; earlier judgments remain in judge-before-observation-recovery. evaluation/replay-final records every measured command. GitHub checks and branch-policy responses are release evidence, reported separately from local CI. The META rating difference between modes and the quarterly-EPS valuation interpretation error remain visible in Report.md.

Verdict: **CHANGES REQUIRED for complete requirements acceptance**. The executable submission and its evidence are ready for review, but the strict legal-name presentation requirement has one real held-out failure. A future change should enforce the general company-identity output contract and evaluate it on a newly reserved set. The frozen result must not be retroactively rewritten or passed with a ticker-specific exception.

GitHub release evidence: main and the actual signed upstream v0.4.0 tag were pushed to the private repository. Both Actions runs were blocked before any step by the account payment/spending-limit condition. Private branch protection returned HTTP 403 with a plan/public-repository requirement. No account billing or visibility setting was changed. GOV-004/D7 remains incomplete; the desired server policy and actual responses are under evaluation/github. This external gap is additional to the frozen META legal-name omission and does not invalidate the recorded local gate executions.


## Release revision review

Decision identifier: leo. Scope: ADR-004, five requirement increments, and the current paired research matrix. This technical review accompanies the source pull request; the required independent GitHub approval is a separate review action.

Specification alignment: all twelve current research runs completed. Mandatory fields passed 60/60; all semantic checks and individual quality thresholds passed. Mean support increased from 0.9000 to 0.9083, and relevance remained 0.95. Compact used 43.00% fewer application tokens, with an elapsed-time ratio of 0.5652.

Architecture alignment: the original graph remains intact. The model has no approval or ledger authority. Complete-input bounds apply at plain, tool-bound and structured request boundaries. Evidence-derived report identity is generic. The release gate validates actual per-arm evidence against current source.

Code and test quality: rejected status remains terminal; current-state policy and exact approvals remain intact. Request serialization now carries the verified provider setting. The current local full suite passed 790 tests and 71 subtests. Required cloud checks are recorded separately in evaluation/github. All twelve CLI replays preserve the original signal with zero external calls, and the slowest takes 0.9119 seconds.

Security and efficiency: temporary implementation permissions were removed. Secrets are supplied through host environment variables. Public branch protection enforces required checks and human review, including for administrators. Native coding sessions and both successful and failed experiments remain available.

Verdict: **APPROVE technical requirements acceptance** for the current-source application and research evidence. The final delivery checklist records the team roster and independent merge review required to complete submission administration.


## Independent automated assessment

Gemini CLI reviewed the original course requirements together with the current source, tests and documentary evidence. The first assessment identified four correctable documentation/alignment issues: Should-target enforcement wording, report-header attribution, prompt snapshot naming and the GOV-004 trace row. All four were corrected.

The follow-up assessment reports technical_ready true and an empty remaining_technical_issues list. It confirms alignment with the higher-grade directions for architecture, governance and token efficiency. Native review responses are retained in transcripts/gemini-release-review.json and transcripts/gemini-release-followup.json.

The assessment leaves three authentic team actions open: formal identities and contribution evidence, per-student annotated interventions, and independent GitHub/rotating peer review. These remain on the delivery checklist.

## Intervention evidence and report review

Reviewer: coordinating workflow, with an independent Gemini CLI assessment. Scope: all non-video deliverables and 30 annotated directives across 11 native OpenCode sessions. Verdict: **CHANGES REQUIRED for complete submission**; technical acceptance is complete.

Each annotation now links its exact source message and quote to the observed result. The message locators and quotations were checked against the native exports. The participant index records Liyu MA (59072966) as decision owner leo and identifies the workflow that sent the prompts. Original conversations remain available alongside the annotations.

Gemini found stale wording in three reflections. Bravo now describes the implemented context cap. Charlie describes the completed rejected-state repair and its transition test. Echo records the passing revision CI and the pending independent approval. Reference spacing was also corrected. Application source and experiment results are unchanged.

The original requirements leave three areas to complete: formal member identification and contribution confirmation; authentic member interventions across the supervised pipeline; independent peer review and protected merge. Requirements classification and architecture candidate evaluation have design artifacts, but their original supervision record still needs to be linked. The team should add the corresponding conversation or document a new review as a subsequent review.

Two assessment details were checked against the course text. D6 requires relative contributions and suggests productive hours or story points as possible measures; it does not prescribe a sprint-by-sprint table. D5 requires marked team interventions and full pipeline coverage; per-student files follow the supplied repository naming convention. The source revision CI link remains attached to the evaluated implementation. The final package also contains the CI receipt for its documentation update.

Native editorial and assessment responses: `transcripts/gemini-intervention-edit.json` and `transcripts/gemini-intervention-review.json`.

Gemini’s focused follow-up confirmed all corrections resolved and reported no remaining editorial issues. Its response is retained in `transcripts/gemini-intervention-followup.json`. The five reflections remain within 300–500 words, and the rendered report contains 23 pages.

## Requirements and architecture process review

Reviewer: Gemini CLI. Scope: all 24 requirement classifications, three architecture candidates and the five assigned responsibility areas. Verdict: **APPROVE technical assessment**. The requirements review and weighted candidate comparison support the existing application-extension design. No new runtime issue was identified.

Six selected user-message excerpts now document leo's actual scope and governance directions. They are linked separately from the 30 implementation prompts issued by the coordinating workflow. The subsequent review and its exact prompts are preserved under `transcripts/gemini-pipeline-review.json` and `transcripts/gemini-pipeline-integration.json`. The finished review is in `docs/process/pipeline-review.md`.

Team attribution and independent code-owner approval remain on the delivery checklist. This review adds a recorded requirements/architecture assessment to the available development evidence.

## Reviewer configuration

The user supplied `wangsaorui` as the review account. A write-access invitation was issued, and the `add-code-owner` branch prepares the owner entry on `main`. The branch reuses the existing six-gate workflow. The activation sequence is recorded in `docs/process/reviewer-onboarding.md`; write access is now confirmed, while the configuration PR and actual review decisions remain pending.
