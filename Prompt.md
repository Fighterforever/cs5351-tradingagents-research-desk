# Project launch prompt

Read `AGENTS.md` and the files in its reading order.

## Plan

Identify the requirement IDs and link each one to the affected module and interface. Define the scope, the acceptance cases and the implementation steps. Cite the relevant ADR for changes to approval, policy or persisted data. Name the tests and the evidence each test will produce.

Present the plan and tests to a team member. Stop before generating code. Record the member’s decision, scope and time in the project record. The approvals in `docs/process/test-approval.yaml` document earlier decisions. Each launch needs a human decision on the plan just presented.

## Build

After approval, use OpenCode to implement the approved change in the upstream application or its extension. Use OpenCode for application code, tests and CI. Follow the ownership rules in `AGENTS.md`. Record the model settings and original session. Use credentials supplied through the runtime environment.

At the end of the build, present the change and its requirement links. Stop for a human decision before moving to verification. If the scope changes, submit the revised plan and tests for approval.

## Verify and release

Run the approved tests. Show the observed behavior, command output and unresolved issues. Include the evidence packs and measured results for an experiment. Stop for a human release decision. Keep the decision with the review memo and preserve the original session, approval record and GitHub checks.
