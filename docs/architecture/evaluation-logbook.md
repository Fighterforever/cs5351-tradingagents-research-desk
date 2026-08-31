# Evaluation logbook

2026-08-31: official TradingAgents v0.4.0 selected after reading graph, memory, price and report contracts. It is a newly released formal tag; the local baseline suite provides the actual tested evidence rather than a claim of long-term release maturity.

12:05:17.791955 UTC: leo approved plan1.0.0 and tests1.0.0. 12:06:32.695 UTC: first OpenCode implementation event. The original upstream run completed with649 passing tests,2 skips and71 subtests. The first extension run converged to47 passing tests after packaging, context and state-transition fixes.

The review then redirected implementation from cleanup toward full real-graph evaluation. Real public OHLCV inputs and official company release facts were frozen for AAPL, MSFT, NVDA, AMZN, META and GOOGL. Development cases are AAPL and MSFT; the remaining four are held out from tuning. Direct API executions and scores are recorded in final evaluation artifacts, not inferred from fixture tests.
