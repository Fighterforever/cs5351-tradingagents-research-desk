# Evaluation logbook

2026-08-31: official TradingAgents v0.4.0 selected after reading graph, memory, price and report contracts. It is a newly released formal tag; the local baseline suite provides the actual tested evidence rather than a claim of long-term release maturity.

12:05:17.791955 UTC: leo approved plan1.0.0 and tests1.0.0. 12:06:32.695 UTC: first OpenCode implementation event. The original upstream run completed with649 passing tests,2 skips and71 subtests. The first extension run converged to47 passing tests after packaging, context and state-transition fixes.

The review then redirected implementation from cleanup toward full real-graph evaluation. Real public OHLCV inputs and official company release facts were frozen for AAPL, MSFT, NVDA, AMZN, META and GOOGL. Development cases are AAPL and MSFT; the remaining four are held out from tuning. Direct API executions and scores are recorded in final evaluation artifacts, not inferred from fixture tests.

The first live launch failed before any provider request because the supplied graph configuration omitted data_cache_dir. The next AAPL pilot completed15 model calls and27 tool calls but could not export a real message object; an overbroad credential filter also removed numeric token fields. Both artifacts remain in their own directories and do not contribute to final cost statistics.

The first complete development comparison is archived under evaluation/development-initial. Its two baseline runs used183143 tokens and305.710 summed seconds, versus117078 tokens and161.133 seconds in compact mode. Zero cited claims in both arms prevented quality acceptance despite36.07% fewer tokens. The source owner introduced common per-request grounding for both modes, corrected source-specific example leakage, and froze prompt0.1.1. The independent report input preserves roles; the mandatory-price check now inspects report text as well as evidence. The judge rubric, thresholds and fixed inputs are unchanged.

The separate max_calls1 MSFT demonstration completed exactly one request, recorded2273 tokens and2.011 seconds, and stopped before a second request. Its package is complete, its outcome is budget_stopped and it has no signal. This run is excluded from the paired cost comparison.

Final frozen application matrix: all12 runs completed. Provider usage was623270 baseline tokens versus338250 compact tokens, a45.73% reduction. Summed elapsed time was970.913 versus392.445 seconds. The uniform final judge used all actual tool-result observations: baseline mean support0.9167, compact0.9000, relevance1.0 in both arms, and counted-citation validity1.0. Mandatory checks passed59/60; META compact omitted the full legal company name. The original output remains unchanged and QUALITY-001 is explicitly not fully met.

All12 independent replay CLI processes exited successfully and retained their original signals, with maximum0.811354 seconds including startup and reported external calls0. The final unified local CI passed all six gates and all six rejection examples. Regression evidence records649 upstream passes,2 skips,71 subtests and98 application passes. GitHub server policy evidence is separate from these local results.

Release provenance correction: the initial local v0.4.0 ref was the release branch in a shallow checkout. The final release process fetched complete upstream ancestry and the actual signed v0.4.0 tag, then confirmed an identical source tree with the tested baseline. This changes ref provenance, not application or baseline code. The ambiguous local branch name is removed and docs/process/upstream-baseline.json preserves the exact comparison.
