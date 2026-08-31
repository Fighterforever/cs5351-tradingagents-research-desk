# Annotated OpenCode session 3: real graph integration and experimental contracts

Session: ses_fa825e6e8fferDOiutg4e8ECO8. Full native record: project-04.full.json. Original events: project-04.raw.jsonl through project-08.raw.jsonl. These are five turns of one actual session, not five conversations. Prompts: prompts/project-04-ready-live.md through prompts/project-08-live-test.md (the exact available filenames are retained in the directory).

Intervention1 required preserving AIMessage.tool_calls and ToolMessage.tool_call_id at the actual model boundary. A text-only substitute would break upstream tool rounds even if a string compaction test passed. The correction used the existing LangChain message contracts and exercised the integration seam.

Intervention2 followed a real pre-request KeyError:data_cache_dir. The supplied configuration had been treated as a partial override, but TradingAgentsGraph expects a complete configuration. The supervisor directed a deep copy of DEFAULT_CONFIG and local cache/result/memory paths. A real construction test confirmed the missing-key fix without a provider request.

Intervention3 separated complete available frozen evidence from tools actually called. The judge must see the same available source corpus used in the run, including market history and technical observations. The source identity fallback was also removed so a fixed-corpus experiment could not quietly fetch a different company identity online.

Intervention4 corrected legitimate sales after a price gain. The 10% limit applies to resulting holdings after a buy. Selling ten shares from an overweight position must be allowed when shares are owned, even if the remaining position is still over the buy cap. The final turn added the opt-in live test entry and archived runtime prompts; the source changes then paused for actual development runs. The session recorded66 passing offline tests and a clean application type check before the separate evidence roundtrip tests were added.

