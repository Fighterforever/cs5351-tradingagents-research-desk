# Release revision interventions

Decision identifier: leo. This record links the current user-authorized revision to actual native OpenCode sessions. The five working team names and review allocation are documented in docs/process/team.md; archived tool operations retain their recorded operator.

| Intervention | Rationale | Native evidence |
|---|---|---|
| Approve ADR-004 and concrete acceptance cases before source edits | Correct the observed rejection-state, report-contract and context-budget gaps | docs/process/revision-authorization.md; project-revision-runtime.raw.jsonl |
| Split runtime, context and quality-gate ownership | Keep overlapping source changes sequential and focused | project-revision-runtime.full.json; project-revision-context.full.json; project-revision-quality.full.json |
| Replace repeated exploration with bounded follow-up prompts | Direct the agent to declared interfaces and exact failing contracts | prompts/project-revision-slice.md; prompts/project-quality-implementation.md; prompts/project-gate-fixes.md |
| Preserve model narrative while rendering identity from evidence | Correct the generic output contract without case-specific answers | prompts/project-report-contract.md; project-revision-runtime.full.json |
| Require separate support and relevance checks plus source provenance | Prevent stale outputs or an average score from concealing a regression | project-revision-gates.full.json |
| Finish only concrete static findings | End implementation after the accepted behavior and checks pass | project-revision-static.full.json |
| Remove temporary revision permissions | Restore the accepted build boundary after source freeze | opencode.json; .opencode/permissions.jsonc |

The complete final experiment is recorded under evaluation/release. Approval records authorize work; measured results come from the saved commands and provider responses.
