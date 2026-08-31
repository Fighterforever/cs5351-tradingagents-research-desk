# Structural constraints

ADR-001 assigns one owner to each architectural element. New code extends the real v0.4.0 baseline under src/research_desk. Shared vendor routes must not branch on this application's identity. A subclass or composition seam may capture an existing external read where callbacks cannot observe it.

Module docstrings identify applicable ADRs and invariants; trace-matrix.md is the authoritative mapping for individual behavior. Pure business functions accept established records. Validate external package files, CLI input and provider output at their boundaries. Do not duplicate validation throughout trusted internal paths.

review and policy cannot call an LLM. The graph cannot import a function that grants approval or mutates the ledger. Storage applies approved deterministic decisions and records the resulting transaction. Context transformations preserve critical identity, date, price and task information. Unknown frozen data remains unknown.

A change to the persistence contract requires models, IO, callers and tests together. Existing upstream directories and license remain. The extension is packaged through pyproject.toml rather than copied into a different toy project. Extra dependencies need a concrete purpose and go only into the project environment.
