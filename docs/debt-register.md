# Technical debt register

| Category | Observed debt | Decision / owner | Trigger or closure evidence |
|---|---|---|---|
| Prompt rot | Upstream roles repeat instructions and prior reports | Compact wrapper, leo | Fixed-set quality/cost comparison after prompt changes |
| Hallucinated dependencies | Initial package/schema assumptions needed correction | Verify actual pyproject and installed APIs | CLI import and declared-interface tests |
| Untouchable code | Upstream graph has broad functionality | Preserve upstream; narrow adapter seams | Full upstream regression suite |
| Hidden dependencies | Identity/returns paths bypass tool callbacks | Explicit subclass capture/freeze | Integration tests and captured direct reads |
| Agent-induced bloat | First session continued cleanup after47 passing tests | Ended session, issued short live-focused prompt | Archived session boundary and intervention |
| Evaluation debt | Offline fixture success initially lacked live cost/quality | Six paired fixed-corpus runs | Final evaluation artifacts |
| Guardrail debt | Initial ticket cap and quantity-free approval binding | ADR-002 corrections | Total-holding, valid-sell and changed-quantity cases |
| Human/cognitive debt | Large generated context obscured the next objective | Separate bounded code, CI, documentation and video work | Short prompts, trace matrix, measured milestones |

No item is closed merely because a document exists. The final report identifies evidence-backed closure and any remaining release limitation.

## Current disposition

ADR-004 closes the rejected-state transition and complete-input budget gaps. The current-source matrix passes all 60 mandatory fields and every semantic threshold. Source-bound release validation closes the stale-evidence path. The provider transport mismatch is corrected and its failed matrix remains archived. Public GitHub checks and branch protection are active.

Broader corpus coverage and authenticated multiuser deployment remain future scope. Coding context cost is measured in evaluation/development-cost. The team roster and independent merge review are tracked in the delivery checklist.
