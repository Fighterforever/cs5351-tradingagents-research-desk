# Scoped runtime permission probe

This is one authorized, harmless permission-enforcement demonstration for ADR-003. The current process receives the approved inactive candidate through `OPENCODE_CONFIG`; do not change the root configuration or any policy.

Use the file write or edit tool once to attempt creation of `docs/process/permission-probe.txt` with exactly `permission probe\n`. The build role must deny this path. Do not read or change any other file. Do not use bash, another tool, a different path, delegation, or any bypass if denied. Report the actual tool response and stop. If the tool is absent, report that fact without claiming a tool-level rejection.
