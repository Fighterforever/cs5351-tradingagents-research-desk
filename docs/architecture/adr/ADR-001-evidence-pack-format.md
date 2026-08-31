# ADR-001 Appendix: Evidence pack format and offline replay

Status: accepted appendix to `001-application-extension.md` (2026-08-31, decided by leo). Context: F1. The application-extension ADR remains the authoritative architectural decision; this appendix specifies its package representation.

## Decision

An evidence pack is a self-contained directory (or a ZIP of one) with a fixed
set of JSON/JSONL files: `manifest.json`, `input.json`, `events.jsonl`,
`final_state.json`, `usage.json`, `calls.json`, optional `proposal.json`, and
`meta.json`. `complete` is only set when every required file is present and
parses. Import validates required files and fails loudly on a missing record.

Replay rebuilds the report tree from `final_state`, derives the signal with the
same deterministic heuristic the graph uses (`SignalProcessor`), and reports
the deterministic policy bounds for the proposal against a ledger. Replay never
constructs an LLM client.

## Why

- The final graph state plus the captured tool data are the *material* needed
  to rebuild reports and policy outputs with zero external calls; LLM re-output
  is not needed and would violate "no network on replay".
- Complete/incomplete is a structural property (required files) so a partial
  pack cannot silently replay a wrong decision.
- JSONL events keep the log append-friendly and streamable.

## Consequences

- Evidence packs can be large (they keep full prompts/responses for provenance).
- Replay is deterministic for the signal and policy; the *report timestamps*
  are display metadata and intentionally differ from the original run.
