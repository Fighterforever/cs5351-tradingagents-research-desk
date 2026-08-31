# Memory and state design

Research memory and paper execution state have different owners. Upstream memory retains structured research decisions for reflection; the application captures exactly the memory used by a run. The paper ledger records approved transactions. A model-generated reflection cannot write the paper ledger.

The application home, selected by RESEARCH_DESK_HOME, contains the SQLite database and run directories. Every demonstration and evaluation uses a separate project-local home. SQLite stores proposals, cash, positions and transactions. Evidence files store manifest, material input, events, calls, provider usage and terminal state. A package can be transferred independently of the database for replay. Proposal approval refers to exact evidence and trade terms.

A completed run survives process exit through its evidence package. Interrupted or budget-stopped runs retain the terminal reason and collected calls. Replay reconstructs saved state. A controlled rerun creates a new run and refers to its source evidence. The evaluation command replaces the selected arm output directory, so the host runner archives earlier attempts and resumes completed cases. A reviewer must use a new output root when repeating the submitted experiment.

Memory retrieval applies the analysis cutoff to resolution/availability dates. Retrieval date is recorded separately because downloading a July release in August does not make its content available before July. Future-resolved lessons are excluded. Unknown availability is visible and unsuitable for strict historical claims. This rule concerns input provenance and does not certify investment validity.

The package schema starts at version1. Release names follow ordinary semantic versioning. Content fingerprints serve integrity and exact approval binding only. Changes to persisted contracts need an explicit migration or documented import path before claiming compatibility. No unsupported cross-version restoration is promised.

Retention: keep source fixtures, experiment evidence, decisions and full credential-scanned sessions through assessment; retain ledger demonstrations as reproducible fixtures. Credentials are never durable state. User-specific caches, environment files and Yahoo cookies are excluded from the submission and repository. Deleting a project home resets local paper state and must not delete the immutable submitted experiment evidence.

The teaching valuation convention re-marks the ticker under review at its captured evidence price. Other holdings use their stored average price, which is visible in ledger records. This is a declared local paper-account convention; a future mark-to-market portfolio service requires explicit per-position market marks.
