# Annotated OpenCode session 1: offline vertical slice

Session: ses_fa849396effeNN2dsVIpTIaax8. Full raw record: project-01.raw.jsonl. Full native export: project-01.full.json. Sanitized convenience export: project-01.export.json. Launch prompt: prompts/project-01-offline.md.

The concrete plan and AT-01 through AT-08 were approved at2026-08-31T12:05:17.791955+00:00. The first implementation event is2026-08-31T12:06:32.695+00:00, obtained from the raw event timestamp. This ordering is checked by the approval gate.

OpenCode read the upstream contracts and generated the application modules, fixtures and tests. The record includes the real failing test rounds and corrections. At the useful offline milestone,47 extension tests passed. The separately executed unmodified upstream suite recorded649 passing tests,2 skips and71 subtests.

Intervention1: require the real upstream graph and application-owned seams rather than a replacement demonstration. Rationale: preserve existing system behavior and make the baseline comparison meaningful.

Intervention2: review package installation and the CLI vertical slice after generation. The first package import failure exposed missing src-layout discovery. Rationale: an application module is not delivered until its installed entry point works.

Intervention3: after the passing offline slice, inspect policy and approval semantics. The review identified a ticket-only cap, excluded valid sells and approval content that omitted quantity/evidence binding. ADR-002 records the required correction. Rationale: passing examples on an empty portfolio do not establish the total-holdings invariant.

Intervention4: terminate the session after its useful milestone when it continued cleanup and lint work. Source changes and raw output were retained. Rationale: the next unresolved acceptance item was real research/evaluation; a fresh focused session reduced repeated context cost.

