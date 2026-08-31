# Actual first live launch failure: fix the config owner and stop

The coordinator launched the real command with host-injected credentials:
`.venv/bin/research-desk evaluate-case AAPL --mode baseline --out evaluation/pilot --max-calls 32`
It failed before any API request with KeyError: 'data_cache_dir'. Actual log is ../orchestration/sessions/project-live-pilot-aapl.log. In TradingAgentsGraph.__init__ line105, config["data_cache_dir"] is required. eval/live.py::_graph_config provides only overrides but upstream treats the supplied dict as complete.

Fix this actual root cause: construct the evaluation config from a deep copy of the actual DEFAULT_CONFIG, then override the explicit model/settings. Ensure data_cache_dir, results_dir and decision-memory paths are inside the arm's isolated home (check actual declarations, do not invent field names). Keep both arms' effective settings identical. Preserve existing supplied backend URL and extra_body. Do not alter upstream code. This is within approved AT07 integration, not new scope.

Confirm constructing the actual graph with this config succeeds using a fake non-secret API token without making a provider request. Run only the directly related smoke check, then STOP immediately and provide readiness. The59 passing tests and CLI help are already established; no more aggregate synthetic datasets, cleanup or broad doc generation now. The coordinator will retry the actual API launch as soon as the config is fixed.
