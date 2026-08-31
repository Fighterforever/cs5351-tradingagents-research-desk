# Research Desk coding contract

Decision owner: leo. Build target: TradingAgents Research Desk, an application extension of official TradingAgents v0.4.0. Read this document first, then `Prompt.md`.

## Reading order

1. `architecture-blueprint.md` and `docs/architecture/adr/001-application-extension.md`.
2. `docs/req/prd.yaml`, `docs/req/requirements.yaml`, `docs/architecture/invariants.md`.
3. `docs/architecture/permission-model.md`, `.opencode/rules.md`, `.agent/rules.md`.
4. `docs/code-governance/verification-constraints.md`, `docs/process/test-approval.yaml`.
5. The actual declarations in the source being changed and its existing callers/tests.

## Scope and baseline

Preserve `tradingagents/`, `cli/`, `tests/`, the upstream license and public interfaces. Extend through `src/research_desk/`; application tests belong in `test/offline/` and API-dependent experiments in `test/live/`. Reuse the real TradingAgentsGraph and its selected market/news, research, trader, risk and portfolio roles. No replacement graph, fabricated market data labeled real, or broker access.

Application module ownership is defined in the blueprint. Policy constants belong to `research_desk.config`; business policy belongs to `research_desk.policy`; approval and state transitions belong to `research_desk.review`; transactions belong to `research_desk.storage`. Avoid shared vendor branches specific to Research Desk. An interface must be located before use. New interfaces require updated callers and contract tests.

## Authority and change control

Model output is advisory. It cannot approve a proposal, choose policy constants, set an evidence price, or mutate the ledger. Approval binds exact terms. Hold, REVIEW and incomplete research do not trade. Valid sells never exceed owned shares. Every execution rechecks current holdings and cash.

The plan/test decision in `docs/process/test-approval.yaml` predates this implementation and authorizes its three-feature scope. It does not authorize unrelated future changes. Changes to policy, approval, permission files or persistent contracts need an ADR and a leo decision covering the concrete change. `.opencode/rules.md`, `.agent/rules.md`, test approvals and permission decisions are owned by leo; implementation agents may propose changes but must not overwrite them.

OpenCode generates and modifies application, tests and CI. The coordinating workflow supplies prompts, runs commands and maintains evidence/report documents. Credentials are supplied only as host environment variables at runtime; never read global credential files or serialize secrets. Use the isolated project `.venv` and explicit DeepSeek model. Do not change the parent workspace's `.venv`.

## Verification and completion

Use the approved AT-01 through AT-08 specifications. At least one meaningful negative test per feature is required. Before a final change, run all `tests/` and `test/offline/` tests. Static checks and requirements schema must pass. Fixed semantic replay is part of the prompt/model change gate; live evaluations require saved actual usage and scores. Update `docs/ai-use-log.yaml` for code/prompt changes, and keep the trace matrix current.

Keep commits concise. Do not invent test outcomes, time spent, external gate deployment or people. Preserve failures and retries. Do not keep adding tests that mirror implementation after the relevant contract is already established. Stop broad cleanup when the approved result works; move to the next acceptance milestone.
