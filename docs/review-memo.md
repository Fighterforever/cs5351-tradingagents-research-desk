# Review memo

## Initial implementation review

Reviewer: leo. Scope: FR-001/002/003 and AT-01 through AT-08. Verdict: CHANGES REQUIRED for live delivery after the offline slice.

Specification alignment: evidence packaging and the operator workflow were runnable. Forty-seven extension tests passed. The code review found that the total-holdings cap, valid-sell contract and exact approval quantity binding still needed correction. These are substantive semantics rather than style findings.

Architecture alignment: the extension kept the upstream graph and placed source in src/research_desk. Direct identity/history data needed explicit observation. Exact recorded tool-argument lookup was inadequate for a fair controlled rerun because valid requests can differ between the two context modes.

Code/test quality: package installation and recovery-state failures were corrected during the first session. The next tests target real omitted boundaries. Baseline/compact must be exercised through full model inputs, not only a local empty-memory transform.

Operational metadata: original upstream suite recorded649 passed,2 skipped and71 subtests passed. Skips concerned an optional AWS dependency and an upstream live DeepSeek test with no key in that test invocation. The extension suite recorded47 passed before the semantic follow-up. No live result was claimed at this checkpoint. Source edits were made by OpenCode; the review supplied concrete corrections. Final release/PR evidence is appended after actual CI and live evaluation.
