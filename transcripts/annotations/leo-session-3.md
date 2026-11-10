# Graph integration and financial contracts

Five follow-up prompts completed the live evaluation interface and corrected defects found during integration.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-03: Preserve tool calls during compaction

Review of the evaluation prototype identified dropped tool-call fields during message compaction, global LLM factory monkeypatching, fallback indicator prices, and static type errors.

> Preserve the full original message via the declared model-copy/update API, only changing content. Never deduplicate away a tool response required by an assistant tool call.

Maintaining LangChain tool-call identifiers, computing genuine CSV technical indicators, and wrapping graph models through a local delegate ensured valid multi-step agent execution and type-safe live CLI entry points.

OpenCode repaired message reconstruction, indicator calculations, budget stop reasons, and static types, while adding the `evaluate-case`, `judge-case`, and `aggregate` CLI commands. Verification passed 59 offline tests and passing mypy checks across 18 source files.

Result: [compact_delegate.py](../../src/research_desk/eval/compact_delegate.py), [frozen_provider.py](../../src/research_desk/eval/frozen_provider.py), [live.py](../../src/research_desk/eval/live.py), [graph_adapter.py](../../src/research_desk/graph_adapter.py), [test_live_fixes.py](../../test/offline/test_live_fixes.py).

Source: [project-04.full.json](../project-04.full.json), message `msg_057da1942001Tp47keCSN4ERtu`, JSON pointer `/messages/0`. Session: `ses_fa825e6e8fferDOiutg4e8ECO8`.

Prompt: [project-04-ready-live.md](../prompts/project-04-ready-live.md).

## I-04: Supply the complete graph configuration

The first live AAPL baseline launch failed before issuing any API request because `TradingAgentsGraph` required `data_cache_dir` in a complete configuration dictionary.

> Fix this actual root cause: construct the evaluation config from a deep copy of the actual DEFAULT_CONFIG, then override the explicit model/settings.

Building evaluation configurations from `DEFAULT_CONFIG` and routing cache, results, and memory paths into each arm's isolated directory satisfied upstream initialization contracts without modifying vendor code.

OpenCode updated `_graph_config` in `src/research_desk/eval/live.py` and added a real graph construction regression test in `test/offline/test_live_fixes.py`. Offline verification recorded 60 passing tests and a passing 18-file mypy check.

Result: [live.py](../../src/research_desk/eval/live.py), [test_live_fixes.py](../../test/offline/test_live_fixes.py).

Source: [project-04.full.json](../project-04.full.json), message `msg_057e18ca30013lkvYNje6DardE`, JSON pointer `/messages/82`. Session: `ses_fa825e6e8fferDOiutg4e8ECO8`.

Prompt: [project-05-config-fix.md](../prompts/project-05-config-fix.md).

## I-05: Give the judge complete evidence

Frozen evaluation runs still permitted online instrument identity fallbacks and omitted uncalled market history and raw structured tool outputs from the judge package.

> Give FrozenMarketProvider an explicit identity contract and pass it to the subclass so frozen runs have no hidden identity request.

Recording the complete frozen corpus separately from observed tool calls and persisting raw structured judge responses allowed deterministic price derivation and verifiable citation-rate calculations.

OpenCode bound frozen company identities in `src/research_desk/graph_adapter.py`, added `available_sources` to `InputSnapshot`, and expanded judge prompt evidence and raw message persistence in `src/research_desk/eval/live.py`. The offline suite passed 65 tests with zero mypy issues.

Result: [live.py](../../src/research_desk/eval/live.py), [graph_adapter.py](../../src/research_desk/graph_adapter.py), [models.py](../../src/research_desk/models.py), [test_live_fixes.py](../../test/offline/test_live_fixes.py).

Source: [project-04.full.json](../project-04.full.json), message `msg_057e4aa250013uEwf2a20yn6lX`, JSON pointer `/messages/109`. Session: `ses_fa825e6e8fferDOiutg4e8ECO8`.

Prompt: [project-06-evidence-judge.md](../prompts/project-06-evidence-judge.md).

## I-06: Allow sales that reduce exposure

The sell policy check enforced the 10% concentration limit on remaining holdings after a sale, blocking legitimate risk-reducing sales when price appreciation pushed an existing position above the cap.

> The10% concentration check applies after a BUY. A valid SELL that reduces an owned position must be permitted even if price appreciation means the remaining holding is still above10%.

Restricting the concentration cap to purchases while retaining positive integer quantity and no-shorting rules on sales aligned `evaluate_sell` with the financial invariant in ADR-002.

OpenCode removed the remaining-position cap check from `evaluate_sell` in `src/research_desk/policy.py` and added a boundary regression in `test/offline/test_at04_reject_boundaries.py`. Verification passed all 66 offline tests and mypy checks.

Result: [policy.py](../../src/research_desk/policy.py), [test_at04_reject_boundaries.py](../../test/offline/test_at04_reject_boundaries.py).

Source: [project-04.full.json](../project-04.full.json), message `msg_057e988f3001a8BWcP7RGaTYte`, JSON pointer `/messages/150`. Session: `ses_fa825e6e8fferDOiutg4e8ECO8`.

Prompt: [project-07-sell-fix.md](../prompts/project-07-sell-fix.md).

## I-07: Archive prompts and add the live entry point

With the application source frozen for evaluation runs, the repository needed an isolated opt-in live test entry point and a versioned YAML archive of the runtime prompt configuration.

> Archive actual current runtime prompt text/settings under prompts/ with a version mapping derived from the existing ResearchDeskSettings.prompt_version.

Isolating the live test behind environment flags and archiving the exact prompt settings from Python source documented the active experimental configuration without altering running graph behavior.

OpenCode added `test/live/test_live_evaluation.py`, `test/live/README.md`, and `prompts/runtime-prompts-v0.1.0.yaml` without touching `src/` or offline tests.

Result: [runtime-prompts-v0.1.0.yaml](../../prompts/runtime-prompts-v0.1.0.yaml), [README.md](../../test/live/README.md), [test_live_evaluation.py](../../test/live/test_live_evaluation.py).

Source: [project-04.full.json](../project-04.full.json), message `msg_057ebf53500134R3qYEe0C5Lyo`, JSON pointer `/messages/164`. Session: `ses_fa825e6e8fferDOiutg4e8ECO8`.

Prompt: [project-08-live-test.md](../prompts/project-08-live-test.md).
