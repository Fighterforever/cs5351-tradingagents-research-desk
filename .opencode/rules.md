# Always-on project rules

Owner: leo. Implementation agents may read this file and propose changes; only leo's decision workflow installs changes.

Follow AGENTS.md, the approved plan and architecture. Preserve TradingAgents v0.4.0 as the research engine. Never read global credential configuration, persist API keys, call a broker or publish outside the authorized private repository. Use project-local data homes and the project .venv.

Model output remains advisory. Exact approval, deterministic current-ledger checks and idempotent recording are mandatory. Do not weaken a requirement to make a test pass. Raw transcripts and experiment outcomes are immutable evidence. Mark incomplete work plainly.

A changed safety requirement needs an ADR and concrete approval before implementation. Existing approval is scoped and timestamped. Update requirements, tests and traceability together. Check actual declarations before using an interface. Keep changes small and purposeful.
