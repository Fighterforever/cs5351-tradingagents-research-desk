# TradingAgents Research Desk

Research Desk extends **TradingAgents v0.4.0** with portable research evidence, zero-network replay, an explicitly approved paper ledger and a measured baseline/compact context experiment. The real upstream market/news, research, trader, risk and portfolio graph remains the research engine. The language model advises; deterministic application code controls paper execution.

Course repository: [Fighterforever/cs5351-tradingagents-research-desk](https://github.com/Fighterforever/cs5351-tradingagents-research-desk), public. Team: **Alfa, Bravo, Charlie and Delta**, each assigned a relative contribution of **1.0**. Responsibilities and rotating review assignments are in [docs/process/team.md](docs/process/team.md). The report maps five requirement increments to the delivered workflows.

## Run locally

Use Python 3.12 and a project-local virtual environment:

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
.venv/bin/pip install --no-deps -e .
.venv/bin/research-desk --help
```

Set `RESEARCH_DESK_HOME` to a project-local directory for a separate paper account. The default teaching account contains USD 100000 cash. Purchases must keep the **total** single-stock holding within 10% of equity. Only whole shares are allowed, and sales cannot exceed owned shares. Prices come from evidence. This application places no real orders.

## Offline demonstration

The packages under `test/fixtures/packs` are deterministic offline fixtures for the evidence and paper-ledger workflows:

```sh
export RESEARCH_DESK_HOME="$PWD/demo-home"
mkdir -p "$RESEARCH_DESK_HOME/runs"
cp -R test/fixtures/packs/aapl_buy_complete "$RESEARCH_DESK_HOME/runs/fixture-aapl-buy"
.venv/bin/research-desk export fixture-aapl-buy --out evidence.zip
.venv/bin/research-desk replay evidence.zip --out replay-report --ledger
.venv/bin/research-desk propose fixture-aapl-buy --operator leo
```

Read the proposal identifier returned by `propose`. Run `review approve PROPOSAL_ID --shares 100 --operator leo`, then `execute PROPOSAL_ID --operator leo`. `ledger --report` shows state and history. Repeating `execute` returns the original transaction without changing balances again. A 101-share proposal against the USD 100 fixture price fails the 10% cap. Execution without approval also fails. Review and execution remain separate commands.

## Actual fixed-corpus research

Supply `DEEPSEEK_API_KEY` through the host environment, never a source file. `DEEPSEEK_BASE_URL` is optional. The configured application model is deepseek-flash, with the authorized endpoint https://api.aiohub.org/v1. The effective request body disables reasoning for both research and judgment. These commands incur real API usage:

```sh
.venv/bin/research-desk evaluate-case AAPL --mode baseline --out evaluation/live --max-calls 32
.venv/bin/research-desk evaluate-case AAPL --mode compact --out evaluation/live --max-calls 32
.venv/bin/research-desk judge-case AAPL --out evaluation/live
.venv/bin/research-desk aggregate evaluation/live
```

Run the same pair for MSFT, NVDA, AMZN, META and GOOGL. Source CSVs are under test/fixtures/market, and case facts/source identities are in src/research_desk/eval/case_registry.py. The original experiment reserved four cases after AAPL/MSFT development. The current revision uses all six as a fixed regression corpus. Save failed attempts separately before rerunning a directory, because the run command replaces that arm's output. The final released evidence is immutable and should be copied to a new output root for a new experiment.

Both arms use the same complete selected graph, model, frozen corpus and provider output cap. Runtime prompt version `research-desk-0.1.2` supplies the same evidence-grounding rules to every role in both modes; version snapshots are retained under `prompts/`. Compact requests concise role outputs and removes redundant non-evidence text. `judge-case` invokes an isolated evaluator role and logs its token usage separately from application runs, while `aggregate` computes summary metrics offline from saved provider metadata and judge outputs.

The current-source comparison completed all 12 runs, passed **60/60 mandatory-field checks**, and passed every semantic and quality threshold. Compact used **43.00% fewer application tokens**; its elapsed-time sum was **56.52% of baseline**. Complete evidence is in [evaluation/release](evaluation/release), with the failed transport attempt preserved under evaluation/revision-initial.

**Replay** rebuilds saved results without external calls. **Controlled rerun** regenerates research from fixed non-LLM inputs and remains stochastic. These modes answer different reproducibility questions.

For the complete matrix, use a fresh output directory:

```sh
.venv/bin/python scripts/evaluate_release.py --out evaluation/reproduction --workers 6
```

The runner executes both modes for all six cases, judges them, aggregates actual usage and validates quality against current source. The whole-input budget uses a 72,000-unit compaction trigger and a 96,000-unit hard cap. Provider usage supplies the reported token counts.

## Verification

```sh
.venv/bin/pytest -q test/offline
.venv/bin/pytest -q tests -m "not integration and not live and not smoke"
.venv/bin/pytest -q tests test/offline -m "not integration and not live and not smoke"
.venv/bin/mypy src/research_desk --follow-imports=skip --ignore-missing-imports --python-version 3.12
```

The current complete unit run passed **790 tests and 71 subtests**, with one optional-dependency skip and one live-test deselection. Structural, schema, approval and semantic checks also pass. Regression includes the preserved upstream tests and the extension unit suite. Full command records and the current cloud run are listed in [docs/ci-gates.md](docs/ci-gates.md). For the opt-in provider-dependent test entry, see [test/live/README.md](test/live/README.md); the complete paired experiment above is the release evidence.

The public repository has six required CI checks and enforced branch protection. Safety changes require an accepted ADR and code-owner review. One approving review is required before merge, including for administrators. The source branch and pull request carry the current implementation; server configuration and actual job results are saved under evaluation/github.

## Repository map

| Path | Purpose |
|---|---|
| src/research_desk | Application extension and fixed-corpus evaluation |
| tradingagents, cli, tests | Preserved upstream engine and regression tests |
| test/offline, test/fixtures | Extension acceptance tests and frozen evidence |
| docs/req | Machine-readable PRD, 24-requirement registry and schema |
| architecture-blueprint.md, docs/architecture | Component contracts, ADRs, invariants, state and permissions |
| AGENTS.md, Prompt.md, .opencode, .agent | Coding governance and effective role rules |
| docs/process, docs/review-memo.md, docs/bug-diary.md | Actual decisions, tests and interventions |
| transcripts | Full session exports, raw events and annotated prompts |
| evaluation | Saved live inputs, runs, judgments and comparison |
| Report.md, Report.pdf | Single process report and 12pt PDF rendering |

The source submission excludes virtual environments, credentials, caches and the separate 600-second demonstration video. Upstream attribution and the original license are retained. The original upstream README is preserved as [UPSTREAM_README.md](UPSTREAM_README.md).


## Prompt snapshots and release review

The course structure illustrates versioned prompt files as prompt_v1.0.yaml and prompt_v1.1.yaml. This project uses the established runtime-prompts-v0.1.0.yaml and runtime-prompts-v0.1.1.yaml names for those first two snapshots; runtime-prompts-v0.1.2.yaml is current. config.py owns the active prompt version.

The current source is in [PR #1](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/pull/1). The source revision’s [six required CI jobs passed](https://github.com/Fighterforever/cs5351-tradingagents-research-desk/actions/runs/42645314153). Branch protection keeps the PR blocked until an independent authorized reviewer approves it. The final roster and member-specific annotations are listed in [the delivery checklist](docs/process/delivery-checklist.md).
