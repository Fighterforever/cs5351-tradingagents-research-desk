"""Gate 6: the AI-use log must be updated for code or prompt changes.

Uses the actual PR base..head (or an explicit changed-file list, or the working
tree) to obtain changed files. When a change touches code (``*.py``) or prompt
files, ``docs/ai-use-log.yaml`` must belong to that same change set and be a
valid, non-empty log under the agreed schema. Every entry must carry the common
fields (date/tool/model/purpose/scope/review/outcome); OpenCode CLI entries must
additionally carry ``session`` and ``prompt``, while non-OpenCode (coordinator)
entries must instead carry a real ``evidence`` reference. The gate does not pass
merely because the log exists: at least one entry's ``scope`` must cover every
changed code/prompt file. A git failure is a gate failure, never "no change".
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from _gate_lib import add_change_args, changed_files, fail, resolve_root

LOG_PATH = "docs/ai-use-log.yaml"
COMMON_ENTRY_FIELDS = ("date", "tool", "model", "purpose", "scope", "review", "outcome")
OPENCODE_TOOL_FIELDS = ("session", "prompt")
COORDINATOR_EVIDENCE_FIELD = ("evidence",)
# Executable workflow / behavior-configuration paths: a change here also needs
# an AI-use log update. Ordinary prose/schema data is intentionally excluded.
BEHAVIOR_CONFIG_PATHS = {
    "pyproject.toml",
    "opencode.json",
    ".opencode/permissions.jsonc",
}


def is_code_or_prompt_change(path: str) -> bool:
    lower = path.lower()
    if path.endswith(".py"):
        return True
    if lower.startswith(".github/workflows/"):
        return True
    if path in BEHAVIOR_CONFIG_PATHS:
        return True
    return "prompt" in lower


def covers(scope_item: str, file_path: str) -> bool:
    scope_item = scope_item.rstrip("/")
    if not scope_item:
        return False
    if file_path == scope_item:
        return True
    return file_path.startswith(scope_item + "/")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 6: AI-use log required for code/prompt changes.")
    add_change_args(parser)
    args = parser.parse_args()

    root: Path = resolve_root(args.root)
    checks: list[str] = []
    failures: list[str] = []

    try:
        changed = changed_files(root, args.base_ref, args.head_ref, args.changed_files)
    except RuntimeError as exc:
        fail(checks, [f"could not resolve changed files: {exc}"])

    code_prompt = sorted(c for c in changed if is_code_or_prompt_change(c))
    checks.append(f"changed files: {len(changed)}")
    checks.append(f"code/prompt changes requiring a log update: {len(code_prompt)}")

    if not code_prompt:
        checks.append("no code/prompt changes; AI-use log not required for this change set")
        fail(checks, failures)

    if LOG_PATH not in changed:
        failures.append(f"{LOG_PATH} was not updated in this change")

    log_file = root / LOG_PATH
    if not log_file.exists():
        fail(checks, [f"code/prompt changed but {LOG_PATH} is missing"])

    try:
        data = yaml.safe_load(log_file.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(checks, [f"{LOG_PATH} is not valid YAML: {exc}"])

    checks.append(f"read {LOG_PATH}")

    if not isinstance(data, dict):
        fail(checks, [f"{LOG_PATH} is not a YAML mapping"])

    for key in ("schema_version", "project", "decision_owner"):
        if not data.get(key):
            failures.append(f"{LOG_PATH} missing top-level key: {key}")

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        failures.append(f"{LOG_PATH} must have a non-empty entries list")

    covered: set[str] = set()
    valid_entries = 0
    for i, entry in enumerate(entries or []):
        if not isinstance(entry, dict):
            failures.append(f"entries[{i}] is not a mapping")
            continue
        valid_entries += 1
        tool = entry.get("tool")
        required = list(COMMON_ENTRY_FIELDS)
        if "opencode" in str(tool).lower():
            required += list(OPENCODE_TOOL_FIELDS)
        else:
            required += list(COORDINATOR_EVIDENCE_FIELD)
        for field in required:
            if field not in entry or entry[field] in (None, ""):
                failures.append(f"entries[{i}] (tool={tool!r}) missing required field: {field}")
        scope = entry.get("scope")
        if scope is not None and not isinstance(scope, list):
            failures.append(f"entries[{i}] scope must be a list")
            scope = []
        for file_path in code_prompt:
            if any(covers(str(s), file_path) for s in (scope or [])):
                covered.add(file_path)

    checks.append(f"log entries: {len(entries or [])} (valid: {valid_entries})")

    uncovered = [f for f in code_prompt if f not in covered]
    if uncovered:
        failures.append("changed code/prompt files not covered by any log entry scope:")
        failures.extend(f"  {f}" for f in uncovered)
    else:
        checks.append("all changed code/prompt files are covered by a log entry scope")

    fail(checks, failures)


if __name__ == "__main__":
    main()
