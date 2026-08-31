# Live opt-in evaluation tests (`test/live/`)

These are **live** integration tests: they drive the real `run_evaluate_case`
entry point (the same code the six-case baseline/compact matrix uses) against
real DeepSeek clients. They are **skipped by default** so the offline suite
never touches the network or credentials.

## Opt-in

Run the single live test with host-injected credentials:

```bash
export RESEARCH_DESK_LIVE_TESTS=1
# export DEEPSEEK_API_KEY=<host-supplied>     # required credential
# export DEEPSEEK_BASE_URL=<optional gateway>
.venv/bin/pytest -q test/live/test_live_evaluation.py
```

Default (no opt-in) skips cleanly:

```bash
.venv/bin/pytest -q test/live
```

Expected: the test is collected and skipped (`1 skipped`) with no API call.

## Credential environment names

| Env var | Required | Meaning |
|---|---|---|
| `RESEARCH_DESK_LIVE_TESTS` | yes | `=1` enables the live test; otherwise skip |
| `DEEPSEEK_API_KEY` | yes | DeepSeek provider credential (host-injected) |
| `DEEPSEEK_BASE_URL` | no | Optional DeepSeek gateway/base URL |
| `RESEARCH_DESK_LIVE_OUT` | no | Explicit output dir; default is a pytest `tmp_path` |

## Output isolation

By default the test writes to an isolated pytest `tmp_path` and never touches
`evaluation/final`. If you must use a stable directory, set
`RESEARCH_DESK_LIVE_OUT` explicitly; the coordinator's real six-case experiment
output is never overwritten by this test.

## Relation to the six-case CLI matrix

This test is a thin single-case smoke of the exact entry point the matrix uses.
The real comparison is run separately by the coordinator/root as:

```bash
# per case (6 tickers) × mode (baseline|compact) = 12 evaluate-case runs
.venv/bin/research-desk evaluate-case AAPL --mode baseline --out evaluation/pilot --max-calls 32
.venv/bin/research-desk evaluate-case AAPL --mode compact  --out evaluation/pilot --max-calls 32
# ... NVDA, AMZN, META, GOOGL, MSFT ...

# independent judge per case
.venv/bin/research-desk judge-case AAPL --out evaluation/pilot

# offline aggregate of the six paired metrics
.venv/bin/research-desk aggregate evaluation/pilot
```

This `test/live/` file exercises only the application entry point; it does not
replace, duplicate, or mock the six-case experiment.
