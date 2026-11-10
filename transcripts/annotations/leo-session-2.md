# Fixed-corpus research and approval semantics

The second session corrected portfolio policy and approval binding, then introduced fixed-corpus evaluation.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-02: Correct portfolio limits and evaluation inputs

The initial offline slice needed business-contract corrections for cumulative position limits, valid equity sales, full approval field binding, and a six-case fixed-evidence evaluation harness.

> The position cap is for TOTAL holdings after a purchase, including existing shares in that ticker, not each independent ticket.

Evaluating cumulative holdings at frozen evidence prices and applying compaction to per-agent message inputs prevented policy bypasses and made the six-case experiment measure real prompt compression.

OpenCode updated the policy, review, context, and graph adapter modules and added the evaluation registry, compact delegate, and frozen provider. Offline verification passed 49 tests across the updated suite.

Result: [policy.py](../../src/research_desk/policy.py), [review.py](../../src/research_desk/review.py), [case_registry.py](../../src/research_desk/eval/case_registry.py), [compact_delegate.py](../../src/research_desk/eval/compact_delegate.py), [frozen_provider.py](../../src/research_desk/eval/frozen_provider.py).

Source: [project-02.full.json](../project-02.full.json), message `msg_057cfd96f001nGEh3Hz4a0uUe0`, JSON pointer `/messages/0`. Session: `ses_fa83026e7ffe84kFIOlxvQB3aB`.

Prompt: [project-02-live.md](../prompts/project-02-live.md).
