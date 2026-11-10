# ADR-004: Bound context and gate release quality

Status: accepted by leo. Scope: the user-authorized project completion revision.

## Drivers and decision

The final review found a rejected proposal could be reopened by an execution attempt, a missing legal company name, an incorrect quarterly-EPS valuation interpretation, and quality evidence disconnected from merge checks. This revision preserves the original graph and fixed corpus while closing these contracts.

Rejected proposals remain rejected after execution attempts. Review-required recovery applies to pending or previously approved proposals whose terms or current portfolio need another review. The CLI never silently reopens a rejection.

Every model request receives a finite input budget with an earlier compaction threshold. Context assembly retains system constraints, current task, factual evidence and complete assistant/tool groups. It removes or compacts older expendable prose first. If required material still exceeds the cap, the run stops before a provider request and cannot produce an approvable proposal. A conservative UTF-8 byte-based token upper bound may enforce the cap without adding an unpinned model tokenizer; provider usage remains the source for measured cost.

The research output includes a deterministic identity/date/evidence-price section. It renders actual frozen data and complements the generated reasoning. The evaluator checks both this output contract and the generated factual reasoning. Derived valuation metrics must name the earnings period and cannot label a quarterly-EPS ratio as trailing P/E.

The semantic gate keeps offline regression and additionally validates current six-case paired live results against declared quality thresholds. Evidence records a source fingerprint for immutable provenance, not a public version identifier. Changes to runtime code, prompts, frozen data or evaluator invalidate stale evidence. A failed or missing result blocks the gate. Prior experiments remain archived.

## Alternatives and consequences

Ticker-specific output edits would overfit one case. Post hoc score edits would disconnect evidence from execution. A prompt-only length instruction cannot impose a hard context bound. Replaying old successful outputs cannot validate a new prompt. The selected design uses explicit output construction, request-boundary budget enforcement and source-bound quality evidence.

Context bounds can stop a run containing too much mandatory evidence. That is an observable incomplete outcome, with the original evidence retained. Reopen this decision if a supported tokenizer enables a tighter bound or larger corpora require hierarchical evidence selection.

## Affected paths

`src/research_desk/policy.py` (docstring cleanup only), `src/research_desk/review.py`, `src/research_desk/config.py`, `src/research_desk/budget.py`, `src/research_desk/context.py`, `src/research_desk/graph_adapter.py`, `src/research_desk/report.py`, `src/research_desk/eval/live.py`, `src/research_desk/eval/compact_delegate.py`, `src/research_desk/models.py`, `scripts/check_semantic.py`, `scripts/check_approval.py`, `scripts/check_static.py`, `scripts/check_permissions.py`, `scripts/check_gate_examples.py`, `.opencode/permissions.jsonc`, `opencode.json`, `.opencode/rules.md`, `.agent/rules.md`.

## Acceptance examples

- Reject, attempt execution, then attempt approval: status remains REJECTED and approval fails.
- Below threshold: preserve input. Above threshold: compact old prose while preserving critical facts and assistant/tool pairing. Mandatory content above cap: stop before model invocation.
- Every fixed-case report states its actual legal name, analysis date and evidence price. Quarterly EPS is never labeled TTM earnings.
- Missing, stale or below-threshold live evidence fails the semantic gate. Current complete passing evidence succeeds.

## Provider transport correction

The first revision experiment returned reasoning despite the requested thinking-disabled flag. All twelve judge responses reached the output cap before producing a structured score. Host-side parameter diagnosis found that the authorized endpoint honors `reasoning_effort: none`. The evaluation adapter now sends this setting in the provider request body alongside the standard thinking-disabled flag. This preserves the same model, output cap and scoring rubric in both arms. The failed matrix remains archived; the corrected transport requires a fresh complete matrix.
