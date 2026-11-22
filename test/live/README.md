# Live evaluation test

The live test runs one AAPL baseline case through the same `run_evaluate_case` function as the six-case experiment. It checks that the research completes and that the resulting evidence package contains a decision and provider-reported token counts.

## Run the test

Supply `DEEPSEEK_API_KEY` for the configured endpoint. The application defaults to `https://api.aiohub.org/v1`. Set `DEEPSEEK_BASE_URL` to select a different endpoint that serves the configured model.

```bash
RESEARCH_DESK_LIVE_TESTS=1 .venv/bin/pytest -q test/live/test_live_evaluation.py
```

The test skips when the opt-in flag or credential is absent. By default, pytest writes the outputs to its temporary directory. Set `RESEARCH_DESK_LIVE_OUT` to keep them in a new directory. The [project README](../../README.md#verification) gives the separate instructions for the upstream provider test.

## Six-case comparison

The [experiment commands](../../README.md#actual-fixed-corpus-research) run both arms for each ticker, judge each report and aggregate the results. The [recorded release results](../../evaluation/release/aggregate/report.md) cover all twelve runs.
