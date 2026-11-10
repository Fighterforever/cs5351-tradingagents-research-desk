# Provider settings and request serialization

Three prompts corrected the observed provider parameter mismatch and verified the direct and structured request payloads.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-28: Apply the provider’s effective thinking setting

Live diagnosis recorded in `evaluation/revision-initial/provider-parameter-diagnosis.json` showed that the AioHub `deepseek-flash` endpoint ignored `thinking: {"type": "disabled"}` alone and exhausted the 1800-token output cap on reasoning tokens.

> In src/research_desk/eval/live.py, add reasoning_effort:"none" to THINKING_DISABLED_EXTRA_BODY so both graph models and judge get the same effective nonthinking setting via extra_body (upstream factory filters top-level reasoning_effort for DeepSeek, so keep it inside extra_body).

Passing `reasoning_effort: "none"` inside `extra_body` disabled reasoning token generation across both experimental arms and the structured judge so responses returned complete content within the 1800-token cap.

OpenCode updated `THINKING_DISABLED_EXTRA_BODY` in `src/research_desk/eval/live.py` and added a request-payload serialization unit test in `test/offline/test_revision_contracts.py`.

Result: [live.py](../../src/research_desk/eval/live.py), [test_revision_contracts.py](../../test/offline/test_revision_contracts.py).

Source: [project-revision-transport.full.json](../project-revision-transport.full.json), message `msg_1c0d70681001leG7JpaXM81KJR`, JSON pointer `/messages/0`. Session: `ses_e3f28f99fffeB3EaSGurvf2t3E`.

Prompt: [project-provider-transport.md](../prompts/project-provider-transport.md).

## I-29: Inspect the actual structured request binding

The new transport unit test failed to locate the underlying `DeepSeekChatOpenAI` model because `with_structured_output` wraps the bound client inside `RunnableParallel.steps__['raw']`.

> Use bound = structured.steps[0].steps__['raw'].bound, assert isinstance(bound, DeepSeekChatOpenAI), and inspect bound._get_request_payload(..., **structured.steps[0].steps__['raw'].kwargs) so the tool schema binding is exercised too.

Inspecting `structured.steps[0].steps__['raw']` directly tested the actual installed LangChain Runnable structure and verified that `extra_body` survived structured tool-schema binding.

OpenCode removed the generic `_first_chat_model` helper in `test/offline/test_revision_contracts.py` and asserted the payload directly on the bound `DeepSeekChatOpenAI` instance and its structured kwargs.

Result: [test_revision_contracts.py](../../test/offline/test_revision_contracts.py).

Source: [project-revision-transport.full.json](../project-revision-transport.full.json), message `msg_1c0d94a08001bGuarwpCGgKFxo`, JSON pointer `/messages/19`. Session: `ses_e3f28f99fffeB3EaSGurvf2t3E`.

Prompt: [project-provider-unit-fix.md](../prompts/project-provider-unit-fix.md).

## I-30: Check the serialized request fields

Calling `json.dumps` on the raw `_get_request_payload` dictionary in the transport test failed because LangChain retains an internal Pydantic schema class reference until the HTTP client serializes the request.

> Edit ONLY test/offline/test_revision_contracts.py: remove its local import json and the two redundant json.dumps substring assertions. Retain both real request-payload assertions of extra_body.reasoning_effort and thinking.type, including the structured binding kwargs.

The generated payload dictionaries expose both provider settings directly. Checking these fields exercises the request contract at the correct serialization boundary.

OpenCode updated `test/offline/test_revision_contracts.py` to assert both settings on direct and structured request payloads. Subsequent validation passed 790 unit tests with 71 subtests. The 12 release runs passed 60/60 mandatory checks, and all six cloud CI gates passed.

Result: [test_revision_contracts.py](../../test/offline/test_revision_contracts.py), [summary.json](../../evaluation/ci-release/summary.json), [release-gate.json](../../evaluation/release/aggregate/release-gate.json), [revision-cloud-run.json](../../evaluation/github/revision-cloud-run.json).

Source: [project-revision-transport.full.json](../project-revision-transport.full.json), message `msg_1c0debec7001cbJyBg2cqQP53A`, JSON pointer `/messages/22`. Session: `ses_e3f28f99fffeB3EaSGurvf2t3E`.

Prompt: [project-provider-unit-serialization.md](../prompts/project-provider-unit-serialization.md).
