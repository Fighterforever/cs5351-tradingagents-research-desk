"""Gate 2: lint, types, dependencies and the deterministic authority boundary.

Runs ``ruff check .`` over the repository, a meaningful mypy check over the new
``src/research_desk`` package (``--follow-imports=skip`` so the untouched
upstream package is not silently made part of the new type contract), and
``python -m pip check`` for dependency consistency. It then scans the policy /
review / storage / graph-adapter modules for the structural authority boundary:
``review`` and ``policy`` must never import an LLM (including direct provider
modules and upstream LLM factories), and the graph must never import a function
that grants approval or mutates the ledger.

Genuine application lint/type findings are reported with file:line and the gate
fails; this implementation does not own application source, so findings are
surfaced to the supervisor rather than suppressed.

In PR mode, a change on a safety-relevant path must carry, in the same diff, a
changed ADR that references the changed owner/path AND a changed concrete
approval record carrying the real APPROVED marker and owner.
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

import yaml
from _gate_lib import add_change_args, changed_files, fail, resolve_root, run, tool_path

# Modules that own deterministic authority and therefore must not touch an LLM.
NO_LLM_MODULES = ("policy", "review")
# Top-level LLM providers / frameworks the authority owners must not import.
LLM_PROVIDER_PREFIXES = (
    "langchain",
    "openai",
    "anthropic",
    "google",
    "google_genai",
    "zhipu",
    "zhipuai",
    "minimax",
    "openrouter",
    "dashscope",
    "dashscopen",
    "bedrock",
    "boto3",
)
# Upstream LLM factory names (checked by original imported name, not only alias).
LLM_FACTORY_NAMES = {"create_llm_client", "create_llm"}
# Functions that grant approval or mutate the ledger; the graph must not import them.
LEDGER_AUTHORITY_NAMES = {
    "approve",
    "execute",
    "apply_transaction",
    "ResearchDeskStore",
    "save_proposal",
}
# Safety-relevant paths (deterministic authority, persistent models, permission
# and rule/config files as declared by permission-model.md).
SAFETY_PATHS = (
    "src/research_desk/policy.py",
    "src/research_desk/review.py",
    "src/research_desk/storage.py",
    "src/research_desk/config.py",
    "src/research_desk/models.py",
    ".agent/rules.md",
    ".opencode/rules.md",
    ".opencode/permissions.jsonc",
    ".opencode/config-schema.json",
    "opencode.json",
)
APPROVAL_DOC = "docs/process/test-approval.yaml"
ADR_PREFIX = "docs/architecture/adr/"
APPROVER = "leo"


def _import_names(tree: ast.Module) -> tuple[list[str], list[str]]:
    """Return (top-level module names, imported original member names).

    Uses the *original* imported names (``alias.name``) rather than only
    aliases, so ``from x import approve as y`` is still detected.
    """
    modules: list[str] = []
    members: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.append(node.module)
            members.extend(alias.name for alias in node.names)
    return modules, members


def check_authority_boundary(root: Path, failures: list[str]) -> None:
    for mod in NO_LLM_MODULES:
        path = root / "src/research_desk" / f"{mod}.py"
        if not path.exists():
            failures.append(f"authority module missing: {path}")
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        modules, members = _import_names(tree)
        offending_modules = [
            m
            for m in modules
            if m.startswith(LLM_PROVIDER_PREFIXES) or m.startswith("tradingagents.llm_clients")
        ]
        offending_factories = [m for m in members if m in LLM_FACTORY_NAMES]
        if offending_modules or offending_factories:
            detail: list[str] = []
            if offending_modules:
                detail.append(f"LLM/provider imports: {sorted(set(offending_modules))}")
            if offending_factories:
                detail.append(f"LLM factory names: {sorted(set(offending_factories))}")
            failures.append(f"{mod}.py must not touch an LLM; {'; '.join(detail)}")

    graph_path = root / "src/research_desk/graph_adapter.py"
    if graph_path.exists():
        tree = ast.parse(graph_path.read_text(encoding="utf-8"))
        modules, members = _import_names(tree)
        forbidden = sorted(LEDGER_AUTHORITY_NAMES & set(members))
        if forbidden:
            failures.append(
                f"graph_adapter.py must not import approval/ledger-mutation "
                f"functions; found: {forbidden}"
            )
        if any(m == "research_desk.storage" or m.endswith(".storage") for m in modules):
            failures.append("graph_adapter.py must not import research_desk.storage")


def _adr_accepted_by_leo(path: Path) -> bool:
    """A changed ADR only counts as a decision if it is accepted by leo."""
    head = "\n".join(path.read_text(encoding="utf-8", errors="ignore").splitlines()[:6])
    lower = head.lower()
    return "accepted" in lower and APPROVER in lower


def _normalize_declared(token: str) -> str:
    """Normalize an ADR-declared token to an exact project-relative path."""
    t = re.sub(r"^\./", "", token.strip())  # drop a leading './' only
    if t.endswith("/"):
        return t.rstrip("/")
    if t.startswith("src/") or t.startswith(".opencode/") or t.startswith(".agent/"):
        return t
    if "/" in t:
        return t
    if t.endswith(".py"):
        return "src/research_desk/" + t
    return t


def _adr_declared_paths(text: str) -> set[str]:
    """Explicitly declared affected paths in an ADR (code spans + bare .py owners)."""
    paths: set[str] = set()
    for token in re.findall(r"`([^`]+)`", text):
        if "/" in token or token.endswith((".py", ".jsonc", ".json", "/")):
            paths.add(_normalize_declared(token))
    for match in re.findall(r"\b([A-Za-z_][\w]*\.py)\b", text):
        paths.add("src/research_desk/" + match)
    return paths


def check_safety_path_evidence(
    root: Path, changed: list[str], failures: list[str]
) -> None:
    safety_changed = [c for c in changed if c in SAFETY_PATHS]
    if not safety_changed:
        return
    checks_ok = True
    changed_set = set(changed)
    adr_changed = sorted(
        p for p in changed if p.startswith(ADR_PREFIX) and p.endswith(".md")
    )
    approval_changed = APPROVAL_DOC in changed_set

    accepted_adrs = [p for p in adr_changed if _adr_accepted_by_leo(root / p)]
    if not accepted_adrs:
        failures.append(
            "safety-path change requires an ADR accepted by leo that is changed "
            "in this same diff; none present"
        )
        checks_ok = False
    if not approval_changed:
        failures.append(
            f"safety-path change requires {APPROVAL_DOC} changed in this same diff"
        )
        checks_ok = False

    declared: set[str] = set()
    for p in accepted_adrs:
        declared |= _adr_declared_paths(
            (root / p).read_text(encoding="utf-8", errors="ignore")
        )
    for path in safety_changed:
        if path not in declared:
            failures.append(
                f"changed safety path {path} is not listed among the affected "
                "paths of an ADR accepted by leo that is changed in this same diff"
            )
            checks_ok = False

    approval_path = root / APPROVAL_DOC
    if approval_path.exists():
        try:
            data = yaml.safe_load(approval_path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            data = None
        if not isinstance(data, dict) or (
            data.get("decision") != "APPROVED" or data.get("approver") != APPROVER
        ):
            failures.append(
                f"{APPROVAL_DOC} must carry decision=APPROVED and approver={APPROVER!r} "
                "(YAML fields)"
            )
            checks_ok = False
    if checks_ok:
        print("safety-path change carries a changed ADR accepted by leo + updated approval evidence")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 2: static/type/dependency + boundary.")
    add_change_args(parser)
    args = parser.parse_args()

    root: Path = resolve_root(args.root)
    checks: list[str] = []
    failures: list[str] = []

    ruff = tool_path(root, "ruff")
    proc = run([ruff, "check", "."], root)
    checks.append(f"ruff check . -> exit {proc.returncode}")
    if proc.returncode != 0:
        findings = [
            line for line in (proc.stdout or "").splitlines()
            if ": error:" in line or ": warning:" in line
        ]
        if not findings:
            findings = (proc.stdout or "").splitlines()[:40]
        failures.append("ruff reported lint findings:")
        failures.extend(f"  {f}" for f in findings)

    mypy = tool_path(root, "mypy")
    mproc = run(
        [mypy, "src/research_desk", "--follow-imports=skip", "--ignore-missing-imports"],
        root,
    )
    checks.append(f"mypy src/research_desk -> exit {mproc.returncode}")
    if mproc.returncode != 0:
        findings = [
            line for line in (mproc.stdout or "").splitlines() if ": error:" in line
        ]
        if not findings:
            findings = (mproc.stdout or "").splitlines()[:40]
        failures.append("mypy reported type findings (src/research_desk):")
        failures.extend(f"  {f}" for f in findings)

    py = tool_path(root, "python") or "python"
    pproc = run([py, "-m", "pip", "check"], root)
    checks.append(f"pip check -> exit {pproc.returncode}")
    if pproc.returncode != 0:
        failures.append("pip check reported broken requirements:")
        failures.extend(f"  {line}" for line in (pproc.stdout or "").splitlines())

    check_authority_boundary(root, failures)

    # Permission configuration: the reviewable manifest must agree with the
    # effective root config and every role must stay inside its boundary. This
    # makes the permission check part of Gate 2 and propagates any failure.
    perm_py = tool_path(root, "python") or "python"
    perm_proc = run([perm_py, str(root / "scripts/check_permissions.py"), "--root", str(root)], root)
    checks.append(f"check_permissions.py -> exit {perm_proc.returncode}")
    if perm_proc.returncode != 0:
        failures.append("permission configuration check failed:")
        failures.extend(
            f"  {line}" for line in (perm_proc.stdout or "").splitlines()
        )
        failures.extend(
            f"  {line}" for line in (perm_proc.stderr or "").splitlines()
        )

    try:
        changed = changed_files(root, args.base_ref, args.head_ref, args.changed_files)
    except RuntimeError as exc:
        fail(checks, [f"could not resolve changed files: {exc}"])
    if changed:
        check_safety_path_evidence(root, changed, failures)

    fail(checks, failures)


if __name__ == "__main__":
    main()
