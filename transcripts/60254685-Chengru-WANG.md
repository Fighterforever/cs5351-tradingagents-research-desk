# Annotated development record: Chengru WANG

Student number: 60254685. Working name: Delta. GitHub account: [wangsaorui](https://github.com/wangsaorui).

This record documents one supervised agentic software-engineering session in which the human owner (Delta) directed an AI coding agent to restore cross-Python-version regression coverage in the project CI, closing review finding **F1** that Delta had raised while independently reviewing PR #1 (see [review memo](../docs/review-memo.md), "Independent code-owner review of PR #1"). Each annotation records the observed situation, the human instruction or decision, the rationale, and the resulting change.

## Session and evidence provenance (stated honestly)

- **Tooling deviation.** The project `AGENTS.md` anticipates OpenCode CLI for code generation. This supervised session was conducted with an IDE-integrated coding agent (Qoder) rather than the OpenCode CLI. No OpenCode `session`/`message` identifiers are claimed for these directives, because none were produced.
- **Auditable artifacts.** The verifiable record of this session is the git commit history on the branch `d5-ci-cross-version` and the resulting pull request, together with the files changed below. The raw conversation is retained in the client session log; it is deliberately not rewritten into the OpenCode `.jsonl` format to avoid presenting fabricated evidence.
- **Governance followed.** Per `Prompt.md`, the agent produced a concrete execution plan and **stopped for a human decision before writing any code**. The plan approval and the advisory-versus-blocking choice are genuine human decisions, not agent-authored approvals.

## Reading guide

| Record | Focus |
|---|---|
| [CI workflow](../.github/workflows/ci.yml) | Added the advisory `cross-version-regression` job (Python 3.10–3.13). |
| [CI gate documentation](../docs/ci-gates.md) | Recorded the advisory job and its promotion-to-blocking condition. |
| [AI-use log](../docs/ai-use-log.yaml) | Logged this change as a coordinator entry with the real local-verification outcome. |
| [Review memo](../docs/review-memo.md) | Source of finding F1 that this session resolves. |

## Interventions

### D5-01 — Select a deliverable that requires real supervision
- **Situation:** The only per-student deliverable still missing was Delta's annotated transcript (D5). A shortcut would have been to compose a transcript describing supervision that never happened.
- **Human instruction:** Do not write a transcript without an underlying session; instead run a real supervised task on the project and record it.
- **Rationale:** D5 is evidence of auditable human supervision and must reconcile with repo artifacts. Fabricated interventions would be detectable against the git history and would constitute academic misconduct.

### D5-02 — Approve the execution plan before code (plan-first gate)
- **Situation:** The agent proposed a scoped change and paused for approval, as `Prompt.md` requires for a new slice.
- **Human decision:** Approved **Task A**: restore the cross-version matrix by adding an advisory CI job that runs the existing Gate 5 regression program across Python 3.10–3.13, limited to pull-request events, touching only `ci.yml`, `docs/ci-gates.md` and the AI-use log.
- **Rationale:** The change stays within Delta's CI ownership, does not modify safety-critical policy or leo-owned frozen files, and directly closes the reviewer's own F1 finding. Running only on `pull_request` bounds CI minutes.

### D5-03 — Keep the new job advisory, not blocking
- **Human decision:** Mark the job `continue-on-error: true` and out of the required-check set until a full-version run is observed green.
- **Rationale:** A blocking gate that has not been demonstrated green on every version could silently break merge for the whole team. Promotion to blocking is reserved as a deliberate human release decision.

### D5-04 — Accept the honest local-verification result
- **Situation:** Running `python scripts/check_regression.py` locally failed: `tests` produced 44 collection errors from missing upstream dependencies, and `test/offline` failed with `ModuleNotFoundError: No module named 'research_desk'` because the project virtual environment was not installed in the global interpreter.
- **Human decision:** Record the failure as-is, do not fabricate a passing count, and treat CI as the authoritative cross-version executor. The local run therefore verifies only that the workflow file and gate scripts are wired correctly, not that every Python version passes.
- **Rationale:** `AGENTS.md` forbids inventing test outcomes. The advisory job's purpose is precisely to obtain that evidence in CI, where dependencies are installed from `requirements-lock.txt`.

## Coverage across the supervised pipeline

| Stage | This session's evidence |
|---|---|
| Requirements / review finding | F1 recorded in [review memo](../docs/review-memo.md); scope confirmed in [team responsibilities](../docs/process/team.md). |
| Architecture / governance | Change confined to CI and documentation; no safety-path or frozen-file edit, consistent with `AGENTS.md`. |
| Implementation | `cross-version-regression` job in [.github/workflows/ci.yml](../.github/workflows/ci.yml); YAML validated (7 jobs present). |
| Verification | Local `check_regression.py` attempted and its real failure documented; authoritative matrix deferred to the CI job. |
| Delivery controls | Change set prepared on branch `d5-ci-cross-version` for an independent-reviewed pull request; AI-use log updated. |

## Result

An advisory, non-blocking CI job now exercises the Gate 5 regression suite on Python 3.10, 3.11, 3.12 and 3.13 for every pull request. Finding F1 is addressed with real, non-fabricated evidence, and the promotion of the job to a required check remains an explicit human decision.
