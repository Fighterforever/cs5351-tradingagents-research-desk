# Final concrete shell boundary correction; leave root config inactive

The current candidate has two reachable write bypasses: `git diff *` / `git log *` can accept Git's `--output` option, and `scripts/check_gate_examples.py *` accepts an arbitrary `--output` target. Broad pytest suffix arguments also permit an arbitrary `--basetemp` location. These conflict with the already approved role write boundaries.

Only edit `../orchestration/project-opencode.proposed.json`, `.opencode/permissions.jsonc`, and `scripts/check_permissions.py`. Do not edit or activate `opencode.json`, rules, approvals, application code, tests or any other file.

Replace ALL build/verify bash suffix-wildcard allows with explicit needed commands. Build can have `pwd`, `ls`, `git status`, `git status --short`, `git diff`, `git diff --stat`, `git diff --name-only`, `git log`, `git log -n 5 --oneline`. Do not allow arbitrary trailing arguments or shell interpreters.

Verify can have `pwd`, `ls`, `git status`, `git status --short`; the approved `.venv/bin/pytest tests`, `.venv/bin/pytest test/offline`, `.venv/bin/pytest tests test/offline`, and their explicit `-q` variants; the already listed named `.venv/bin/python scripts/check_*.py` commands with no arguments; the six change-aware gate commands with the exact suffix `--base-ref v0.4.0 --head-ref HEAD`; and the explicit `check_gate_examples.py --output verification/negative-examples.json`. Avoid a glob in any allow command. The human coordinator can run the evidence runner from its own terminal; it does not need a verify-role blanket grant.

Add just a few meaningful checker assertions for the actual reachable bypass commands: `git diff --output docs/process/permission-probe.txt`, `git log --output opencode.json`, `.venv/bin/python scripts/check_gate_examples.py --output opencode.json`, and `.venv/bin/pytest tests --basetemp docs/process`. They must resolve to deny. Also assert one exact intended build command and one exact intended verification gate command resolve to allow. Keep the existing matcher and validation structure.

Run only the candidate permission/schema check and ruff on the changed checker, then stop. Root configuration remains unchanged until the coordinator confirms source freeze.
