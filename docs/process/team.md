# Team responsibilities

The project team uses the working names Alfa, Bravo, Charlie and Delta. The team has assigned equal responsibility for completing and reviewing the delivery. Relative contributions are 1.0 each, with an average of 1.0. These weights record the team's allocation rather than measured working hours.

| Member | Primary responsibility | Review responsibility | Relative contribution |
|---|---|---|---:|
| Alfa | Requirements, acceptance criteria and report integration | Architecture and release governance | 1.0 |
| Bravo | Architecture, context budgets and GitHub release governance | Evidence, state contracts and packaging | 1.0 |
| Charlie | Evidence, proposal state and reproducible packaging | Evaluation and CI gates | 1.0 |
| Delta | Unit tests, research evaluation and CI gates | Requirements, report consistency and submission completeness | 1.0 |

The four-person review rotation is Alfa → Bravo → Charlie → Delta → Alfa. Each reviewer checks the next member’s area and records the actual findings and decision in the review memo.

Report integration and the submission checklist belong to Alfa. Bravo owns GitHub permissions and release coordination. Charlie owns installation packaging and reproducibility materials. Delta owns the six CI gates. Each member retains an equal assigned weight of 1.0.

The recorded decision identifier leo refers to Liyu MA (59072966). The [annotated development record](../../transcripts/59072966-Liyu-MA.md) preserves that identity and the coordinating workflow’s role in sending prompts. The submission roster must connect each working name to its formal name and student number. Delta is now identified as `wangsaorui`, student number 60254685; the formal names and student numbers for Alfa, Bravo and Charlie remain with their owners to confirm.

## Five substantial requirement increments

| Increment | Contract | Evidence |
|---|---|---|
| Portable research evidence | FR-001, NFR-001 | Complete packages and zero-network replay |
| Reviewed paper transactions | FR-002, INV-001/002 | Exact-term approval and deterministic current-state checks |
| Measured context optimization | FR-003, COST-001, PERF-001 | Paired full-graph research and provider usage |
| Bounded model context | CTX-001, NFR-003 | Whole-input cap, compaction threshold and pre-request stop |
| Quality-controlled releases | GOV-003/004, QUALITY-001/002/003 | Current-source quality evidence and protected GitHub checks |

These increments include functional and non-functional requirements. They share the existing graph and preserve upstream responsibilities.

## Member account

| Working name | GitHub account | Assigned area |
|---|---|---|
| Charlie | [nicolas393](https://github.com/nicolas393) | Evidence, proposal state and reproducible packaging |

Charlie is assigned to the user-supplied account `nicolas393`. A repository invitation with write permission has been issued for this account. Charlie reviews Delta’s evaluation and CI gates under the four-person rotation.

## GitHub reviewer

The user designated `wangsaorui` for GitHub review. The invitation has been accepted and write access is active. The [onboarding record](reviewer-onboarding.md) explains activation on `main` and the independent review sequence. The account maps to working name **Delta** with formal student number **60254685**, and its independent approval of PR #1 is recorded in `docs/review-memo.md`.
