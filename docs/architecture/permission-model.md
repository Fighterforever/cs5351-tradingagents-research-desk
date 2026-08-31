# Permission model

The principle is no access until a role needs a path. The machine-readable permissions and effective OpenCode configuration must agree; a file named permissions.jsonc alone is not enforcement. The host keeps credentials outside agent-readable files and injects only the application's runtime environment.

| Role | Read | Write | Forbidden |
|---|---|---|---|
| Plan | AGENTS, Prompt, docs, public upstream source, src/test declarations | proposed plan documents | Application implementation, approvals, secrets |
| Build | Approved requirements/architecture/tests, src, test, pyproject | src/research_desk, approved test files, scoped package metadata | Human-owned rules/approval decisions, global config, upstream replacement |
| Verify | Source, tests, requirements, frozen fixtures, run evidence | verification outputs and proposed test changes | Granting approval, weakening requirements, editing source to force a result |
| Release | Final artifacts and local git state | package, workflow evidence, authorized private remote | Publishing credentials, public release, real orders |
| leo | All project decisions and review evidence | Plans, ADRs, rules, concrete stage approvals | Falsifying raw sessions or measured results |

Runtime authority is separate from coding-agent permissions. The graph has market/news tools and model access. It has no review, execute or ledger tool. The local operator commands own approval and execution. This is a single-user workstation boundary, not a claim of production identity assurance.

Safety-relevant paths include policy.py, review.py, storage.py, config.py, model contracts, permission configuration and rule files. Changes need a reviewed ADR plus a corresponding approval record. Current fixes to total holdings, valid sells and exact approval binding are covered by ADR-002 and the approved AT-04/05 semantics.
