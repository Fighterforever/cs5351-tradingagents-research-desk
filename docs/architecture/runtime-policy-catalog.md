# Runtime policy catalog

| Trigger | Behavior | Evidence retained | Recovery |
|---|---|---|---|
| Provider request failure | Mark incomplete/failed; do not approve research | Actual request, error, usage received | Correct configuration or explicitly rerun the failed case |
| Context budget exhausted | Stop before provider invocation; no proposal | Estimate, configured cap and stop event | Narrow the requested evidence or explicitly revise the configured budget |
| Call budget exhausted | Stop before next request; no proposal | budget_stop event and all prior calls | Increase budget only as a documented experiment change |
| Missing frozen optional data | Return an explicit unavailable sentinel | Tool name, parameters and absence | Continue with unknown facts; never synthesize a source |
| Required package file absent | Reject replay | Named missing record | Re-export the complete source run |
| Future-only memory | Exclude from context | Cutoff and excluded record metadata | Use at an eligible later analysis date |
| Missing evidence price | Reject approval/execution | Proposal and reason | Obtain a complete research price record |
| Hold or REVIEW signal | No tradeable proposal | Saved report and terminal signal | Operator can inspect evidence; no execution shortcut |
| Unapproved or changed terms | REVIEW_REQUIRED, ledger unchanged | Current terms and approval reference | Review exact current terms again |
| Cash, total position or sell limit violation | Reject deterministic execution | Named policy checks | Choose permissible quantity and obtain approval |
| Repeat execution | Return original transaction | Stable transaction reference | No financial side effect |
| Semantic threshold failure | Fail applicable gate | Per-case facts/scores and reason | Correct the prompt or retain the previous release |
| Required review or CI missing | GitHub blocks the merge | Branch protection and PR check results | Complete the required checks and obtain the code-owner review |
