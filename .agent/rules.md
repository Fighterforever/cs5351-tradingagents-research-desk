# Project covenant

Owner: leo. ADR-001 governs the application extension; ADR-002 clarifies exact approval and total holdings.

Use the smallest abstraction that owns the behavior. No replacement upstream graph, speculative framework or unrelated refactor. Reuse pinned dependencies unless a requirement demonstrates a missing capability. Keep public contracts unchanged outside the approved seams.

Each feature has an independent negative test. Every safety-relevant code change requires a corresponding ADR and leo approval. Verification cannot lower a threshold or delete a failing case without a recorded requirement decision. The final suite includes every earlier test suite.

When a requirement changes, update this covenant and the effective rules within the same delivery cycle, which is shorter than one sprint. Preserve evidence of the old decision and the reason for change. Credentials and real trading stay outside this project.


ADR-004 adds terminal rejection, complete-input budgets and source-bound release quality. The same revision updates requirements, tests and review evidence. The user-authorized temporary revision role ends at source freeze.
