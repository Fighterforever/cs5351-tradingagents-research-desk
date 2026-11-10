# Reviewer onboarding

Designated GitHub reviewer: [wangsaorui](https://github.com/wangsaorui). The repository owner is Fighterforever. The collaborator invitation has been accepted, and GitHub confirms write permission.

## Prepared configuration

The `add-code-owner` branch starts from `main` and adds `@wangsaorui` alongside `@Fighterforever` in `.github/CODEOWNERS`. It also reuses the existing six-gate workflow from `improve-delivery`, consolidating the duplicate workflows. The same owner entry is present in `improve-delivery`.

GitHub evaluates code ownership using the pull request's base branch. The current `main` branch names only Fighterforever, who authored PR #1. Activate the additional owner through the following sequence.

## Activation sequence

1. **Completed:** wangsaorui accepted the [repository invitation](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/invitations).
2. **wangsaorui**, signed in with that account, opens the [prepared configuration pull request](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/compare/main...add-code-owner?expand=1). Use the title `Add code owner`. The changes add the designated reviewer and reuse the project's established CI workflow.
3. **Fighterforever** reviews the configuration PR. After the six required checks pass and the owner approves it, merge it into `main`.
4. Update `improve-delivery` with `main` and preserve both branches' AI-use log entries. After its required checks pass, **wangsaorui** independently reviews [PR #1](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/1) and submits the review decision.
5. Merge PR #1 through the protected branch after approval.

Branch protection keeps its six required checks and code-owner review requirement throughout this sequence. The supplied GitHub account has not yet been mapped to a formal student identity or a working team alias.

Reference: [GitHub code-owner rules](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
