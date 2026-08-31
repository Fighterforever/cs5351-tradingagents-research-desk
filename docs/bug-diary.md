# Significant defect diary

## Packaging entry point

Symptom: the first research-desk invocation could not import its package. Reproduction: install editable metadata, run the CLI help. Classification: integration/configuration. Root cause: the new src-layout package was absent from the package discovery contract. OpenCode corrected pyproject package configuration. Verification: the actual CLI help and full offline vertical slice run successfully. Exposed gap: module existence is insufficient without an installable public entry point.

## Baseline/compact assembly

Symptom: early context tests failed and baseline could reference an uninitialized deduplication counter. Reproduction: assemble baseline and compact with repeated memory paragraphs. Classification: implementation/control flow. Root cause: compaction bookkeeping was not initialized consistently, while the two modes did not express the intended preservation difference. OpenCode corrected the branches. A further review found that compressing only past memory would barely affect fresh research runs; the follow-up task moved compaction to actual per-agent input. Exposed gap: passing local transformation tests does not establish a useful optimization on the real workload.

## Re-review state

Symptom: a stale or unapproved proposal entered REVIEW_REQUIRED but could not be approved after correction. Reproduction: execute before approval, then review the current terms. Classification: business-state transition. Root cause: the approval path treated a recovery state as terminal. OpenCode allowed a fresh review while keeping SIMULATED and REJECTED behavior explicit. Verification: test_reapprove_after_review_required. Exposed gap: a fail-closed response needs a supported recovery path.

## Ticket cap versus total position

Symptom found by code inspection: evaluate_buy compared one order value to equity while ignoring existing shares in the same ticker. Reproduction: execute two individually permissible purchases whose total exceeds10% equity. Classification: business invariant. Root cause: the policy's unit of analysis was a ticket rather than resulting holdings. ADR-002 directs a ticker-aware current-position check. Exposed gap: an exact-cap test on an empty portfolio cannot establish a portfolio invariant.

## Incomplete approval binding and sales

Symptom found by code inspection: the approved content fingerprint omitted shares and evidence identity; create_proposal also rejected Sell/Underweight unconditionally. Reproduction: change quantity after approval, or attempt to sell an owned position. Classification: authority contract / normalized business behavior. Root cause: a simplified buy-only slice was not equivalent to the approved no-short policy. ADR-002 defines exact terms and valid bounded sales. Final completion is determined by the corrected test suite.

## Callback budget boundary

Risk found during integration review: callback exceptions can be swallowed, and structured-output fallback can retry after a budget exception. The unit test of BudgetTracker alone cannot establish the no-next-request invariant. The follow-up task requires a fake provider invocation through the real adapter path and a request boundary that prevents the extra call. The final test log records the actual outcome; this entry does not manufacture an observed live overrun.

## Complete upstream configuration

The first actual evaluate-case AAPL launch failed before a model request with KeyError:data_cache_dir. The evaluation helper supplied an override dictionary, while TradingAgentsGraph treats a supplied config as complete. OpenCode changed the evaluation configuration owner to deep-copy the real DEFAULT_CONFIG, then apply model settings and project-local cache/results/memory paths. A real graph-construction smoke test used a non-secret dummy token without an API request. This uncovered an integration contract that fake graph tests had not exercised.

## Real message serialization and overbroad redaction

The next AAPL pilot completed the full research graph:15 model requests/responses,27 tool calls/results, Hold,141.522 seconds in its run_end event. Export then failed at final_state.json because the merged real state contained a LangChain HumanMessage. The complete report and early package files survived under evaluation/pilot/AAPL/baseline/.home/runs/run-52aa20b7d9a8, but the package was incomplete and cannot serve as the final evaluation sample.

Inspection also found that sanitize_secrets matched the fragment "token" and replaced input_tokens/output_tokens with a redaction marker. That confused usage measurements with authentication secrets. The approved repair belongs in evidence.py: serialize actual model/message structures recursively and redact credential fields precisely while retaining numeric usage. A real-message export/import regression must cover this boundary. The pilot's lost token measurements are not reconstructed by estimation. The final experiment uses corrected evidence capture and retains the failed attempt.

## Shared context did not reach every research role

The first complete two-case comparison recorded36.07% fewer application tokens in compact mode, yet both variants produced zero cited claims. The MSFT compact report also introduced a forward valuation multiple absent from the fixed corpus. Inspection found that the standing constraints were placed in initial past_context, while several downstream upstream roles consumed different state fields. The repair belongs at the real model-request boundary. The same grounding layer reaches plain, tool-bound and structured calls in baseline and compact. The baseline history remains uncompressed; the compact target remains unchanged. Initial outputs are retained, and a new prompt version is evaluated on the two development cases before the four reserved cases.

## Evaluation must inspect the output it claims to score

Review found that frozen_price_used checked the existence of the price in input evidence instead of its presence in the generated report. The corrected deterministic check requires both. A separate report-assembly issue flattened role stages and repeated the same terminal field, which could misrepresent disagreement as an inconsistent single final answer. The permitted repair retains actual role headings and removes only an identical duplicate terminal field. Raw generated text, dissent, judge model, rubric and thresholds remain unchanged. The additional negative examples use missing and incorrect report prices; the original development evaluation artifacts are not rewritten.
