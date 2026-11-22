# Team responsibilities

Group 32 assigned each member a primary area and a review responsibility. At final review, Liyu MA confirmed that each member contributed one quarter of the work. [Contribution record](../../transcripts/leo-project-directions.md#u-13--architecture-discussion-and-final-contributions).

| Member | Primary responsibility | Review responsibility | Relative contribution |
|---|---|---|---:|
| Liyu MA (59072966) | Requirements, acceptance criteria and report integration | Architecture and release governance | 1.0 |
| Xinyao HENG (60106154) | Architecture, context budgets and GitHub release governance | Evidence, state contracts and packaging | 1.0 |
| Yinuo Li (60980401) | Evidence, proposal state and reproducible packaging | Evaluation and CI gates | 1.0 |
| Chengru WANG (60254685) | Unit tests, research evaluation and CI gates | Requirements, report consistency and submission completeness | 1.0 |

The four-person review rotation is Liyu MA → Xinyao HENG → Yinuo Li → Chengru WANG → Liyu MA. Each reviewer checks the next member’s area and records the actual findings and decision in the review memo.

Report integration and the submission checklist belong to Liyu MA. Xinyao HENG owns GitHub permissions and release coordination. Yinuo Li owns installation packaging and reproducibility materials. Chengru WANG owns the six CI gates. Each member retains an equal final weight of 1.0.

The recorded decision identifier leo refers to Liyu MA (59072966). The [annotated development record](../../transcripts/59072966-Liyu-MA.md) preserves that identity and the coordinating workflow’s role in sending prompts. Chengru WANG’s identity is recorded in [the member's own follow-up record](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/blob/9435dcbf0b3697bec8c30d0cb2d514ab255032f2/transcripts/60254685-Chengru-WANG.md). Liyu MA confirmed the remaining names and student numbers in the [student directions](../../transcripts/leo-project-directions.md).

## Requirement increments

| Increment | Contract | Evidence |
|---|---|---|
| Portable research evidence | FR-001, NFR-001 | Complete packages and zero-network replay |
| Reviewed paper transactions | FR-002, INV-001/002 | Exact-term approval and deterministic current-state checks |
| Measured context optimization | FR-003, COST-001, PERF-001 | Paired full-graph research and provider usage |
| Bounded model context | CTX-001, NFR-003 | Whole-input cap, compaction threshold and pre-request stop |
| Quality-controlled releases | GOV-003/004, QUALITY-001/002/003 | Current-source quality evidence and protected GitHub checks |
| Register and recover a proposal from a research package | FR-004, INV-001 | [Registration and recovery cases](../../test/offline/test_submission_runtime.py) for unchanged, revised and closed proposals |

The six increments include four new functional contracts. FR-004 was registered in the submission revision after the team reviewed the package-to-ledger workflow. The input budget and release-quality increments have their own non-functional criteria.

## Member account

| Member | GitHub account | Assigned area |
|---|---|---|
| Yinuo Li (60980401) | [nicolas393](https://github.com/nicolas393) | Evidence, proposal state and reproducible packaging |

Yinuo Li is assigned to the user-supplied account `nicolas393`. A repository invitation with write permission has been issued for this account. Yinuo Li reviews Chengru WANG’s evaluation and CI gates under the four-person rotation.

## GitHub reviewer

The user designated `wangsaorui` for GitHub review. The invitation has been accepted and write access is active. The [release review record](reviewer-onboarding.md) links the approval and merge on `main`. The account maps to **Chengru WANG** with formal student number **60254685**, and its independent approval of PR #1 is recorded in `docs/review-memo.md`.
