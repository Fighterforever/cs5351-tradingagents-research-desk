# Per-request evidence grounding

Two prompts corrected the citation failure in development runs and removed unsupported examples from shared grounding instructions.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-15: Deliver evidence instructions to every role

Initial development runs on AAPL and MSFT achieved roughly 36% token savings in compact mode but produced zero inline source citations because grounding headers were placed only in `past_context` and baseline models were unwrapped.

> Every actual LLM request in BOTH baseline and compact must receive the same common grounding layer after any compaction. It must require factual claims to cite the proper source ID inline.

Wrapping both baseline and compact clients with a plain `RunnableLambda` delegate ensured that every plain, tool-bound, and structured LLM request received identical source registries and citation rules without dynamic class mutation.

OpenCode updated `context.py`, `compact_delegate.py`, `graph_adapter.py`, `frozen_provider.py`, and `config.py`, and added `test/offline/test_common_grounding_delegate.py`. All 72 offline tests passed.

Result: [context.py](../../src/research_desk/context.py), [compact_delegate.py](../../src/research_desk/eval/compact_delegate.py), [graph_adapter.py](../../src/research_desk/graph_adapter.py), [frozen_provider.py](../../src/research_desk/eval/frozen_provider.py), [config.py](../../src/research_desk/config.py), [test_common_grounding_delegate.py](../../test/offline/test_common_grounding_delegate.py).

Source: [project-09.full.json.gz](../project-09.full.json.gz), message `msg_057f1a19e001W5VzxxxKnN4lj8`, JSON pointer `/messages/0`. Session: `ses_fa80e5e8bffei1CBiJ8vadPRtm`.

Prompt: [project-09-grounding.md](../prompts/project-09-grounding.md).

## I-16: Remove unsupported grounding examples

Code review of `build_common_grounding` found illustrative MSFT revenue numbers in the shared instruction text and fabricated source registries when `available_sources` was empty.

> Remove ALL numeric/company-specific examples from instruction prose. Give only a format such as "<supported claim> [<actual source ID>]"; arithmetic instruction can simply require actual operands and their citations without example values.

Eliminating foreign ticker numbers and registering only sources actually present in the run prevented cross-company contamination and required final rationales to report the active case's frozen close, date, and ticker.

OpenCode refined `src/research_desk/context.py`, updated `prompts/runtime-prompts-v0.1.1.yaml`, and expanded `test/offline/test_common_grounding_delegate.py`. Verification passed all 5 focused grounding tests and a passing 18-file mypy check.

Result: [context.py](../../src/research_desk/context.py), [runtime-prompts-v0.1.1.yaml](../../prompts/runtime-prompts-v0.1.1.yaml), [test_common_grounding_delegate.py](../../test/offline/test_common_grounding_delegate.py).

Source: [project-09.full.json.gz](../project-09.full.json.gz), message `msg_057f71ae5001McaBa8PQGkTYCe`, JSON pointer `/messages/43`. Session: `ses_fa80e5e8bffei1CBiJ8vadPRtm`.

Prompt: [project-10-grounding-precision.md](../prompts/project-10-grounding-precision.md).
