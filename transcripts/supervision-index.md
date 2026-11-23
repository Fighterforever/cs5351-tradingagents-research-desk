# Supervised development evidence

The five sessions below follow the project from the first implementation to a release revision prompted by failed checks. Each annotation links a decision to the original message and the change that followed.

## Direct team decisions and review

| Evidence | Decision and reason | Outcome |
|---|---|---|
| [Project scope and release review](leo-project-directions.md#u-01--working-aliases-video-scope-exclusion-and-gemini-cli-assessment) (U-01) | The student directed the team to complete the reviewed non-video scope and obtain a separate technical assessment. | [Revision authorization](../docs/process/revision-authorization.md) and [ADR-004](../docs/architecture/adr/004-release-quality-and-context-budget.md) define the resulting work. |
| [Repository visibility](leo-project-directions.md#u-03--public-repository-visibility-and-history-publication) (U-03) | The student authorized publishing the project repository and history after the private repository blocked hosted checks and branch protection. | The repository became public. [Recorded branch policy](../evaluation/github/branch-protection-current.json). |
| [Recordkeeping and technical review](leo-project-directions.md#u-05--source-linked-intervention-annotations-clear-prose-and-re-review) (U-04 through U-06) | The student asked for concise commit messages, source-linked annotations and a Gemini review of the existing work. | The [intervention index](intervention-index.json) links original prompts to outcomes. The [technical review](../docs/process/pipeline-review.md) evaluates requirements and architecture after implementation. |
| [Four-person allocation](leo-project-directions.md#u-07--four-person-team-allocation) (U-07) | The student changed the team to four and directed redistribution of the former fifth role's work. | The [responsibility and review table](../docs/process/team.md) records the four areas. |
| [Chengru WANG's release approval](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/1#pullrequestreview-5840085663) (R-01) | Chengru WANG (`wangsaorui`) reviewed PR #1. The review memo records the gate and architecture checks, limitations of the inspection and the Python version coverage finding. | The reviewer approved PR #1, the PR merged, and all six [main-branch CI checks](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42798475065) passed. [Review memo](../docs/review-memo.md#independent-code-owner-review-of-pr-1). |

The [directives appendix](leo-project-directions.md) identifies the student who issued the recorded project directions. Chengru WANG's approval also has a [saved GitHub receipt](../evaluation/github/pr-1-release.json).

## Five annotated native sessions

Each row pairs a complete OpenCode export with its annotations. The coordinating workflow supplied the implementation instructions under the delegated project scope. The [message index](intervention-index.json) gives the session ID, message ID and exact position of each quoted instruction. Annotations explain the observed problem, why the instruction changed the work and what followed.

| Session | Original export | Annotations | Evidence of the development process |
|---|---|---|---|
| 1. Initial implementation | [project-01.full.json](project-01.full.json) | [I-01](annotations/leo-session-1.md) | Begins from the upstream baseline and builds the first offline slice under the recorded plan and tests. |
| 2. Contract correction | [project-02.full.json](project-02.full.json) | [I-02](annotations/leo-session-2.md) | Corrects the cumulative position cap and approval binding after review and defines the fixed evaluation inputs. |
| 3. Graph and live evaluation | [project-04.full.json](project-04.full.json) | [I-03 through I-07](annotations/leo-session-3.md) | Preserves tool-call pairs, restores the full graph configuration and checks valid sales and judgment inputs. |
| 4. Blocking verification | [project-ci.full.json](project-ci.full.json) | [I-08 through I-13](annotations/leo-session-4.md) | Implements the six gates and captures the rejection outcomes for targeted violations. |
| 5. Release revision | [project-revision-runtime.full.json](project-revision-runtime.full.json) | [I-21 through I-24](annotations/08-release-revision.md#i-21-set-the-release-revision-scope) | Uses failed quality and state checks to scope corrective work in ADR-004. Separate sessions cover the input budget and provider request settings. |

The [complete development index](59072966-Liyu-MA.md) covers 30 directives across 11 native sessions. Entries I-14 through I-20 cover evidence capture, grounding and judging. Entries I-25 through I-30 cover request context and provider transport.

## Planning and later review

- The [initial approval packet](../docs/process/APPROVAL_PACKET.md#决策记录) and [test approval record](../docs/process/test-approval.yaml) place plan and test acceptance before the first implementation. The coordinating workflow made the specific plan and test decisions under delegated authority. The [first implementation prompt](prompts/project-01-offline.md) cites the approval before work begins.
- The [requirements registry](../docs/req/requirements.yaml), [candidate comparison](../docs/architecture/evaluation-table.md) and [architecture decision](../docs/architecture/adr/001-application-extension.md) record design choices. The [recorded Gemini assessment](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/a1af194bbd1540c0ae2a11c1395269c52e02dfec/transcripts/gemini-pipeline-review.json) is a later technical review of these materials. Liyu MA later identified the two students who advocated different options. Their retrospective account appears below.
- [Chengru WANG’s annotated Qoder session](60254685-Chengru-WANG.md) uses the member’s formal name. The original was published in [PR #2](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/9435dcbf0b3697bec8c30d0cb2d514ab255032f2/transcripts/60254685-Chengru-WANG.md). Its workflow links and conclusions describe the PR branch. The six required checks passed there. The advisory matrix completed on Python 3.12 and 3.13 and stopped at dependency installation on 3.10 and 3.11. [PR #2](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/2) awaits review. The original Qoder conversation remains in the member’s client.

### Decisions that can be traced to a person

| Decision | Evidence and consequence |
|---|---|
| Liyu MA asked for approval and registration repairs | [U-08](leo-project-directions.md#u-08--submission-contracts-and-release) names the two failing workflows. The [repair annotations](submission-repair/annotations.md) connect that direction to the plan and acceptance cases. [ADR-005](../docs/architecture/adr/005-submission-contracts.md) records the revised contracts. |
| Chengru WANG approved the CI follow-up plan and kept the version matrix advisory | In [D5-02 and D5-03](60254685-Chengru-WANG.md), Chengru WANG explains why the first four-version run should inform future policy. The [resulting pull request](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/2) preserves the workflow change separately from the six required checks. |

For the initial architecture choice, the [candidate table](../docs/architecture/evaluation-table.md) gives the application extension 4.65 out of 5. Editing the core and replacing the graph each scored 3.10. The planning workflow assigned those scores under delegated authority. [ADR-001](../docs/architecture/adr/001-application-extension.md) records the resulting choice. In [Liyu MA’s retrospective account](leo-project-directions.md#u-13--architecture-discussion-and-final-contributions), Liyu MA advocated retaining the upstream graph and Xinyao HENG advocated editing it directly. The table gives direct edits the highest evidence-capture score (5/5) and the extension the highest baseline-preservation score (5/5). These are the planning workflow’s recorded engineering reasons.

Liyu MA also recalled Yinuo Li checking offline replay and approval persistence. The [replay case](../test/offline/test_at01_replay.py) and the [unchanged-registration case](../test/offline/test_submission_runtime.py) identify the behaviors Yinuo Li checked. Attribution comes from Liyu MA’s account above.

## Submission repair

Liyu MA requested a repair after the submission audit found missing evidence identity and problems in registration, replay and release validation. [U-08 through U-11](leo-project-directions.md#u-08--submission-contracts-and-release) record the scope and provider decision together with the roster confirmations. OpenCode returned the [planning session](submission-repair/plan.full.json). The [annotated repair sessions](submission-repair/annotations.md) record why the work changed and where the new evidence appears. The coordinating workflow selected the specific acceptance conditions under Liyu MA’s delegated authority before implementation. [ADR-005](../docs/architecture/adr/005-submission-contracts.md) records the decision.

## Archived copies and published paths

The complete OpenCode exports are included in the submission. The earlier public revision holds seven auxiliary event streams with their original capture timestamps. The corresponding exports contain every message part from those streams.

| Archived stream | Complete session |
|---|---|
| [project-01.raw.jsonl](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/project-01.raw.jsonl) | [project-01.full.json](project-01.full.json) |
| [project-02.raw.jsonl](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/project-02.raw.jsonl) | [project-02.full.json](project-02.full.json) |
| [project-04.raw.jsonl](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/project-04.raw.jsonl) | [project-04.full.json](project-04.full.json) |
| [project-06.raw.jsonl](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/project-06.raw.jsonl) | [project-04.full.json](project-04.full.json) |
| [project-ci.jsonl](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/project-ci.jsonl) | [project-ci.full.json](project-ci.full.json) |
| [project-permissions.jsonl](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/project-permissions.jsonl) | [project-permissions.full.json](project-permissions.full.json) |
| [project-revision-transport.raw.jsonl](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/project-revision-transport.raw.jsonl) | [project-revision-transport.full.json](project-revision-transport.full.json) |

These prompt copies are also available in the earlier revision. Their inputs appear in the retained exports.

- [project-ci-finalize.md](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/prompts/project-ci-finalize.md) → [project-ci.full.json](project-ci.full.json), `/messages/77/parts/1/text`.
- [plan.txt](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/submission-repair/plan.txt) → [plan.full.json](submission-repair/plan.full.json), `/messages/0/parts/0/text`.
- [records-confirmed.txt](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/transcripts/submission-repair/records-confirmed.txt) → [records-confirmed.full.json](submission-repair/records-confirmed.full.json), `/messages/0/parts/0/text`.

Four historical test records use `<LOCAL_PYTHON>` for the machine-specific interpreter directory. Their original copies below preserve the exact original paths.

- [check_static.stdout.txt](../evaluation/ci-initial/check_static.stdout.txt) · [Original](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/evaluation/ci-initial/check_static.stdout.txt)
- [negative-examples.json](../evaluation/ci-initial/negative-examples.json) · [Original](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/evaluation/ci-initial/negative-examples.json)
- [focused-regression-before-fixture.txt](../evaluation/development-cost/context-study/focused-regression-before-fixture.txt) · [Original](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/evaluation/development-cost/context-study/focused-regression-before-fixture.txt)
- [full-regression-before-fixture.txt](../evaluation/development-cost/context-study/full-regression-before-fixture.txt) · [Original](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/cdf64b674d8007ab438b44b37274fac6e5fe6265/evaluation/development-cost/context-study/full-regression-before-fixture.txt)
