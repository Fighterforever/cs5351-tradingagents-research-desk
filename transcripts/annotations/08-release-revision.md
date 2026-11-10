# Release contracts and context budgets

Seven prompts across three sessions implemented the approved release revision. They covered proposal state, report identity, context budgets and release acceptance.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-21: Set the release revision scope

Release review identified four remaining issues: execution attempts mutating rejected proposals, missing whole-input context caps, quarterly-to-TTM EPS confusion, and retirement of `deepseek-v4-flash` in the provider catalog.

> Use the current deepseek-flash model consistently in new runtime experiments and judge; retain historical model labels in archived records. Do not compare a new arm against an old-model arm.

Establishing the ADR-004 requirements and migrating both experimental arms and the judge to `deepseek-flash` ensured consistent model comparisons and clear module boundaries for the release revision.

In this initial turn, OpenCode read the revision authorization, ADR-004, and the runtime module declarations to prepare the bounded patches executed in the subsequent turns.

Result: [config.py](../../src/research_desk/config.py), [review.py](../../src/research_desk/review.py), [context.py](../../src/research_desk/context.py), [live.py](../../src/research_desk/eval/live.py).

Source: [project-revision-runtime.full.json](../project-revision-runtime.full.json), message `msg_1c0ac015a001go87a2Fh2EiOcv`, JSON pointer `/messages/0`. Session: `ses_e3f53febfffeJxqxKnMdRFfCgx`.

Prompt: [project-revision-runtime.md](../prompts/project-revision-runtime.md).

## I-22: Correct rejection state and EPS semantics

Following code inspection in the revision session, the coordinator narrowed the immediate patch to rejected-proposal immutability, quarterly-versus-TTM EPS rules, `deepseek-flash` config constants, and judge `semantic_valid` scoring.

> Before any version or generic status check in execute, if status REJECTED return ExecutionRecord(executed=False,reason='proposal rejected') without changing status or store. Keep approve rejecting REJECTED.

Splitting these four runtime and schema edits into a focused slice prevented terminal `REJECTED` proposals from reopening and required the judge to fail reports with period or unit errors.

OpenCode updated `review.py`, `config.py`, `context.py`, and `eval/live.py`, wrote `prompts/runtime-prompts-v0.1.2.yaml`, and added unit tests in `test/offline/test_revision_contracts.py`.

Result: [review.py](../../src/research_desk/review.py), [config.py](../../src/research_desk/config.py), [context.py](../../src/research_desk/context.py), [live.py](../../src/research_desk/eval/live.py), [runtime-prompts-v0.1.2.yaml](../../prompts/runtime-prompts-v0.1.2.yaml), [test_revision_contracts.py](../../test/offline/test_revision_contracts.py).

Source: [project-revision-runtime.full.json](../project-revision-runtime.full.json), message `msg_1c0afbfbb001ORSPNsMkXsRB7J`, JSON pointer `/messages/20`. Session: `ses_e3f53febfffeJxqxKnMdRFfCgx`.

Prompt: [project-revision-slice.md](../prompts/project-revision-slice.md).

## I-23: Render identity from the evidence package

User-facing reports and judge inputs needed a consistent, evidence-backed header presenting legal company identity, ticker, analysis date, and frozen close price without altering raw model narratives.

> Define ONE reusable render_research_identity(pack) helper in report.py. It renders identity/date/evidence close with source attribution. Include the same header in the actual user-visible complete_report.md and run summary, not only inside the evaluator.

Composing the identity header directly from `EvidencePack` fields across live export, offline replay, and judge preparation guaranteed uniform report presentation while leaving raw reasoning intact for semantic evaluation.

OpenCode implemented `render_research_identity` and `apply_research_identity_header` in `src/research_desk/report.py`, integrated them into `graph_adapter.py`, `replay.py`, and `eval/live.py`, and added `test/offline/test_report_contract.py`.

Result: [report.py](../../src/research_desk/report.py), [graph_adapter.py](../../src/research_desk/graph_adapter.py), [replay.py](../../src/research_desk/replay.py), [live.py](../../src/research_desk/eval/live.py), [test_report_contract.py](../../test/offline/test_report_contract.py).

Source: [project-revision-runtime.full.json](../project-revision-runtime.full.json), message `msg_1c0b752e3001K3XI43qZM4bsPU`, JSON pointer `/messages/48`. Session: `ses_e3f53febfffeJxqxKnMdRFfCgx`.

Prompt: [project-report-contract.md](../prompts/project-report-contract.md).

## I-24: Align identity checks and approval records

Final review of the report contract and approval gate found that `_deterministic_checks` ignored the rendered header, `render_research_identity` synthesized `market-<ticker>` IDs without corpus evidence, and `check_approval.py` omitted revision chronology checks.

> When revision exists in test-approval.yaml, require revision decision APPROVED, approver leo, ISO timestamps approved_at<implementation_started_at, authorization/ADR/evidence real file paths, nonempty scope/tests.

Validating identity against the rendered report contract, citing canonical market IDs only when corpus evidence exists, and checking raw JSONL edit timestamps against revision approval enforced end-to-end provenance.

OpenCode updated `src/research_desk/eval/live.py`, `src/research_desk/report.py`, and `scripts/check_approval.py`, extended `test/offline/test_report_contract.py`, and created `test/offline/test_approval_revision.py`.

Result: [live.py](../../src/research_desk/eval/live.py), [report.py](../../src/research_desk/report.py), [check_approval.py](../../scripts/check_approval.py), [test_report_contract.py](../../test/offline/test_report_contract.py), [test_approval_revision.py](../../test/offline/test_approval_revision.py).

Source: [project-revision-runtime.full.json](../project-revision-runtime.full.json), message `msg_1c0c3ee21001awRNJ7B7bnak0k`, JSON pointer `/messages/73`. Session: `ses_e3f53febfffeJxqxKnMdRFfCgx`.

Prompt: [project-final-integration.md](../prompts/project-final-integration.md).

## I-25: Bound the complete model input

The runtime needed a pre-invocation context budget across all messages in plain, tool-bound, and structured requests, using default thresholds of 72000 trigger units and 96000 maximum units.

> Above trigger compact expendable OLD non-fact prose while preserving system/grounding constraints, latest user/task, and entire AI tool-call/ToolMessage groups. Never remove essential factual evidence merely to fit.

Estimating complete message payloads via UTF-8 byte bounds, compacting only expendable older prose above the trigger, and raising `ContextBudgetExceeded` before oversized calls protected factual evidence and tool-call pairs.

OpenCode implemented `ContextBudgetExceeded` and `estimate_input_units` in `src/research_desk/budget.py`, added budget settings in `config.py`, enforced compaction in `eval/compact_delegate.py` and `graph_adapter.py`, and added `test/offline/test_context_budget.py`.

Result: [budget.py](../../src/research_desk/budget.py), [config.py](../../src/research_desk/config.py), [compact_delegate.py](../../src/research_desk/eval/compact_delegate.py), [graph_adapter.py](../../src/research_desk/graph_adapter.py), [test_context_budget.py](../../test/offline/test_context_budget.py).

Source: [project-revision-context.full.json](../project-revision-context.full.json), message `msg_1c0b18d7c001ohLotoIhf0vhU2`, JSON pointer `/messages/0`. Session: `ses_e3f4e729affepTXL7uidfzUkEm`.

Prompt: [project-context-cap.md](../prompts/project-context-cap.md).

## I-26: Record context usage and source provenance

Per-request budget estimates were logged only to standard logging rather than the exported evidence pack, and live runs and judgments needed cryptographic source-fingerprint provenance checks.

> Integrate this actual contract into eval/live.py: save run provenance immediately BEFORE ResearchRunner runs, and save judge provenance immediately BEFORE judge invocation.

Recording `context_budget` events into `evidence_log` and verifying matching `source_fingerprint` records before and after run and judge execution prevented stale or mid-run modified code from certifying evaluation outputs.

OpenCode added the typed `budget_observer` callback in `eval/compact_delegate.py` and `graph_adapter.py`, integrated provenance checks in `eval/live.py`, cleaned the docstring in `policy.py`, and added `test/offline/test_eval_provenance.py`.

Result: [compact_delegate.py](../../src/research_desk/eval/compact_delegate.py), [live.py](../../src/research_desk/eval/live.py), [graph_adapter.py](../../src/research_desk/graph_adapter.py), [policy.py](../../src/research_desk/policy.py), [test_context_budget.py](../../test/offline/test_context_budget.py), [test_eval_provenance.py](../../test/offline/test_eval_provenance.py).

Source: [project-revision-context.full.json](../project-revision-context.full.json), message `msg_1c0bcec29001N2uJPwOI2ZhxB4`, JSON pointer `/messages/37`. Session: `ses_e3f4e729affepTXL7uidfzUkEm`.

Prompt: [project-runtime-finalize.md](../prompts/project-runtime-finalize.md), [project-budget-observations.md](../prompts/project-budget-observations.md).

## I-27: Separate quality checks and consolidate CI

The release quality module required both `.yaml` and `.yml` prompt files simultaneously, averaged support, relevance, and citation scores into a single number, and needed a consolidated six-job `ci.yml` workflow and release runner.

> Preserve declared quality retention: compare baseline/compact mean support (and mean relevance separately), each permitted drop <=.05. Cite validity has its existing .95 threshold.

Checking support and relevance drops independently prevented high citation rates from masking quality regressions, while consolidating the six required jobs into `.github/workflows/ci.yml` and adding `scripts/evaluate_release.py` standardized release validation.

OpenCode updated `src/research_desk/eval/quality.py` and `test/offline/test_release_quality.py`, consolidated the workflow into `.github/workflows/ci.yml`, updated `scripts/check_regression.py`, and implemented `scripts/evaluate_release.py`.

Result: [ci.yml](../../.github/workflows/ci.yml), [check_regression.py](../../scripts/check_regression.py), [evaluate_release.py](../../scripts/evaluate_release.py), [quality.py](../../src/research_desk/eval/quality.py), [test_release_quality.py](../../test/offline/test_release_quality.py).

Source: [project-revision-gates.full.json](../project-revision-gates.full.json), message `msg_1c0be1b5b001lpth0QH5Llk3Mj`, JSON pointer `/messages/0`. Session: `ses_e3f41e4c3ffePb0Q8P4fk877uH`.

Prompt: [project-gate-fixes.md](../prompts/project-gate-fixes.md).
