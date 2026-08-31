# TradingAgents Research Desk

Research Desk extends **TradingAgents v0.4.0** with portable research evidence, zero-network replay, an explicitly approved paper ledger and a measured baseline/compact context experiment. The real upstream market/news, research, trader, risk and portfolio graph remains the research engine. The language model advises; deterministic application code controls paper execution.

Private course repository: [Fighterforever/cs5351-tradingagents-research-desk](https://github.com/Fighterforever/cs5351-tradingagents-research-desk). Participant and evaluation identifier: **leo**. Relative contribution: **1.0**. See the provenance statement in [Report.md](Report.md) and the actual [session records](transcripts/leo-leo.md).

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

The committed packages under test/fixtures/packs are labeled deterministic fixtures, not live model runs. For a clean example:

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

Supply `DEEPSEEK_API_KEY` through the host environment, never a source file. `DEEPSEEK_BASE_URL` is optional. The configured application model is deepseek-v4-flash. These commands incur real API usage:

```sh
.venv/bin/research-desk evaluate-case AAPL --mode baseline --out evaluation/live --max-calls 32
.venv/bin/research-desk evaluate-case AAPL --mode compact --out evaluation/live --max-calls 32
.venv/bin/research-desk judge-case AAPL --out evaluation/live
.venv/bin/research-desk aggregate evaluation/live
```

Run the same pair for MSFT, NVDA, AMZN, META and GOOGL. Source CSVs are under test/fixtures/market, and case facts/source identities are in src/research_desk/eval/case_registry.py. AAPL/MSFT are development cases; the other four were held out before final tuning. Save failed attempts separately before rerunning a directory, because the run command replaces that arm's output. The final released evidence is immutable and should be copied to a new output root for a new experiment.

Both arms use the same complete selected graph, model, frozen corpus and provider output cap. Runtime prompt version `research-desk-0.1.1` supplies the same evidence-grounding rules to every role in both modes; version snapshots are retained under `prompts/`. Compact requests concise role outputs and removes redundant non-evidence text. `judge-case` uses a separate evaluator role and records its usage outside application totals. `aggregate` reads saved files and makes no provider request. API usage and quality are actual results, not values inferred from output length.

**Replay** rebuilds saved results without external calls. **Controlled rerun** regenerates research from fixed non-LLM inputs and remains stochastic. These modes answer different reproducibility questions.

## Verification

```sh
.venv/bin/pytest -q test/offline
.venv/bin/pytest -q tests
.venv/bin/pytest -q tests test/offline
.venv/bin/mypy src/research_desk --follow-imports=skip --ignore-missing-imports --python-version 3.12
```

The unchanged upstream baseline recorded 649 passed, 2 skipped and 71 subtests. The extension's initial slice recorded 47 passing tests. After the shared grounding repair, the recorded offline run passed 72 tests; the final focused prompt correction passed all five grounding checks. Final test and live results are reported from their saved logs in Report.md. Tests that call real providers are separate from offline CI and require explicit environment credentials.

The CI workflow implements six checks: prior test approval, static/dependency/safety checks, requirement schema, fixed semantic replay, all prior regressions, and an updated AI-use log for source/prompt changes. [docs/ci-gates.md](docs/ci-gates.md) describes exact commands and negative examples. Private GitHub branch protection is a separate server setting; the final release records the actual API/check outcome and does not equate local passing tests with remote enforcement.

## Repository map

| Path | Purpose |
|---|---|
| src/research_desk | Application extension and fixed-corpus evaluation |
| tradingagents, cli, tests | Preserved upstream engine and regression tests |
| test/offline, test/fixtures | Extension acceptance tests and frozen evidence |
| docs/req | Machine-readable PRD, 23-requirement registry and schema |
| architecture-blueprint.md, docs/architecture | Component contracts, ADRs, invariants, state and permissions |
| AGENTS.md, Prompt.md, .opencode, .agent | Coding governance and effective role rules |
| docs/process, docs/review-memo.md, docs/bug-diary.md | Actual decisions, tests and interventions |
| transcripts | Full session exports, raw events and annotated prompts |
| evaluation | Saved live inputs, runs, judgments and comparison |
| Report.md, Report.pdf | Single process report and 12pt PDF rendering |

The source submission excludes virtual environments, credentials, caches and the separate 600-second demonstration video. Upstream attribution and the original license are retained. The original upstream README is preserved as [UPSTREAM_README.md](UPSTREAM_README.md).
