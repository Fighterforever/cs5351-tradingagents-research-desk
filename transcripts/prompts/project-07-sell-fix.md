# One final policy correction; do not touch graph, evidence or CI

The frozen-identity/full-judge task is complete (65tests/mypy pass). The coordinator and leo accepted one precise interpretation already implicit in original FR002/INV002 and now explicit in ADR-002:

The10% concentration check applies after a BUY. A valid SELL that reduces an owned position must be permitted even if price appreciation means the remaining holding is still above10%. evaluate_sell currently adds a remaining-position cap check, which is an extra unapproved restriction.

Change only policy.py and one meaningful sell regression in existing/new test/offline file. Keep positive integer quantity, evidence price and no-short checks. Keep the buy total-holdings cap unchanged. Example reachable state:100 shares acquired at100, cash90000; new evidence mark200 means18.18% concentration. Selling10 shares is valid and leaves cash92000 and90 shares, even though remaining value18000 still exceeds10% of equity110000. A sell over100 must still fail. Do not alter ledger authority, approval binding or graph/evidence code (another OpenCode session owns evidence.py).

Run the relevant policy/ledger tests and stop. No broad cleanup, no live requests, no docs edits. All decisions use leo; this is a correction within approved AT04/05, not new scope.
