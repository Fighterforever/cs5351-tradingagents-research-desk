# Project launch prompt

Read `AGENTS.md` and its reading order. Before generating code, produce a concrete execution plan identifying requirement IDs, modules, declared interfaces, scope boundaries, tests and implementation steps. Identify any safety-relevant paths and cite the applicable ADR.

Check for a leo approval of this exact plan and its tests that predates implementation. An existing approval is reusable only within its recorded scope. The approved three-feature plan and AT-01 through AT-08 in `docs/process/test-approval.yaml` authorize the current delivery. For a new scope or changed safety policy, stop after a reviewable plan and obtain a new decision; never create an approval on behalf of the implementation agent.

After approval, build the smallest complete vertical slice on the real upstream application. Run the approved acceptance examples. Present behavior, test evidence and concrete unresolved issues for the next stage decision. Preserve the build, verification and release stage records. Do not treat a textual PASS as evidence.

Generate all application/test/CI code through OpenCode. Preserve upstream behavior. Record actual model settings and sessions. Runtime model requests use environment credentials provided by the host; inspect neither user secrets nor unrelated services. A finished delivery includes runnable source, source-linked requirements, architecture contracts, all prior regression tests, real evidence packs, comparison results, AI-use records, the process report and genuine GitHub check evidence.
