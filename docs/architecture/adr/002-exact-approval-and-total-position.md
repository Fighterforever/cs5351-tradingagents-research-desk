# ADR-002: Bind approval to exact terms and cap total holdings

Status: accepted by leo during implementation review, 2026-08-31. Requirements: FR-002, INV-001, INV-002. This clarifies the approved policy rather than adding a new feature.

The first generated implementation treated the10% cap as a limit on one new ticket. It also excluded Sell/Underweight even though the plan prohibited shorting rather than all sales. Its approval fingerprint omitted quantity and evidence identity. These behaviors would allow repeated individually small buys to exceed the policy or allow changed terms to reuse an earlier approval.

The correct unit is the total position after a purchase, valued at the current ticker's frozen evidence mark. Other position marks must be explicit under the supported ledger convention. A sell reduces owned shares and is permitted only within that holding. Hold and REVIEW remain nontradeable. Approval binds symbol, date, normalized side, price, shares and material evidence identity. Changed terms cause REVIEW_REQUIRED. The operator can review and approve corrected terms; this state must not become a dead end.

The smallest owners are policy.py for business decisions, review.py for binding and transitions, storage.py for signed position updates, and models.py for explicit fields. Upstream agent code has no reason to change. Tests cover a second buy in an existing position, a valid sell, overselling and quantity changes after approval. The source of truth for completion is the final offline test log, not this acceptance decision.

The10% concentration test applies when buying. A valid sale can reduce a position that became overweight through a price rise, even when the remaining holding is still above10%. Such a sale cannot create a short position. Rejecting risk-reducing sales would add an unapproved constraint to the original policy. The direct boundary example holds100 shares bought at100 with90000 cash, marks them at200, and permits a sale of10 shares; it leaves90000 +2000 cash and90 shares.
