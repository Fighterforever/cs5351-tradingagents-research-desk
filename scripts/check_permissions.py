"""Permission configuration check (part of Gate 2).

Validates the effective OpenCode permission configuration and the reviewable
``.opencode/permissions.jsonc`` manifest agree, the required rule files are
loaded, and each concrete role (plan / build / verify) cannot step outside its
approved boundary.

OpenCode does not load ``permissions.jsonc``; it is only a reviewable
projection. The authoritative file is the effective root ``opencode.json``
(candidate becomes authoritative only after installation). This check therefore
reads the effective config and verifies the manifest against it.

Evaluation model
----------------
- Path tools (read / edit / glob / grep / bash / task / skill) can carry
  granular object rules. A rule object maps a glob pattern to an action
  (allow / ask / deny); the last matching pattern wins, and agent rules are
  evaluated after global rules so they take precedence.
- Wildcards follow OpenCode's documented simple semantics: ``*`` matches zero
  or more of any character, ``?`` matches exactly one, everything else is
  literal.

The boundary assertions are the enforcement: if a protected path ever resolves
to a non-deny ``edit`` (or a forbidden path resolves to allow), the check
reports it, so a misconfigured build role that can edit approvals or a verify
role that can edit application code is detected.

Schema validation is required. The vendored official schema
``.opencode/config-schema.json`` is validated first; both the effective config
and the manifest are then validated against the real official schema (no subset
or network-fetched schema), and their projection agreement is checked. Default
mode (no ``--config``) inspects the actually installed root config and fails
until the approved candidate is installed. ``--config PATH`` enables the
focused candidate check used during preparation.

This is coding-tool enforcement, not an OS sandbox: it does not claim to stop
arbitrary malicious code inside approved tests.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RULE_FILES = (".opencode/rules.md", ".agent/rules.md")
# Projection keys the manifest is allowed to carry.
MANIFEST_KEYS = ("$schema", "permission", "agent")
REQUIRED_MANIFEST_KEYS = ("permission", "agent")

# The current accepted implementation; these deterministic authority owners and
# the policy-constant owner stay frozen after installation. Reopening them needs
# a new concrete scoped leo decision. Preserved upstream CLI and original tests
# are frozen by AGENTS.md and must not be writable by a build role.
BUILD_PROTECTED_EDIT = (
    "AGENTS.md",
    "Prompt.md",
    "README.md",
    "UPSTREAM_README.md",
    "Report.md",
    "Report.pdf",
    "architecture-blueprint.md",
    "requirements-lock.txt",
    ".opencode/rules.md",
    ".agent/rules.md",
    ".opencode/permissions.jsonc",
    ".opencode/config-schema.json",
    "opencode.json",
    "docs/process/test-approval.yaml",
    "docs/process/APPROVAL_PACKET.md",
    "docs/architecture/adr/001-application-extension.md",
    "tradingagents/agents/analysts.py",
    "cli/main.py",
    "tests/test_analyst_execution.py",
    "src/research_desk/config.py",
    "src/research_desk/policy.py",
    "src/research_desk/review.py",
    "src/research_desk/storage.py",
    "src/research_desk/models.py",
)
# The approved application/test/CI paths a build role must be able to write.
BUILD_ALLOWED_EDIT = (
    "src/research_desk/budget.py",
    "src/research_desk/cli.py",
    "test/offline/test_at01_replay.py",
    "test/offline/test_evidence_message_roundtrip.py",
    "scripts/check_permissions.py",
    "scripts/check_static.py",
    "pyproject.toml",
)
# A verify role must never edit application code or tests (weakening a test is
# forbidden); it may write only verification output.
VERIFY_FORBIDDEN_EDIT = (
    "src/research_desk/budget.py",
    "src/research_desk/config.py",
    "test/offline/test_at01_replay.py",
    "tests/test_data.py",
)
VERIFY_ALLOWED_EDIT = ("verification/report.md",)
# A plan role must not modify implementation or approve work; it writes only
# proposed plan documents.
PLAN_FORBIDDEN_EDIT = (
    "src/research_desk/budget.py",
    "src/research_desk/policy.py",
    "AGENTS.md",
    "docs/process/test-approval.yaml",
)
PLAN_ALLOWED_EDIT = ("proposals/plan.md",)

# Reachable shell write bypasses that must never resolve to allow, and the exact
# intended commands that must stay allowed. No allow command may carry a glob.
BUILD_BASH_DENY = (
    "git diff --output docs/process/permission-probe.txt",
    "git log --output opencode.json",
)
BUILD_BASH_ALLOW = ("git diff --stat",)
VERIFY_BASH_DENY = (
    ".venv/bin/python scripts/check_gate_examples.py --output opencode.json",
    ".venv/bin/pytest tests --basetemp docs/process",
)
VERIFY_BASH_ALLOW = (".venv/bin/python scripts/check_static.py --base-ref v0.4.0 --head-ref HEAD",)


def _wildcard_to_regex(pattern: str) -> re.Pattern[str]:
    """Convert OpenCode's simple wildcard pattern to a compiled regex.

    ``*`` -> zero or more of any character; ``?`` -> exactly one character;
    all other characters match literally.
    """
    out: list[str] = []
    for ch in pattern:
        if ch == "*":
            out.append(".*")
        elif ch == "?":
            out.append(".")
        else:
            out.append(re.escape(ch))
    return re.compile("".join(out))


def _resolve(tool_rules: dict[str, str], target: str) -> str | None:
    """Resolve the effective action for ``target`` under object rules.

    The last matching pattern wins, per OpenCode's documented semantics.
    """
    action: str | None = None
    for pattern, value in tool_rules.items():
        if value not in ("allow", "ask", "deny"):
            continue
        if _wildcard_to_regex(pattern).fullmatch(target):
            action = value
    return action


def _effective_rules(config: dict, role: str, tool: str) -> dict[str, str]:
    """Merge global + agent rules for ``role``/``tool``, agent rules last.

    Evaluating agent rules after global rules gives them precedence and
    preserves last-matching-wins within each source.
    """
    merged: dict[str, str] = {}
    global_rules = (config.get("permission") or {}).get(tool)
    agent_rules = (
        (config.get("agent") or {}).get(role, {}).get("permission", {}).get(tool)
    )
    for rules in (global_rules, agent_rules):
        if isinstance(rules, dict):
            merged.update(rules)
    return merged


def _expect_deny(config: dict, role: str, tool: str, paths: tuple[str, ...],
                 why: str, failures: list[str]) -> None:
    for target in paths:
        action = _resolve(_effective_rules(config, role, tool), target)
        if action != "deny":
            failures.append(
                f"{role} role must NOT be able to {tool} {target} "
                f"({why}); resolved action is {action!r}"
            )


def _expect_allow(config: dict, role: str, tool: str, paths: tuple[str, ...],
                  why: str, failures: list[str]) -> None:
    for target in paths:
        action = _resolve(_effective_rules(config, role, tool), target)
        if action != "allow":
            failures.append(
                f"{role} role must be able to {tool} {target} "
                f"({why}); resolved action is {action!r}"
            )


def _load_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _load_schema(path: Path, failures: list[str]) -> dict | None:
    if not path.exists():
        failures.append(f"official schema not found at {path}; schema validation is required")
        return None
    try:
        import importlib.util

        if importlib.util.find_spec("jsonschema") is None:
            raise ImportError
    except ImportError:
        failures.append("jsonschema is not installed; schema validation is required")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        failures.append(f"invalid official schema at {path}: {exc}")
        return None


def _check_schema(instance: dict, name: str, schema_path: Path, failures: list[str]) -> None:
    schema = _load_schema(schema_path, failures)
    if schema is None:
        return
    import jsonschema  # already confirmed available by _load_schema

    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        failures.append(f"{name} does not match the official OpenCode schema: {error.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Permission configuration check.")
    parser.add_argument("--root", default=None, help="Repository root (defaults to project root).")
    parser.add_argument("--config", default=None,
                        help="Effective config file to inspect (default: <root>/opencode.json).")
    parser.add_argument("--schema", default=None,
                        help="Official OpenCode config schema (default: <root>/.opencode/config-schema.json).")
    parser.add_argument("--manifest", default=None,
                        help="Reviewable permission manifest (default: <root>/.opencode/permissions.jsonc).")
    args = parser.parse_args()

    root = (
        Path(args.root).resolve()
        if args.root
        else Path(__file__).resolve().parent.parent
    )

    config_path = Path(args.config).resolve() if args.config else root / "opencode.json"
    schema_path = (
        Path(args.schema).resolve()
        if args.schema
        else root / ".opencode" / "config-schema.json"
    )
    manifest_path = (
        Path(args.manifest).resolve()
        if args.manifest
        else root / ".opencode" / "permissions.jsonc"
    )

    checks: list[str] = []
    failures: list[str] = []

    try:
        config = _load_json(config_path)
        manifest = _load_json(manifest_path)
    except ValueError as exc:
        failures.append(str(exc))
        return _report(checks, failures)

    if config is None:
        failures.append(f"missing effective config: {config_path}")
    if manifest is None:
        failures.append(f"missing permission manifest: {manifest_path}")
    if failures:
        return _report(checks, failures)

    checks.append(f"read effective config {config_path}")
    checks.append(f"read manifest {manifest_path}")
    checks.append(f"official schema {schema_path}")

    # Required schema validation of BOTH the config and the manifest.
    _check_schema(config, "effective config", schema_path, failures)
    _check_schema(manifest, "manifest", schema_path, failures)

    # Required rule files must be loaded through the instructions array.
    instructions = config.get("instructions")
    if not isinstance(instructions, list):
        failures.append("config must declare an instructions array")
    else:
        for rule in RULE_FILES:
            if rule not in instructions:
                failures.append(f"required rule file is not loaded via instructions: {rule}")
    checks.append(
        "instructions rules present: "
        + f"{[r for r in RULE_FILES if r in (instructions or [])]}"
    )

    # Manifest is a projection using only $schema / permission / agent.
    unknown_keys = [k for k in manifest if k not in MANIFEST_KEYS]
    if unknown_keys:
        failures.append(f"manifest carries unsupported keys: {sorted(unknown_keys)}")
    for key in REQUIRED_MANIFEST_KEYS:
        if key not in manifest:
            failures.append(f"manifest missing required projection key: {key}")

    # Agreement: manifest projection must equal the effective global permission
    # and role definitions.
    if manifest.get("permission") != config.get("permission"):
        failures.append("manifest permission projection does not match the effective config")
    if manifest.get("agent") != config.get("agent"):
        failures.append("manifest agent projection does not match the effective config")
    checks.append("manifest agrees with effective permission and agent definitions")

    # Default policy must be no access until granted: global and bash catch-alls
    # must be deny, and network/delegation/external tools must be denied.
    global_permission = config.get("permission") or {}
    if global_permission.get("*") != "deny":
        failures.append("global permission default must be deny (no access until granted)")
    bash_default = global_permission.get("bash")
    if isinstance(bash_default, dict) and bash_default.get("*") != "deny":
        failures.append("global bash default must be deny")
    for tool in ("webfetch", "websearch", "task", "external_directory"):
        if global_permission.get(tool) != "deny":
            failures.append(f"global {tool} must be denied")

    # Concrete role boundaries (edit tool is the write authority).
    _expect_deny(config, "build", "edit", BUILD_PROTECTED_EDIT,
                 "protected rule/approval/frozen-upstream/safety path", failures)
    _expect_allow(config, "build", "edit", BUILD_ALLOWED_EDIT,
                  "approved application/test/CI path", failures)
    _expect_deny(config, "verify", "edit", VERIFY_FORBIDDEN_EDIT,
                 "verify must not edit source or weaken tests", failures)
    _expect_allow(config, "verify", "edit", VERIFY_ALLOWED_EDIT,
                  "verification output only", failures)
    _expect_deny(config, "plan", "edit", PLAN_FORBIDDEN_EDIT,
                 "plan must not modify implementation or approve work", failures)
    _expect_allow(config, "plan", "edit", PLAN_ALLOWED_EDIT,
                  "proposed plan documents only", failures)

    # A build role must never bypass file-tool write restrictions through bash.
    if _resolve(_effective_rules(config, "build", "bash"), "python -c 1") == "allow":
        failures.append("build role must not run arbitrary python via bash")
    if _resolve(_effective_rules(config, "build", "bash"), "bash -c 1") == "allow":
        failures.append("build role must not run nested shell via bash")
    # Verify must not run arbitrary python or shell interpreters.
    if _resolve(_effective_rules(config, "verify", "bash"), "python -c 1") == "allow":
        failures.append("verify role must not run arbitrary python via bash")
    if _resolve(_effective_rules(config, "verify", "bash"), "bash -c 1") == "allow":
        failures.append("verify role must not run a shell interpreter via bash")
    # The concrete reachable shell write bypasses must resolve to deny.
    _expect_deny(config, "build", "bash", BUILD_BASH_DENY,
                 "reachable git --output write bypass", failures)
    _expect_allow(config, "build", "bash", BUILD_BASH_ALLOW,
                  "exact intended build command", failures)
    _expect_deny(config, "verify", "bash", VERIFY_BASH_DENY,
                 "reachable --output/--basetemp write bypass", failures)
    _expect_allow(config, "verify", "bash", VERIFY_BASH_ALLOW,
                  "exact intended verification gate command", failures)
    # No role may delegate to a subagent or reach the network in this workflow.
    for role in ("plan", "build", "verify"):
        for tool, why in (("task", "subagent delegation"), ("webfetch", "network fetch"),
                          ("websearch", "web search")):
            if config.get("agent", {}).get(role, {}).get("permission", {}).get(tool) == "allow":
                failures.append(f"{role} role must not allow {tool} ({why})")

    return _report(checks, failures)


def _report(checks: list[str], failures: list[str]) -> int:
    for line in checks:
        print(line)
    print("RESULT: FAIL" if failures else "RESULT: PASS")
    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"- {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
