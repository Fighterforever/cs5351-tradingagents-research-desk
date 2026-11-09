# Course deliverable index

Participant and evaluation identifier: leo. Relative contribution:1.0. Execution provenance is explained once in Report.md. The table points to actual artifacts; local verification and GitHub enforcement are reported separately.

| Deliverable | Review entry points | Evidence and scope |
|---|---|---|
| D1: requirements | req/prd.yaml; req/requirements.yaml; req/req-schema.json | 24 classified requirements with fit criteria, MoSCoW priority, inherited sources and test mappings |
| D2: architecture | ../architecture-blueprint.md; architecture/ | Authoritative blueprint; ADRs and an explicitly named appendix; invariant/trace/state/permission/policy records; candidate comparison and optional logs |
| D3: coding governance | ../AGENTS.md; code-governance/; ../.opencode/; ../.agent/ | Module and function ownership, allowed tools, role permissions, frozen human-owned rules and change process; actual candidate enforcement probe retained |
| D4: verification | code-governance/verification-constraints.md; review-memo.md; debt-register.md; bug-diary.md; ci-gates.md | Structural, regression and behavioral checks; real defects and review decisions; six gate implementations and a controlled rejection harness, with execution outcomes recorded in ci-gates.md |
| D5: supervised sessions | ../transcripts/leo-leo.md; ../transcripts/annotations/ | Seven original annotated sessions plus the release-revision intervention record, complete native records, original events and exact prompts; large native records use lossless gzip |
| D6: single report | ../Report.md; ../Report.pdf | Process report, participant record and five 300–500-word reflections; final 12pt PDF rendered from the same Markdown |
| D7: repository | ../README.md; ../.github/; ../evaluation/ci/ | Public Fighterforever/cs5351-tradingagents-research-desk; preserved upstream history and concise extension commits; six required checks and human-review protection enabled. Current cloud results are under evaluation/github |
| D8: source and tests | ../src/research_desk/; ../test/offline/; ../test/live/; ../test/fixtures/ | Application extension around the unchanged upstream graph; API-free tests separated from opt-in live evaluation; actual source data and prompt snapshots |
| D9: launch prompt | ../Prompt.md | Static plan-first execution instruction with scoped approvals and verification stages |

The 600-second MP4 is a separate submission artifact. Source ZIP preparation excludes virtual environments, local caches and credential files. The source tree preserves upstream attribution and includes evidence that can be inspected without provider access. Live reruns incur API usage and must use a fresh output root.

Prompt naming: the course layout examples prompt_v1.0.yaml and prompt_v1.1.yaml map to this repository’s first two versioned runtime snapshots, runtime-prompts-v0.1.0.yaml and runtime-prompts-v0.1.1.yaml. The current snapshot is runtime-prompts-v0.1.2.yaml; config.py defines its active version.
