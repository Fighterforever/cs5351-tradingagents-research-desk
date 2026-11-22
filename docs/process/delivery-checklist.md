# Delivery checklist

| Requirement | Current evidence | Status |
|---|---|---|
| D1 requirements | 25 schema-valid requirements with fit criteria and trace links | Complete |
| D2 architecture | Blueprint, five ADRs, required design records and optional evaluation/risk/option artifacts | Complete |
| D3 coding governance | Effective plan/build/verify permissions, structural contracts and tool manifest | Complete |
| D4 verification | The [current unit run](../../evaluation/submission-verification/unit-regression.txt) passed 832 tests and 71 subtests. | The revised approval, compatibility, quality and AI-log gates have dedicated unit cases. |
| D5 supervised sessions | [Five complete annotated OpenCode sessions, direct decisions and the release review](../../transcripts/supervision-index.md) | Available evidence indexed; original early design deliberations and remaining student records to confirm |
| D6 report | Single report under 10,000 words; 12pt single-spaced PDF; four reflections of 300–500 words | All four identities recorded; members still need to confirm personal reflections and actual contributions |
| D7 GitHub | PR #1 merged after independent review. All six [main-branch jobs passed](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42798475065). | The [submission branch](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/tree/submission-repairs) carries the new contracts. Its pull request records the six checks and the independent review decision. |
| D8 source/tests | The repository includes the upstream source and tests, the Research Desk extension, its offline tests and the live evaluation. | The ADR-005 [registration and recovery cases](../../test/offline/test_submission_runtime.py) cover FR-004. The [submission review](../review-memo.md#submission-review) records the original findings. |
| D9 launch instruction | The [launch prompt](../../Prompt.md) calls for decisions on the proposed plan, completed build and verified release. | Complete. Each launch stops for approval before code generation. |
| Team scope | Four members and four new functional requirements, FR-001 to FR-004, plus context-budget and release-quality increments. | ADR-005 defines registration and recovery from a saved package. [Acceptance cases](../../test/offline/test_submission_runtime.py) exercise the persistent ledger decision. |
| Runtime efficiency | [42.50% fewer research tokens](../../evaluation/submission-release/aggregate/report.md), with 60/60 fields and all twelve individual assessments passing | Complete |
| Coding efficiency | Same maintenance task, 26 unit cases per condition, 60.74% fewer tokens | Complete paired study |

## Submission actions

The software evidence and roster are in place. The following records remain with the team.

1. Each member should review the personal reflection under their own name and confirm the assigned weight against completed work. The formal roster is complete.
2. Attach any retained student directions and early design discussion to the relevant stage in the [supervision index](../../transcripts/supervision-index.md).
3. The [protected submission PR](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/3) requests review from wangsaorui. The reviewer should inspect the latest diff and record their own verdict.
4. Upload the completed ten-minute MP4 separately from the project ZIP. It shows the recorded commands and the results of the submission experiment.
