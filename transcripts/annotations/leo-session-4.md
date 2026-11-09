# CI gates and negative cases

Six prompts developed the blocking CI gates and their expected-rejection examples.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-08: Define the six CI gates

The repository needed six automated offline CI gates and a corrected JSON schema to validate test approval chronology, static typing, requirement traceability, deterministic replay, full test suites, and AI-use logging.

> Validate the real YAML registry against the corrected JSON schema; reject missing or duplicate IDs, unmeasurable fit criteria, and broken component/test/trace links.

Defining strict write ownership and six offline verification gates established enforceable repository checks while parallel application edits were underway.

In this initial turn, OpenCode inspected the repository interfaces, requirement registry, and 49 passing offline tests to prepare the gate implementation completed in the following turn.

Result: [req-schema.json](../../docs/req/req-schema.json).

Source: [project-ci.full.json](../project-ci.full.json), message `msg_057d35063001V7BNOJy9zL3Iud`, JSON pointer `/messages/0`. Session: `ses_fa82cafc9ffeeAkOozPwPQ41De`.

Prompt: [project-ci.md](../prompts/project-ci.md).

## I-09: Move from inspection to implementation

During the initial CI turn, the agent continued running baseline checks after inspecting the required interfaces instead of writing the gate scripts and workflow.

> Continue the already inspected CI task now. The coordinator stopped your first turn because you repeated baseline checks after enough interfaces were known.

Redirecting the session from repeated exploration to immediate file creation produced the concrete GitHub workflow, requirement schema, and six gate scripts without redundant test loops.

OpenCode created `.github/workflows/research-desk.yml`, replaced `docs/req/req-schema.json`, and implemented `scripts/_gate_lib.py` along with all six `scripts/check_*.py` validators.

Result: [req-schema.json](../../docs/req/req-schema.json), [_gate_lib.py](../../scripts/_gate_lib.py), [check_approval.py](../../scripts/check_approval.py), [check_static.py](../../scripts/check_static.py), [check_requirements.py](../../scripts/check_requirements.py), [check_semantic.py](../../scripts/check_semantic.py), [check_regression.py](../../scripts/check_regression.py), [check_ai_use_log.py](../../scripts/check_ai_use_log.py).

Source: [project-ci.full.json](../project-ci.full.json), message `msg_057d7a4b2001oLlP2CtoQc6Xle`, JSON pointer `/messages/38`. Session: `ses_fa82cafc9ffeeAkOozPwPQ41De`.

Prompt: [project-ci-focus.md](../prompts/project-ci-focus.md).

## I-10: Connect gates to real changes and interfaces

Review of the initial CI scripts found that git failures returned empty change sets, legacy approvals passed modified tests, and the semantic gate referenced a placeholder evaluation function.

> `_gate_lib.changed_files` must fail the gate on git failure; returning an empty list currently makes an invalid diff pass.

Raising errors on failed git diffs, requiring same-diff ADR and approval updates for safety paths, and calling `case_registry.all_cases` and `compact_transform` ensured that the gates enforced real repository invariants.

OpenCode updated `.github/workflows/research-desk.yml`, `scripts/_gate_lib.py`, and all six gate scripts to enforce strict diff resolution, per-row matrix traceability, socket-blocked pack replay, and six-case prompt compaction checks.

Result: [_gate_lib.py](../../scripts/_gate_lib.py), [check_approval.py](../../scripts/check_approval.py), [check_static.py](../../scripts/check_static.py), [check_requirements.py](../../scripts/check_requirements.py), [check_semantic.py](../../scripts/check_semantic.py), [check_regression.py](../../scripts/check_regression.py), [check_ai_use_log.py](../../scripts/check_ai_use_log.py).

Source: [project-ci.full.json](../project-ci.full.json), message `msg_057dc326f001NRTNntwda9nw33`, JSON pointer `/messages/52`. Session: `ses_fa82cafc9ffeeAkOozPwPQ41De`.

Prompt: [project-ci-corrections.md](../prompts/project-ci-corrections.md).

## I-11: Repair workflow outputs and ADR matching

The GitHub workflow wrote resolved base SHAs only to standard output rather than `$GITHUB_OUTPUT`, and Gate 2 matched module names anywhere in ADR prose instead of parsing declared path lists.

> Write the resolved value to `$GITHUB_OUTPUT` so the next step receives it. Preserve PR base/head SHA, ordinary push before/head, and fetch-depth 0.

Writing base refs to `$GITHUB_OUTPUT` against the `v0.4.0` baseline tag and requiring `docs/ai-use-log.yaml` and explicit ADR path matches in the active diff closed remaining bypasses before local gate execution.

OpenCode updated `.github/workflows/research-desk.yml`, `scripts/check_ai_use_log.py`, `scripts/check_approval.py`, `scripts/check_semantic.py`, and `scripts/check_static.py` to finalize the six validators.

Result: [check_ai_use_log.py](../../scripts/check_ai_use_log.py), [check_approval.py](../../scripts/check_approval.py), [check_semantic.py](../../scripts/check_semantic.py), [check_static.py](../../scripts/check_static.py).

Source: [project-ci.full.json](../project-ci.full.json), message `msg_057e05d13001kspLz9g5VTC61T`, JSON pointer `/messages/77`. Session: `ses_fa82cafc9ffeeAkOozPwPQ41De`.

Prompt: [project-ci-finalize.md](../prompts/project-ci-finalize.md).

## I-12: Demonstrate each gate’s rejection behavior

Acceptance test AT-08 required a reproducible negative demonstration proving that each of the six CI gates fails for its intended violation without mutating tracked repository files.

> The script should create temporary isolated roots as needed and execute a single deliberately violating example for each gate. Record the actual command, nonzero exit code and relevant failure message.

Running deliberate violations inside auto-cleaned temporary directories verified that each validator actively rejected malformed approvals, unapproved safety edits, broken schemas, missing fixture packs, failing tests, and unlogged code changes.

OpenCode created `scripts/check_gate_examples.py` and expanded `scripts/check_ai_use_log.py` to treat workflow and behavior-configuration edits as code changes requiring AI-use log updates.

Result: [check_gate_examples.py](../../scripts/check_gate_examples.py), [check_ai_use_log.py](../../scripts/check_ai_use_log.py).

Source: [project-ci.full.json](../project-ci.full.json), message `msg_057e2f9fc001782x6W2yD7S3Qm`, JSON pointer `/messages/107`. Session: `ses_fa82cafc9ffeeAkOozPwPQ41De`.

Prompt: [project-ci-negative-examples.md](../prompts/project-ci-negative-examples.md).

## I-13: Capture reproducible gate failure evidence

The negative gate demonstration needed explicit changed-file arguments for temporary roots without `.git` directories, direct resolution of the project Python interpreter, and captured subprocess output in the JSON report.

> In each JSON result save the actual proc.args, stdout and stderr as evidence alongside exit/matched, so a reviewer can see the real rejection.

Passing explicit changed files in temporary roots, deriving the late approval timestamp dynamically, and saving command arguments and streams made every expected gate rejection self-contained and auditable.

OpenCode updated `scripts/check_gate_examples.py` to pass `--changed-files docs/ci-gates.md` for Gate 4, use the real environment interpreter for Gate 5, compute `approved_at` from `implementation_started_at`, and persist `args`, `stdout`, and `stderr`.

Result: [check_gate_examples.py](../../scripts/check_gate_examples.py).

Source: [project-ci.full.json](../project-ci.full.json), message `msg_057e5ae86001yVs7qc6kgdcw4D`, JSON pointer `/messages/114`. Session: `ses_fa82cafc9ffeeAkOozPwPQ41De`.
