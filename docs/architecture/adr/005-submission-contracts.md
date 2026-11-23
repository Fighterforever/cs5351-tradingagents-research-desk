# ADR-005: Preserve ledger authority and validate the complete release

Status: Accepted within the repair scope delegated by Liyu MA. The student's direction is U-08. The coordinating workflow reviewed the OpenCode plan and selected the detailed acceptance cases before implementation. U-09 separately confirms Liyu MA's identity.
Approval record ID: `leo`.

## Decision and scope

The research package identifies the evidence for a proposed trade. The ledger owns registration, approval and execution state. Re-registering a package must preserve prior operator decisions and completed transactions. Derive a stable identity from the material research inputs, including on the supported import path for older packages. Leave archived research files intact. The replay command must report successful reconstruction only after its output files exist. Enforce the documented judge call budget across both arms and propagate failure to the CLI.

For each code change, check the scope and timing of the corresponding approval and test evidence. Check public interfaces on safety-related changes. Match changed code or prompt paths to entries actually amended in the current AI-use log. Validate each of six pairs before aggregating the release results. Bind results to the research graph, role code and inputs actually used. Continue to apply the existing quality thresholds. Publish fresh research results when the source changes.

Affected owners are `src/research_desk/graph_adapter.py`, `src/research_desk/evidence.py`, `src/research_desk/review.py`, `src/research_desk/models.py`, `src/research_desk/storage.py`, `src/research_desk/replay.py`, `src/research_desk/cli.py`, `src/research_desk/eval/live.py` and `src/research_desk/eval/quality.py`. Governance rule synchronization covers `.agent/rules.md` and `.opencode/rules.md`. Verification owners are the gate scripts and `.github/workflows/ci.yml`. The working copies used by OpenCode can edit only the files listed for their assigned task. The published role permissions continue to apply to the repository.

## Acceptance

- In the real graph-to-registration flow, material evidence has a stable identity and a change to that evidence requires review. A repeat registration preserves the ledger's existing terminal state and original transaction. A register call cannot import approval authority. Cover both current and previously stored evidence.
- A successful replay lists each output once. An ordinary filesystem write error produces a readable diagnostic and a failing exit. With a limited judge call budget, both arms together cannot exceed the limit. A failed judge result reaches the command's exit status.
- Validate the shape and presence of every case, arm and corresponding judgment; require six complete pairs before publishing aggregate metrics. Changes in the upstream graph or role prompts invalidate the prior source binding.
- Check a code-only change against the applicable approval, the relevant tests and their temporal order. Check affected public API compatibility, and match the current diff to the current log and actual evidence. Include normal covered changes and negative cases as unit tests. Use the protected main merge base for new-branch comparisons.
- Compare the Git release branch and the generated ZIP by path and contents. Keep the existing public record and document any pending independent review.

The student requested repair of the reported contracts and publication, and delegated implementation decisions. The historic releases and genuine tool-use records remain the source for what happened in earlier runs. A separate student's confirmation is required before attributing an unverified contribution or reflection to that student. Reopen if the approval or evidence schema has to change incompatibly, or the six-case corpus or source boundaries change.

During unit review, the existing CLI case for an incomplete package was identified as checking the internal exception type as well as the failed command. Its approved CLI-level expectation is a nonzero exit with the missing-file diagnostic. The lower-level tests retain the evidence-reader exception contract.

The submission review also found that the launch prompt reused an earlier approval. For D9, the next launch must stop after presenting its plan and again at the build and verification boundaries for the human decision on that stage. Review the edited prompt against the project sheet before release. Existing decisions retain their original scope.
