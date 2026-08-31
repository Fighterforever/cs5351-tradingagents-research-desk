# Install the accepted role policy, then stop

The coordinator has now confirmed that all approved source sessions are finished. Under the existing accepted leo decision in `docs/architecture/adr/003-effective-agent-permissions.md`, install the already validated candidate as the active project configuration.

Your only mutation is to copy `../orchestration/project-opencode.proposed.json` byte for byte to `opencode.json`. The candidate is the approved final version, with exact permitted shell commands, both explicit instruction files and the synchronized reviewable manifest. Do not regenerate or edit its content. Do not change the manifest, schema, rules, approvals, application source, tests, CI or documentation.

Report that the copy completed and stop immediately. Do not run any tests or add a probe; the prior real permission denial is already archived, and the coordinator will run the final six gates after the source-plus-CI commit.
