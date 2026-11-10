# Invariant register

| ID | Requirement | Statement | Enforcer | Verification | Operational fallback |
|---|---|---|---|---|---|
| I-AUTH | INV-001 | Ledger mutations require exact approved terms | review, storage | AT-03/05 | Keep ledger unchanged; set REVIEW_REQUIRED and request a fresh review |
| I-POLICY | INV-002 | Cash stays nonnegative and sells never exceed owned shares. A buy must leave total ticker holdings at or below 10% of current equity; a valid sale may reduce an already overweight holding even if it remains above the cap. | policy | AT-04/05 | Reject transaction and retain named failed checks |
| I-ADVISORY | INV-002 | Research cannot grant itself approval or execute | graph_adapter, CLI boundary | AT-04 | Treat model instructions as report text; never route them to review/execute |
| I-COMPLETE | FR-001 | A complete package has the records required for replay | evidence | AT-01 | Reject incomplete replay; preserve partial run for diagnosis |
| I-CUTOFF | SEC-001 | Historical inputs are eligible at the analysis cutoff | context, frozen corpus | AT-02 | Exclude ineligible records and mark unknown availability |
| I-BUDGET | NFR-003 | No request starts after the configured call limit | budget, actual model boundary | AT-06 | Stop graph, record budget_stopped and produce no tradeable proposal |
| I-CONTEXT | CTX-001 | Complete model inputs stay within the configured conservative cap | budget, request delegate | AT-06 context unit tests | Stop before the provider request; retain context_budget_exhausted evidence and no proposal |
| I-USAGE | FR-003 | Cost claims use actual provider usage | evidence, evaluation | AT-07 | Mark missing usage and exclude no failure silently; rerun only with a recorded reason |
| I-REPLAY | NFR-001 | Replay never initiates an external request | replay | AT-01 | Fail test on any attempted socket/model call |

Zero tolerance applies to safety escapes. A failed quality or performance target is a reported experiment result and does not authorize weakening these invariants.
