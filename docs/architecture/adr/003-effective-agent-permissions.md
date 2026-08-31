# ADR-003: Install effective role permissions

Status: accepted by leo, 2026-08-31. Requirements: GOV-001 through GOV-004; source: docs/architecture/permission-model.md.

The required .opencode/permissions.jsonc is a machine-readable permission manifest. OpenCode does not automatically enforce that filename. The real project opencode.json must load .opencode/rules.md through its documented instructions field and configure supported role permissions. The CI check verifies consistency between the documented manifest and effective configuration.

The approved plan/build/verify roles have explicit read/write scope. The implementation role cannot edit rules, approvals or permission decisions. Safety source changes are limited to the existing approved feature/test scope and ADR-002 corrections. Credentials remain outside agent-readable paths. Arbitrary shell execution must not provide an alternative route around frozen-file restrictions; verification commands are separately scoped.

This installation is authorized now, but activation waits until the current implementation session ends so it does not unexpectedly revoke an in-progress approved operation. The actual installed configuration and activation evidence are recorded at release. No document claims enforcement before configuration exists.

## Affected paths

This decision covers `opencode.json`, `.opencode/permissions.jsonc`, `.opencode/rules.md`, `.agent/rules.md` and the permission-consistency checks in `scripts/`. The two rules files and approval records remain owned by leo. This explicit path list documents the same accepted installation scope and does not alter the decision date.

The pinned public `.opencode/config-schema.json` accompanies the effective configuration so CI validates the same official schema without depending on an orchestration directory outside the repository.
