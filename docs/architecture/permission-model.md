# Permission model

[opencode.json](../../opencode.json) defines the installed coding roles. Its file and tool rules match the [permission manifest](../../.opencode/permissions.jsonc). Each role inherits the explicit read allowlist. The default read and edit rules deny access.

| Role | Files it can edit | Commands it can run |
|---|---|---|
| Plan | `proposals/**` | No shell commands |
| Build | `src/research_desk/**`, `test/**`, `scripts/**`, `pyproject.toml` and `.github/workflows/**`, subject to the protected files below | The exact read-only Git and directory commands in the manifest |
| Verify | `verification/**` | The listed project-local test and gate commands and a limited set of read-only inspection commands |

Build cannot edit the policy, review, storage, configuration or model-contract modules. The upstream engine and its tests are frozen. Rules and approval records are protected for all three roles. A change to a safety boundary requires a scoped decision and an accepted ADR. During the release revision a temporary role covered the paths approved in [ADR-004](adr/004-release-quality-and-context-budget.md). That role was removed after implementation.

The release operator handles provider credentials, repository publication and GitHub checks outside the coding-agent roles. The running research graph receives market and news tools. Only the operator CLI can approve exact terms and invoke the deterministic execution policy.
