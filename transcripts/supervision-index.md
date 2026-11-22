# Supervised development evidence

This index connects project decisions, five complete OpenCode sessions and the independent release review. It links each record to its scope and outcome.

## Direct team decisions and review

| Evidence | Decision and reason | Outcome |
|---|---|---|
| [Project scope and release review](leo-project-directions.md#u-01--working-aliases-video-scope-exclusion-and-gemini-cli-assessment) (U-01) | The student directed the team to complete the reviewed non-video scope and obtain a separate technical assessment. | [Revision authorization](../docs/process/revision-authorization.md) and [ADR-004](../docs/architecture/adr/004-release-quality-and-context-budget.md) define the resulting work. |
| [Repository visibility](leo-project-directions.md#u-03--public-repository-visibility-and-history-publication) (U-03) | The student authorized publishing the project repository and history after the private repository blocked hosted checks and branch protection. | The repository became public. [Recorded branch policy](../evaluation/github/branch-protection-current.json). |
| [Recordkeeping and technical review](leo-project-directions.md#u-05--source-linked-intervention-annotations-clear-prose-and-re-review) (U-04 through U-06) | The student asked for concise commit messages, source-linked annotations and a Gemini review of the existing work. | The [intervention index](intervention-index.json) links original prompts to outcomes. The [technical review](../docs/process/pipeline-review.md) evaluates requirements and architecture after implementation. |
| [Four-person allocation](leo-project-directions.md#u-07--four-person-team-allocation) (U-07) | The student changed the team to four and directed redistribution of the former fifth role's work. | The [responsibility and review table](../docs/process/team.md) records the four areas. |
| [Delta's release approval](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/1#pullrequestreview-5840085663) (R-01) | Chengru WANG (`wangsaorui`) reviewed PR #1. The review memo records the gate and architecture checks, limitations of the inspection and the Python version coverage finding. | The reviewer approved PR #1, the PR merged, and all six [main-branch CI checks](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42798475065) passed. [Review memo](../docs/review-memo.md#independent-code-owner-review-of-pr-1). |

The [directives appendix](leo-project-directions.md) identifies the student who issued the recorded project directions. Delta's approval also has a [saved GitHub receipt](../evaluation/github/pr-1-release.json).

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
- The [requirements registry](../docs/req/requirements.yaml), [candidate comparison](../docs/architecture/evaluation-table.md) and [architecture decision](../docs/architecture/adr/001-application-extension.md) record design choices. The [recorded Gemini assessment](gemini-pipeline-review.json) is a later technical review of these materials. An original human discussion of the candidate scores is still needed to document that part of early supervision.
- [Delta’s annotated Qoder session](60254685-Chengru-WANG.md) is included as published in [PR #2](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/9435dcbf0b3697bec8c30d0cb2d514ab255032f2/transcripts/60254685-Chengru-WANG.md). Its workflow links and conclusions describe the PR branch. The six required checks passed there. The advisory matrix completed on Python 3.12 and 3.13 and stopped at dependency installation on 3.10 and 3.11. [PR #2](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/2) awaits review. The original Qoder conversation remains in the member’s client.

## Submission repair

Alfa requested a repair after the submission audit found missing evidence identity and problems in registration, replay and release validation. [U-08 through U-11](leo-project-directions.md#u-08--submission-contracts-and-release) record the scope and provider decision together with the roster confirmations. OpenCode returned the [planning session](submission-repair/plan.full.json). The [annotated repair sessions](submission-repair/annotations.md) record why the work changed and where the new evidence appears. The coordinating workflow selected the specific acceptance conditions under Alfa’s delegated authority before implementation. [ADR-005](../docs/architecture/adr/005-submission-contracts.md) records the decision.
