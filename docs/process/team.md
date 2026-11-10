# Team responsibilities

The project team uses the working names Alfa, Bravo, Charlie, Delta and Echo. The team has assigned equal responsibility for completing and reviewing the delivery. Relative contributions are 1.0 each, with an average of 1.0. These weights record the team's allocation rather than measured working hours.

| Member | Primary responsibility | Review responsibility | Relative contribution |
|---|---|---|---:|
| Alfa | Requirements, scope and acceptance criteria | Traceability and final submission checklist | 1.0 |
| Bravo | Architecture, context layers and input budget | Evidence and runtime boundary design | 1.0 |
| Charlie | Evidence packages and proposal state machine | Integration and persistent-state contracts | 1.0 |
| Delta | Unit tests and research-quality evaluation | Negative cases and experimental comparisons | 1.0 |
| Echo | CI, release controls and report integration | Reproducibility and delivery packaging | 1.0 |

For the final review, ownership rotates one row forward: Alfa reviews Bravo's architecture, Bravo reviews Charlie's state contracts, Charlie reviews Delta's tests, Delta reviews Echo's CI evidence, and Echo reviews Alfa's requirements. Record each completed review with its actual author and result in the review memo. Completed reviews become part of the contribution record.

The recorded decision identifier leo refers to Liyu MA (59072966). The [annotated development record](../../transcripts/59072966-Liyu-MA.md) preserves that identity and the coordinating workflow’s role in sending prompts. The submission roster must connect each working name to its formal name and student number.

## Five substantial requirement increments

| Increment | Contract | Evidence |
|---|---|---|
| Portable research evidence | FR-001, NFR-001 | Complete packages and zero-network replay |
| Reviewed paper transactions | FR-002, INV-001/002 | Exact-term approval and deterministic current-state checks |
| Measured context optimization | FR-003, COST-001, PERF-001 | Paired full-graph research and provider usage |
| Bounded model context | CTX-001, NFR-003 | Whole-input cap, compaction threshold and pre-request stop |
| Quality-controlled releases | GOV-003/004, QUALITY-001/002/003 | Current-source quality evidence and protected GitHub checks |

These increments include functional and non-functional requirements. They share the existing graph and preserve upstream responsibilities.

## GitHub reviewer

The user designated `wangsaorui` for GitHub review. A write-access invitation has been issued. The [onboarding record](reviewer-onboarding.md) explains activation on `main` and the independent review sequence. The account’s formal student identity and working-name mapping remain unassigned.
