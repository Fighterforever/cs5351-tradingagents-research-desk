"""Gate 6 matches changed code and runtime prompt paths to new or amended AI-use log
entries relative to Git. It verifies evidence and review files plus the original prompt
and session ID for OpenCode.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from _gate_lib import add_change_args, changed_files, fail, read_base_text, resolve_root

LOG_PATH = "docs/ai-use-log.yaml"
COMMON_ENTRY_FIELDS = ("date", "tool", "model", "purpose", "scope", "review", "outcome")
OPENCODE_TOOL_FIELDS = ("session", "prompt")
COORDINATOR_EVIDENCE_FIELD = ("evidence",)
BEHAVIOR_CONFIG_PATHS = {
    "pyproject.toml",
    "opencode.json",
    ".opencode/permissions.jsonc",
}
ARCHIVE_PREFIXES = ("transcripts/", "evaluation/")


def is_code_or_prompt_change(path: str) -> bool:
    lower = path.lower()
    if path.endswith(".py"):
        return True
    if lower.startswith(".github/workflows/"):
        return True
    if path in BEHAVIOR_CONFIG_PATHS:
        return True
    if lower.startswith(ARCHIVE_PREFIXES):
        return False
    if Path(path).name == "Prompt.md" or "prompts/" in lower:
        return True
    return "prompt" in lower


def covers(scope_item: str, file_path: str) -> bool:
    scope_item = scope_item.rstrip("/")
    if not scope_item:
        return False
    if file_path == scope_item:
        return True
    return file_path.startswith(scope_item + "/")


def _real_file(root: Path, value) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    raw = Path(value)
    if raw.is_absolute():
        return False
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return False
    return candidate.is_file()


def _normalize_scope(scope) -> list[str] | None:
    if not isinstance(scope, list) or not scope:
        return None
    out = []
    for item in scope:
        if not isinstance(item, str) or not item.strip():
            return None
        item = item.strip()
        if Path(item).is_absolute() or ".." in Path(item).parts:
            return None
        out.append(item)
    return out


def _entry_covers_any(entry: dict, files: list[str]) -> set[str]:
    scope = _normalize_scope(entry.get("scope"))
    if scope is None:
        return set()
    return {f for f in files if any(covers(s, f) for s in scope)}


def validate_entries(root, entries, previous_entries, changed_paths) -> list[str]:
    root = Path(root)
    failures: list[str] = []
    code_prompt = [p for p in changed_paths if is_code_or_prompt_change(p)]

    changed_entries = []
    for i, entry in enumerate(entries or []):
        if not isinstance(entry, dict):
            failures.append(f"entries[{i}] is not a mapping")
            continue
        if any(entry == prev for prev in previous_entries or [] if isinstance(prev, dict)):
            continue
        changed_entries.append((i, entry))

    covered: set[str] = set()
    for i, entry in changed_entries:
        tool = entry.get("tool")
        is_opencode = "opencode" in str(tool).lower()
        required = list(COMMON_ENTRY_FIELDS)
        required += list(OPENCODE_TOOL_FIELDS if is_opencode else COORDINATOR_EVIDENCE_FIELD)
        for field in required:
            if field not in entry or entry[field] in (None, ""):
                failures.append(f"entries[{i}] (tool={tool!r}) missing required field: {field}")
        if not _real_file(root, entry.get("review")):
            failures.append(f"entries[{i}] review is not a repo-local file: {entry.get('review')!r}")
        if is_opencode:
            session = entry.get("session")
            if not isinstance(session, str) or not session.strip():
                failures.append(f"entries[{i}] session must be a nonempty string: {session!r}")
            if not _real_file(root, entry.get("prompt")):
                failures.append(f"entries[{i}] prompt is not a repo-local file: {entry.get('prompt')!r}")
        if not _real_file(root, entry.get("evidence")):
            failures.append(f"entries[{i}] evidence is not a repo-local file: {entry.get('evidence')!r}")
        if _normalize_scope(entry.get("scope")) is None:
            failures.append(f"entries[{i}] scope must be a nonempty list of project-relative paths")
        covered |= _entry_covers_any(entry, code_prompt)

    uncovered = [f for f in code_prompt if f not in covered]
    if uncovered:
        failures.append("changed code/prompt files not covered by any changed log entry scope:")
        failures.extend(f"  {f}" for f in uncovered)
    return failures


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

    previous_entries = []
    try:
        base_text = read_base_text(root, args.base_ref or "HEAD", LOG_PATH)
    except Exception as exc:
        fail(checks, failures + [f"could not read baseline {LOG_PATH}: {exc}"])

    if base_text is not None:
        try:
            prev_data = yaml.safe_load(base_text)
        except yaml.YAMLError as exc:
            fail(checks, failures + [f"baseline {LOG_PATH} is not valid YAML: {exc}"])
        if isinstance(prev_data, dict) and isinstance(prev_data.get("entries"), list):
            previous_entries = prev_data["entries"]
        elif prev_data is not None:
            fail(checks, failures + [f"baseline {LOG_PATH} has malformed entries"])

    failures.extend(validate_entries(root, entries or [], previous_entries, code_prompt))
    checks.append(f"log entries: {len(entries or [])}")

    fail(checks, failures)


if __name__ == "__main__":
    main()
