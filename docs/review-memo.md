# Review memo

The [review of the repaired submission](#review-of-the-repaired-submission) covers ADR-005. The earlier entries below record the findings and decisions for the versions reviewed at the time.

## Initial implementation review

Reviewer: Liyu MA. Scope: FR-001/002/003 and AT-01 through AT-08. Verdict: CHANGES REQUIRED for live delivery after the offline slice.

Specification alignment: evidence packaging and the operator workflow were runnable. Forty-seven extension tests passed. The code review found that the total-holdings cap, valid-sell contract and exact approval quantity binding still needed correction. These are substantive semantics rather than style findings.

Architecture alignment: the extension kept the upstream graph and placed source in src/research_desk. Direct identity/history data needed explicit observation. Exact recorded tool-argument lookup was inadequate for a fair controlled rerun because valid requests can differ between the two context modes.

Code/test quality: package installation and recovery-state failures were corrected during the first session. The next tests target real omitted boundaries. Baseline/compact must be exercised through full model inputs, not only a local empty-memory transform.

Operational metadata: original upstream suite recorded 649 passed, 2 skipped and 71 subtests passed. Skips concerned an optional AWS dependency and an upstream live DeepSeek test with no key in that test invocation. The extension suite recorded 47 passed before the semantic follow-up. No live result was claimed at this checkpoint. Source edits were made by OpenCode; the review supplied concrete corrections. Final release/PR evidence is appended after actual CI and live evaluation.

## First frozen-result review

Reviewer: Liyu MA. Recorded at 2026-08-31T13:34:52.198947+00:00. Scope: the three application features, AT-01 through AT-08, the final six-case matrix and its complete evidence.

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

The follow-up assessment reports technical_ready true and an empty remaining_technical_issues list. It confirms alignment with the higher-grade directions for architecture, governance and token efficiency. The [review excerpts](../transcripts/editorial-review-excerpts.json) link both full responses.

The assessment identified gaps in the roster, individual supervision evidence and independent review. The [delivery checklist](process/delivery-checklist.md) records their current status.

## Intervention evidence and report review

Reviewer: coordinating workflow, with an independent Gemini CLI assessment. Scope: all non-video deliverables and 30 annotated directives across 11 native OpenCode sessions. Verdict: **CHANGES REQUIRED for complete submission**; technical acceptance is complete.

Each annotation now links its exact source message and quote to the observed result. The message locators and quotations were checked against the native exports. The participant index records Liyu MA (59072966) as decision owner leo and identifies the workflow that sent the prompts. Original conversations remain available alongside the annotations.

The editorial review corrected three accounts: how the context cap works, which test covered the rejected-state repair, and which CI checks had passed at the time of review.

At this review, the team still needed to confirm individual contributions, locate student decisions from early design and obtain an independent merge review. The requirements registry and candidate comparison already recorded the resulting design choices.

Two assessment details were checked against the course text. D6 requires relative contributions and suggests productive hours or story points as possible measures; it does not prescribe a sprint-by-sprint table. D5 requires marked team interventions and full pipeline coverage; per-student files follow the supplied repository naming convention. The source revision CI link remains attached to the evaluated implementation. The final package also contains the CI receipt for its documentation update.

Native editorial and assessment responses: `transcripts/gemini-intervention-edit.json` and [archived gemini-intervention-review](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/a1af194bbd1540c0ae2a11c1395269c52e02dfec/transcripts/gemini-intervention-review.json).

Gemini checked the revised passages and closed the editorial findings. The [follow-up review](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/a1af194bbd1540c0ae2a11c1395269c52e02dfec/transcripts/gemini-intervention-followup.json) records its decision.

## Requirements and architecture process review

Reviewer: Gemini CLI. Scope: the classification of 24 requirements, the comparison of three architecture candidates and the allocation of design responsibilities. Verdict: **APPROVE technical assessment**. The requirements review and weighted candidate comparison support the existing application-extension design. No new runtime issue was identified.

Six selected user-message excerpts now document Liyu MA’s actual scope and governance directions. They are linked separately from the 30 implementation prompts issued by the coordinating workflow. The subsequent review and its exact prompts are preserved under [archived gemini-pipeline-review](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/a1af194bbd1540c0ae2a11c1395269c52e02dfec/transcripts/gemini-pipeline-review.json) and [archived gemini-pipeline-integration](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/a1af194bbd1540c0ae2a11c1395269c52e02dfec/transcripts/gemini-pipeline-integration.json). The finished review is in `docs/process/pipeline-review.md`.

This review documented the requirements and architecture assessment. The independent code-owner review took place later and is recorded below.

## Reviewer configuration

The team designated `wangsaorui` as a code owner. The [onboarding record](process/reviewer-onboarding.md) documents write access and activation on `main`. The account subsequently approved PR #1.

## Four-member allocation

The four members are Liyu MA, Xinyao HENG, Yinuo Li and Chengru WANG. Liyu MA handles report integration and submission checks. Xinyao HENG handles release governance, Yinuo Li handles packaging, and Chengru WANG handles CI. The [team table](process/team.md) records their assigned weights and review rotation.

## Independent code-owner review of PR #1

Reviewer: wangsaorui (Chengru WANG, student 60254685), the designated non-author code owner. Review analysis was assisted by the AI coding agent; the verdict below and the GitHub approval are the human reviewer's own decision. Recorded 2026-11-10.

Scope: pull request #1 (`improve-delivery` into `main`, head `154e77c`). The reviewer inspected the substantive code/CI/governance diff against `main` and verified that each referenced gate program exists; the large `evaluation/` and `transcripts/` evidence blobs were spot-checked, not re-executed.

Specification alignment: the CI workflow is consolidated into six blocking jobs (`gate-1-approval` through `gate-6-ai-use-log`) that map one-to-one onto the six course gates. All six referenced scripts (`scripts/check_approval.py`, `check_static.py`, `check_requirements.py`, `check_semantic.py`, `check_regression.py`, `check_ai_use_log.py`) are present on the branch. The AI-use log is updated on this change, so Gate 6 is satisfied.

Architecture alignment: the upstream research graph is preserved and the extension remains under `src/research_desk`. Model output carries no approval or ledger authority; ADR-004 documents the release-quality and context-budget decisions.

Code and test quality: six new offline modules expand regression coverage (`test_approval_revision`, `test_context_budget`, `test_eval_provenance`, `test_release_quality`, `test_report_contract`, `test_revision_contracts`).

Security: the workflow runs with `permissions: contents: read`; secrets come from host environment variables; no broker is connected.

Findings carried as follow-ups (non-blocking):
- F1 (medium): the gate rewrite pins Python 3.12 only, dropping the prior 3.10-3.13 matrix; cross-version coverage is no longer exercised.
- F2 (documentation): this PR does not close D6 — `team.md` still records equal assigned weights rather than measured hours, and the formal roster for Liyu MA/Xinyao HENG/Yinuo Li is unfinished.
- F3 (hygiene, low): roughly 1013 files and about 119k added lines, most of them committed evidence artifacts.
- F4 (verification statement): the reviewer did not locally re-run the full 790-test suite; approval is conditioned on the PR's own CI turning green.

Verdict: **APPROVE with comments**. No finding is safety-blocking; F1-F4 are recorded as follow-ups. The independent code-owner approval on GitHub and the protected-branch merge remain the human administrative actions that complete D7.

**Release outcome.** After this memo, Chengru WANG recorded the [approval on GitHub](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/1#pullrequestreview-5840085663). PR #1 merged, and all six [main-branch checks](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42798475065) passed.

## Technical review of PR #2

[PR #2](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/2) restores an advisory Python-version matrix. Its two commits change the workflow, CI documentation and AI-use log, and include [Chengru WANG’s supervision record](../transcripts/60254685-Chengru-WANG.md). The change leaves the application and the six required checks in place. The version matrix runs the existing regression job on pull requests. No model credentials or paid calls are required.

All six required checks passed. The advisory jobs passed on Python 3.12 and 3.13. Installation stopped before regression on [Python 3.10](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/43003982308/job/130466775782) at the pandas pin and on [Python 3.11](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/43003982308/job/130466775679) at the NumPy pin. The package declares Python 3.10 or later.

Technical verdict: **CHANGES REQUIRED** to claim reproducibility across the declared Python versions. Reconcile the dependency pins with the supported interpreters and retain the advisory status until those jobs pass. This assessment covers the published diff and CI output. The PR is open and awaits an independent reviewer’s decision on GitHub.

## Submission review

This review covers the archived release, the published pull requests and the submitted source. The twelve release runs support the reported 60/60 mandatory fields and 43.00% token reduction. The following findings concern contracts outside those measurements.

| Requirement | Finding | Acceptance condition for the repair |
|---|---|---|
| INV-001, FR-002 | The nine tradeable proposals in the release have an empty evidence identifier. The research graph omits the field used by the approval fingerprint. The other three runs produced no proposal. | The research path supplies a stable evidence identity. Changing material evidence invalidates the earlier approval in a normal research-to-review flow. |
| INV-001, INV-002 | Registration writes proposal state taken from the research package. Registering a known proposal can replace a terminal ledger record. | The ledger owns review and execution state. Repeat registration preserves the original rejection or execution and its audit record. |
| FR-001 | Replay can record a report-write error while the CLI prints success. Its file count can also include the completed report twice because it compares a path object with file name strings. | A report-write failure reaches the caller with a nonzero exit and a diagnostic. Successful reconstruction reports the files actually written. |
| D8, evaluator CLI | The judge command exposes a call budget that the judging function does not consult. | Enforce the advertised limit or remove the argument and document the number of calls. |
| D7, Gates 1 and 2 | A source-only change can reuse an old approval without a check that the new behavior falls within its scope. Gate 2 checks permissions and selected imports but has no distinct public API compatibility check for safety-related changes. | Check the changed behavior against the approved tests and verify the affected public interface on safety-related PRs. |
| D7, Gate 4 | The validator can omit an incorrectly shaped evidence record from a pair without recording a failure. Its provenance covers the extension but excludes the upstream graph and its role prompts. | Require six complete, validated pairs and cover the graph and prompt code used to generate them. |
| D7, Gate 6 | Path coverage comes from the union of past log entries. A historical entry can satisfy the path check for a new change. | Match changed paths to the evidence in the entry added or amended for that PR. |

The [supplementary replay check](../evaluation/replay-review/check_replay.py) ran the archived packages in fresh, network-guarded Python processes. All twelve signals matched and no network events were recorded. Its [observations](../evaluation/replay-review/observations.json) distinguish Hold results and proposals with no approved quantity. On sell proposals the CLI still labels the displayed limits as purchase bounds. Direction-specific bounds and an archived original policy result would permit a stronger comparison.

At the end of this review, the technical verdict was **CHANGES REQUIRED**. The [delivery checklist](process/delivery-checklist.md) tracks student attribution and early supervision evidence. The GitHub checks cited above apply to their published revisions.

## Review of the repaired submission

The technical review traced each finding above through the revised entry point and the unit case that would fail if the defect returned. Liyu MA requested the work in [U-08](../transcripts/leo-project-directions.md#u-08--submission-contracts-and-release). The implementation decisions and corresponding OpenCode sessions appear in the [annotated record](../transcripts/submission-repair/annotations.md).

| Finding | Resolution and evidence |
|---|---|
| Evidence identity and registration | Research and import derive an identifier from the saved research inputs. Registration preserves an existing operator decision when the terms are unchanged. A material change to a nonterminal proposal requires fresh review. Rejected and executed proposals retain their ledger records. [Registration and import tests](../test/offline/test_submission_runtime.py) |
| CLI failures and judge budget | Replay reports each written file once and exits with a diagnostic if reconstruction fails. Sell bounds use the owned quantity. Incomplete evaluation output and unsuccessful judgments produce a failing exit. A capped judge counts failed calls against the same allowance as successful calls. [CLI regression cases](../test/offline/test_submission_cli.py) |
| Approval and static checks | Gate 1 checks the scope and timing of the approval for each changed implementation path. Gate 2 checks whether existing callers of an affected public safety interface retain a valid call. [Approval cases](../test/offline/test_submission_governance.py) · [Interface cases](../test/offline/test_submission_api.py) |
| Research quality and provenance | Gate 4 requires a valid baseline and compact arm for every case. A malformed record blocks aggregation. The source fingerprint covers the upstream graph and role prompts as well as the extension. [Release-quality tests](../test/offline/test_release_quality.py) |
| AI-use log | Gate 6 matches changed code and runtime prompts to entries added or amended since the comparison branch. It verifies the prompt and native export for each new OpenCode entry. The local check passed against the published main baseline. [Gate implementation](../scripts/check_ai_use_log.py) · [Session register](ai-use-log.yaml) |

The [unit regression](../evaluation/submission-verification/unit-regression.txt) passed 649 upstream tests and 183 Research Desk tests. It also recorded 71 passing subtests. The upstream run skipped one test and deselected one.

The [earlier release](../evaluation/release/) retains the measurements and replay findings cited in the preceding review. The repaired application has its own [paired matrix and release decision](../evaluation/submission-release/aggregate/release-gate.json). The [evaluation logbook](architecture/evaluation-logbook.md) identifies the source and results for each experiment. Independent code-owner review of this submission belongs to its protected pull request.

On the first [submission-branch CI run](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/45031340237/job/137235399147), a long temporary path wrapped the incomplete-replay diagnostic. The revised unit case uses a 40-column terminal and checks the exit status, normalized diagnostic and missing filename. The protected [submission PR](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/3) lists the checks for the revised commit.

Verdict: **APPROVE** technical verification of the ADR-005 contracts; **CHANGES REQUIRED** before merge pending independent non-author code-owner review on [PR #3](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/3).

## Pull request #3 review record (pending independent code-owner sign-off)

- **Scope**: PR #3 (`submission-repairs` into `main`), implementing ADR-005 / FR-004 contract repairs and governance/documentation synchronization.
- **Specification alignment**: All 25 requirements pass schema and trace-matrix validation (`Gate 3`). FR-001–FR-004, INV-001/002, and CTX-001 are mapped to enforcing components, tests, and runtime monitors.
- **Architecture alignment**: The upstream TradingAgents v0.4.0 research graph remains intact. Proposal registration, exact-term approval, policy evaluation, and SQLite execution remain deterministic and outside LLM tool authority.
- **Code and test quality**: 832 unit tests and 71 subtests pass (`tests/` 649 passed + 71 subtests; `test/offline/` 183 passed). Dedicated regression modules verify proposal registration recovery (`test_submission_runtime.py`), CLI failure propagation and judge call budgets (`test_submission_cli.py`), public safety API compatibility (`test_submission_api.py`), scoped gate enforcement (`test_submission_governance.py`), and six-pair release provenance (`test_release_quality.py`).
- **Security and efficiency**: Zero external network calls during offline replay across all 12 submission packages (max 0.7922s); credentials read solely from host environment variables; no broker access; application tokens reduced by 42.50% (600,576 → 345,309) with 48.65% summed runtime ratio and 60/60 mandatory fields passing; coding-context study reduced observed tokens by 60.74% (60,409 → 23,719) across the same 26 passing tests.
- **Operational metadata**: All six required GitHub Actions checks passed on `submission-repairs`. Protected `main` requires passing CI and code-owner review (`enforce_admins: true`).
- **Independent code-owner reviewer**: `PENDING (wangsaorui or nicolas393 — to be completed on GitHub PR #3 before merge)`.
- **Independent review verdict**: `PENDING (APPROVE / CHANGES REQUIRED / REJECT to be recorded by the independent human reviewer)`.
