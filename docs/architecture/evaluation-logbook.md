# Evaluation logbook

2026-08-31: official TradingAgents v0.4.0 selected after reading graph, memory, price and report contracts. It is a newly released formal tag; the local baseline suite provides the actual tested evidence rather than a claim of long-term release maturity.

At 12:05:17.791955 UTC, the coordinating workflow recorded approval of plan 1.0.0 and tests 1.0.0 under the scope delegated by Liyu MA. The first OpenCode implementation event followed at 12:06:32.695 UTC. The original upstream run completed with 649 passing tests, 2 skips and 71 subtests. The first extension run converged to 47 passing tests after packaging, context and state-transition fixes.

The review then redirected implementation from cleanup toward full real-graph evaluation. Real public OHLCV inputs and official company release facts were frozen for AAPL, MSFT, NVDA, AMZN, META and GOOGL. Development cases are AAPL and MSFT; the remaining four are held out from tuning. Direct API executions and scores are recorded in final evaluation artifacts, not inferred from fixture tests.

The first live launch failed before any provider request because the supplied graph configuration omitted data_cache_dir. The next AAPL pilot completed 15 model calls and 27 tool calls but could not export a real message object; an overbroad credential filter also removed numeric token fields. Both artifacts remain in their own directories and do not contribute to final cost statistics.

The first complete development comparison is archived under evaluation/development-initial. Its two baseline runs used 183,143 tokens and 305.710 summed seconds, versus 117,078 tokens and 161.133 seconds in compact mode. Zero cited claims in both arms prevented quality acceptance despite 36.07% fewer tokens. The source owner introduced common per-request grounding for both modes, corrected source-specific example leakage, and froze prompt 0.1.1. The independent report input preserves roles; the mandatory-price check now inspects report text as well as evidence. The judge rubric, thresholds and fixed inputs are unchanged.

The separate `max_calls=1` MSFT demonstration completed exactly one request, recorded 2,273 tokens and 2.011 seconds, and stopped before a second request. Its package is complete, its outcome is budget_stopped and it has no signal. This run is excluded from the paired cost comparison.

First complete frozen application matrix: all 12 runs completed. Provider usage was 623,270 baseline tokens versus 338,250 compact tokens, a 45.73% reduction. Summed elapsed time was 970.913 versus 392.445 seconds. The uniform final judge used all actual tool-result observations: baseline mean support 0.9167, compact 0.9000, relevance 1.0 in both arms, and counted-citation validity 1.0. Mandatory checks passed 59/60; META compact omitted the full legal company name. The original output remains unchanged and QUALITY-001 is explicitly not fully met.

All 12 independent replay CLI processes exited successfully and retained their original signals, with maximum 0.811354 seconds including startup and reported external calls 0. The final unified local CI passed all six gates and all six rejection examples. Regression evidence records 649 upstream passes, 2 skips, 71 subtests and 98 application passes. GitHub server policy evidence is separate from these local results.

Release provenance correction: the initial local v0.4.0 ref was the release branch in a shallow checkout. The final release process fetched complete upstream ancestry and the actual signed v0.4.0 tag, then confirmed an identical source tree with the tested baseline. This changes ref provenance, not application or baseline code. The ambiguous local branch name is removed and docs/process/upstream-baseline.json preserves the exact comparison.


Current release revision: all twelve corrected research runs completed and all twelve judgments passed. Mandatory fields passed 60/60. Compact reduced application tokens by 43.00%, with an elapsed-time ratio of 0.5652. Support increased from 0.9000 to 0.9083 and relevance stayed at 0.95. The failed transport matrix is preserved separately in evaluation/revision-initial.

All twelve CLI replays for ADR-004 preserved their original signal, reported zero external calls and completed within 0.9119 seconds. The coding-context comparison used the same maintenance task and 26 unit cases in both conditions; focused input reduced total observed coding tokens by 60.74%. Native session counters and prompt variants are retained. Public GitHub required checks and branch protection are active.

## Submission repair

The original release supplied the evidence for ADR-005. Nine tradeable research proposals had no evidence identifier. Reviewing the registration and replay entry points also exposed lost terminal state and a missing CLI error signal. The repair introduced a separate registration operation and bound the proposal to the captured inputs. The gate now validates complete pairs and includes the upstream graph in the source record. [ADR-005](adr/005-submission-contracts.md) records the design and acceptance cases.

The [ADR-005 experiment](../../evaluation/submission-release/aggregate/release-gate.json) passed all twelve individual assessments and 60 field checks. Research used 600,576 baseline and 345,309 compact tokens. All eleven proposals carry the identifier of their saved input material. GOOGL changed from Hold to Overweight in the compact run.
