# Function ownership and inherited trace links

Generated from the actual application AST at report preparation. Each function inherits its module’s owning decision and acceptance contract shown below. This index supplements the behavior-level architecture trace matrix; it does not claim that every function separately enforces every invariant. Nested closures belong to their enclosing function. Tests provide the behavior evidence.

## src/research_desk/budget.py

Owner: ADR-001. Requirement contract: NFR-003. Verification: AT-06.

`BudgetExhausted.__init__`, `BudgetTracker.can_start`, `BudgetTracker.start_call`, `BudgetTracker.record_usage`, `BudgetTracker.stop_reason`, `BudgetTracker.summary`, `BudgetTracker.merge`.

## src/research_desk/cli.py

Owner: ADR-001; ADR-002. Requirement contract: FR-001/002/003; INV-001/002. Verification: AT-01/03/04/07.

`_settings`, `_store`, `_default_operator`, `analyze`, `_print_run_result`, `export`, `replay`, `propose`, `review`, `execute`, `ledger`, `compare`, `_context_chars`, `evaluate_case`, `judge_case`, `aggregate`.

## src/research_desk/config.py

Owner: ADR-001; ADR-002. Requirement contract: INV-002; NFR-003. Verification: AT-04/06.

`ResearchDeskSettings.__post_init__`, `ResearchDeskSettings.home_path`, `ResearchDeskSettings.db_path`, `ResearchDeskSettings.runs_dir`, `ResearchDeskSettings.reports_dir`, `ResearchDeskSettings.ensure_dirs`, `ResearchDeskSettings.config_snapshot`.

## src/research_desk/context.py

Owner: ADR-001. Requirement contract: SEC-001; FR-003. Verification: AT-02/06/07.

`StandingConstraints.header_text`, `_extract_news_notes`, `market_source_id`, `build_common_grounding`, `dedup_repeated_blocks`, `bound_history`, `estimate_token_heuristic`, `ContextAssembler.__init__`, `ContextAssembler.assemble`, `ContextAssembler.assemble_from_entries`, `_join_parts`.

## src/research_desk/eval/case_registry.py

Owner: ADR-001. Requirement contract: FR-003; QUALITY-001/002/003; COST-001; PERF-001. Verification: AT-07.

`all_cases`, `case_for`, `development_cases`, `held_out_cases`, `load_market_manifest`.

## src/research_desk/eval/compact_delegate.py

Owner: ADR-001. Requirement contract: FR-003; QUALITY-001/002/003; COST-001; PERF-001. Verification: AT-07.

`_tuple_to_message`, `_to_messages`, `_content_of`, `_has_fact_marker`, `_rebuild`, `compact_transform`, `_measure_chars`, `delegate_transform`, `GroundingDelegate.__init__`, `GroundingDelegate._transform`, `GroundingDelegate.invoke`, `GroundingDelegate.bind_tools`, `GroundingDelegate.with_structured_output`, `wrap_for_mode`.

## src/research_desk/eval/frozen_provider.py

Owner: ADR-001. Requirement contract: FR-003; QUALITY-001/002/003; COST-001; PERF-001. Verification: AT-07.

`_market_source_label`, `_format_header`, `FrozenMarketProvider.__init__`, `FrozenMarketProvider._find_case`, `FrozenMarketProvider.get_stock_data`, `FrozenMarketProvider._rows_between`, `FrozenMarketProvider._to_upstream_csv`, `FrozenMarketProvider.get_indicators`, `FrozenMarketProvider._indicator`, `FrozenMarketProvider._macd_line`, `FrozenMarketProvider._unavailable_window`, `FrozenMarketProvider.get_verified_market_snapshot`, `FrozenMarketProvider._frame_as_of`, `FrozenMarketProvider.get_news`, `FrozenMarketProvider.get_global_news`, `FrozenMarketProvider.get_insider_transactions`, `FrozenMarketProvider.get_macro_indicators`, `FrozenMarketProvider.get_prediction_markets`, `_rsi`, `_atr`, `_vwma`.

## src/research_desk/eval/live.py

Owner: ADR-001. Requirement contract: FR-003; QUALITY-001/002/003; COST-001; PERF-001. Verification: AT-07.

`_graph_config`, `_desk_settings`, `_dump_json`, `run_evaluate_case`, `_replace_dir`, `_normalize_number_token`, `_contains_price`, `_report_text`, `_report_text._add`, `_deterministic_checks`, `_deterministic_checks.check`, `run_judge_case`, `_observed_tools_text`, `_judge_prompt`, `_valid_citation_rate`, `_llm_judge`, `_llm_judge._Judge._supported_within_cited`, `run_aggregate`, `_arm_value`, `_aggregate_report`, `_pct`.

## src/research_desk/evidence.py

Owner: ADR-001 and its evidence-format appendix. Requirement contract: SEC-001; FR-001. Verification: AT-01/02.

`_is_credential_key`, `sanitize_secrets`, `EvidenceLog.__init__`, `EvidenceLog.record`, `record_data_read`, `EvidenceRecorder.__init__`, `EvidenceRecorder._node_from_kwargs`, `EvidenceRecorder.on_chat_model_start`, `EvidenceRecorder.on_llm_start`, `EvidenceRecorder._start_llm`, `EvidenceRecorder._serialize_messages`, `EvidenceRecorder.on_llm_end`, `EvidenceRecorder.on_llm_error`, `EvidenceRecorder.on_tool_start`, `EvidenceRecorder.on_tool_end`, `EvidenceRecorder.on_tool_error`, `_msg_to_text`, `_safe_str`, `_extract_usage`, `_data_snapshot_from_events`, `build_pack`, `EvidencePackIO.export`, `EvidencePackIO.export_zip`, `EvidencePackIO._flatten`, `EvidencePackIO.import_pack`, `EvidencePackIO._load_dir`, `EvidencePackIO.load_external_proposal`.

## src/research_desk/graph_adapter.py

Owner: ADR-001. Requirement contract: SEC-001; NFR-003; QUALITY-001/002/003. Verification: AT-01/02/06/07.

`_provider_tools`, `_provider_tools.get_stock_data`, `_provider_tools.get_indicators`, `_provider_tools.get_verified_market_snapshot`, `_provider_tools.get_news`, `_provider_tools.get_global_news`, `_provider_tools.get_insider_transactions`, `_provider_tools.get_macro_indicators`, `_provider_tools.get_prediction_markets`, `EvidenceTradingGraph.__init__`, `EvidenceTradingGraph._create_tool_nodes`, `EvidenceTradingGraph.resolve_instrument_context`, `EvidenceTradingGraph._fetch_returns`, `_available_sources_from_provider`, `_parse_stock_data_price`, `_parse_verified_snapshot_price`, `price_from_evidence`, `merge_trace`, `decide_proposal`, `ResearchRunner.__init__`, `ResearchRunner._memory_entries`, `ResearchRunner._assemble_context`, `ResearchRunner._build_graph`, `ResearchRunner._price_from_provider`, `ResearchRunner.run`, `ResearchRunner._data_snapshot_from_run`, `ResearchRunner._available_sources`, `_trim_state`.

## src/research_desk/models.py

Owner: ADR-001; ADR-002. Requirement contract: FR-001/002; INV-001/002. Verification: AT-01/03/05.

`UsageSummary.add`, `EvidencePack._final_state_serializable`, `ProposalRecord._shares_positive_int`, `LedgerState.equity`, `utcnow_iso`, `make_proposal_version`.

## src/research_desk/policy.py

Owner: ADR-002. Requirement contract: INV-002. Verification: AT-04/05.

`_owned_shares`, `_revalue_equity`, `PolicyViolation.__init__`, `evaluate_buy`, `evaluate_buy.check`, `evaluate_sell`, `evaluate_sell.check`, `raise_for_violations`, `reject_reasons`, `policy_bounds`.

## src/research_desk/replay.py

Owner: ADR-001. Requirement contract: FR-001; NFR-001. Verification: AT-01.

`ReplayEngine.__init__`, `ReplayEngine.load`, `ReplayEngine.replay`.

## src/research_desk/report.py

Owner: ADR-001. Requirement contract: FR-001; QUALITY-001. Verification: AT-01/07.

`render_run_report`, `render_proposal_report`, `render_ledger_report`, `render_compare_report`, `render_compare_report.row`, `_delta`.

## src/research_desk/review.py

Owner: ADR-002. Requirement contract: INV-001/002. Verification: AT-03/04/05.

`_side_for_signal`, `_proposal_content_version`, `create_proposal`, `approve`, `reject`, `execute`, `_execute_sell`, `evaluate_proposal_legibility`, `now_iso`.

## src/research_desk/storage.py

Owner: ADR-002. Requirement contract: INV-001/002. Verification: AT-03/05.

`ResearchDeskStore.__init__`, `ResearchDeskStore._migrate`, `ResearchDeskStore.get_ledger`, `ResearchDeskStore.apply_transaction`, `ResearchDeskStore.list_transactions`, `ResearchDeskStore.save_proposal`, `ResearchDeskStore.get_proposal`, `ResearchDeskStore.list_proposals`, `ResearchDeskStore.update_proposal_status`, `ResearchDeskStore._row_to_proposal`, `ResearchDeskStore.close`, `_json_default`, `write_json`, `read_json`.
