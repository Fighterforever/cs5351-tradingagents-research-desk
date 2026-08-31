# Annotated OpenCode sessions: leo

Participant and evaluation identifier: leo. All timestamps are UTC. Full original event streams and native full exports are preserved. An exact local credential scan redacts secrets only; the separate --sanitize exports are convenience files and redact message text broadly, so they are not the full transcript. The annotations describe actual interventions; they are not substituted conversation messages.

## Session1: offline vertical slice

Session: ses_fa849396effeNN2dsVIpTIaax8. Full raw record: project-01.raw.jsonl. Full native export: project-01.full.json. Sanitized convenience export: project-01.export.json. Launch prompt: prompts/project-01-offline.md.

The concrete plan and AT-01 through AT-08 were approved at2026-08-31T12:05:17.791955+00:00. The first implementation event is2026-08-31T12:06:32.695+00:00, obtained from the raw event timestamp. This ordering is checked by the approval gate.

OpenCode read the upstream contracts and generated the application modules, fixtures and tests. The record includes the real failing test rounds and corrections. At the useful offline milestone,47 extension tests passed. The separately executed unmodified upstream suite recorded649 passing tests,2 skips and71 subtests.

Intervention1: require the real upstream graph and application-owned seams rather than a replacement demonstration. Rationale: preserve existing system behavior and make the baseline comparison meaningful.

Intervention2: review package installation and the CLI vertical slice after generation. The first package import failure exposed missing src-layout discovery. Rationale: an application module is not delivered until its installed entry point works.

Intervention3: after the passing offline slice, inspect policy and approval semantics. The review identified a ticket-only cap, excluded valid sells and approval content that omitted quantity/evidence binding. ADR-002 records the required correction. Rationale: passing examples on an empty portfolio do not establish the total-holdings invariant.

Intervention4: terminate the session after its useful milestone when it continued cleanup and lint work. Source changes and raw output were retained. Rationale: the next unresolved acceptance item was real research/evaluation; a fresh focused session reduced repeated context cost.

## Session2: real fixed-corpus research and review corrections

Session: ses_fa83026e7ffe84kFIOlxvQB3aB. Launch prompt: prompts/project-02-live.md. Full native export: project-02.full.json. Raw event stream: project-02.raw.jsonl.

The follow-up named the exact business corrections and required a frozen-data provider backed by actual CSVs. It also explained why exact recorded tool-argument lookup could bias the experiment and why compaction of empty past memory would not address the main workload. The implementation must retain the complete selected upstream graph and actual DeepSeek requests.

The coordinator prepared six public-source cases before final comparison. AAPL and MSFT are development cases. NVDA, AMZN, META and GOOGL are held out. The live model key is injected by host execution and is never read by OpenCode or written into a session file. Failures and retries remain part of the evidence.

## Session3: real graph integration and experimental contracts

Session: ses_fa825e6e8fferDOiutg4e8ECO8. Full native record: project-04.full.json. Original events: project-04.raw.jsonl through project-08.raw.jsonl. These are five turns of one actual session, not five conversations. Prompts: prompts/project-04-ready-live.md through prompts/project-08-live-test.md (the exact available filenames are retained in the directory).

Intervention1 required preserving AIMessage.tool_calls and ToolMessage.tool_call_id at the actual model boundary. A text-only substitute would break upstream tool rounds even if a string compaction test passed. The correction used the existing LangChain message contracts and exercised the integration seam.

Intervention2 followed a real pre-request KeyError:data_cache_dir. The supplied configuration had been treated as a partial override, but TradingAgentsGraph expects a complete configuration. The supervisor directed a deep copy of DEFAULT_CONFIG and local cache/result/memory paths. A real construction test confirmed the missing-key fix without a provider request.

Intervention3 separated complete available frozen evidence from tools actually called. The judge must see the same available source corpus used in the run, including market history and technical observations. The source identity fallback was also removed so a fixed-corpus experiment could not quietly fetch a different company identity online.

Intervention4 corrected legitimate sales after a price gain. The 10% limit applies to resulting holdings after a buy. Selling ten shares from an overweight position must be allowed when shares are owned, even if the remaining position is still over the buy cap. The final turn added the opt-in live test entry and archived runtime prompts; the source changes then paused for actual development runs. The session recorded66 passing offline tests and a clean application type check before the separate evidence roundtrip tests were added.

## Session4: six CI gates and meaningful rejection examples

Session: ses_fa82cafc9ffeeAkOozPwPQ41De. Full native record: project-ci.full.json. Raw event stream and exact prompts are retained alongside it. Scope was scripts/, the Research Desk workflow and requirement schema; the session did not own application source.

Intervention1 rejected a proposed gate that treated a git-diff failure as an empty changed-file set. A failed comparison cannot establish that no review is needed. The corrected check preserves a concrete failure.

Intervention2 required approval to correspond to changed tests and explicit safety paths. An old ADR mentioning a module cannot authorize arbitrary future edits. The implemented gate checks the actual changed documents and approval chronology rather than accepting a generic APPROVED marker.

Intervention3 bound the semantic check to the actual case_registry and compact_transform interfaces. The six fixed cases and captured packages supply its inputs. It recomputes deterministic contracts and does not fabricate fresh LLM judge scores in offline CI.

Intervention4 requested isolated negative examples for all six gates. The harness alters temporary copies and captures expected refusal, avoiding contamination of the real tests or research data. The final local and remote check status is documented separately in docs/ci-gates.md; the transcript proves implementation and review, not an unrun server result.

## Session5: preserving real messages and provider usage

Session: ses_fa817dbb4ffescaq14SFvAqA2I. Full native record: project-evidence-fix.full.json. Original events: project-evidence-fix.raw.jsonl. Prompt: prompts/project-evidence-fix.md. This was a separate bounded OpenCode session owned by the coordinating workflow.

The intervention followed a real completed AAPL pilot whose export failed on a LangChain HumanMessage. At the same time, inspection found that an overbroad secret filter had removed numeric input_tokens/output_tokens. The completed report survived, but the missing measurements were not reconstructed or used in the cost comparison.

The prompt limited the repair to evidence.py and a real-message roundtrip regression. OpenCode serializes actual message structures and distinguishes credential fields from usage counters. The new regression passes real HumanMessage, AIMessage and ToolMessage objects through directory and ZIP exports, then replays with sockets blocked. An initial assertion incorrectly treated the declared CallRecord model as a dictionary; the saved session retains the failure and correction to its declared fields.

Verification recorded two new roundtrip passes and eight existing replay passes. The later development packs contain real numeric usage and complete terminal state. This is evidence of a repaired boundary, while the original incomplete pilot remains preserved.

## Transcript integrity and counting

These five numbered sections refer to five distinct native OpenCode session identifiers. Later grounding and permission sessions are retained as additional evidence. A large native export must be redirected to a regular file; a captured pipe produced a65KB truncated JSON file during preparation. The final full exports were parsed successfully and scanned for the exact configured credential. Only any actual credential value is redacted. Optional --sanitize exports redact message text and are clearly separated from complete course evidence.

## Session6: common per-role evidence grounding

Session: ses_fa80e5e8bffei1CBiJ8vadPRtm. Complete native export: project-09.full.json.gz. Original events: project-09.raw.jsonl and project-10.raw.jsonl. Prompts: prompts/project-09-grounding.md and prompts/project-10-grounding-precision.md. The gzip is lossless; decompress it to recover the exact full JSON. The native export exceeded GitHub's single-file size limit, so compression preserves content without broad redaction. An exact credential scan found no configured key in the export.

Intervention1 responded to the actual two-case citation failure. The coordinator required a shared grounding layer at every real LLM request, including bound tool and structured-output paths. Both modes receive identical source/fact instructions. Baseline history remains uncompressed, the actual upstream role graph remains intact, and the compact target stays600 tokens with the same provider cap.

Intervention2 required a plain delegate composed with real LangChain Runnables, replacing dynamic class mutation. Tests invoke the actual preprocessor paths with recording Runnables and preserve assistant/tool identifiers. The first fake bindings were not Runnable-compatible; the recorded failure led to correcting the test doubles against the real contract.

Intervention3 caught illustrative numeric facts and a hardcoded source ticker in the newly generated prompt. Those examples could contaminate another stock's analysis. The follow-up removed fabricated numeric examples, registered only sources that actually exist, and left unknown live facts unknown. The final response contract requests the real ticker, date and frozen close where available. An additional no-corpus/other-ticker test guards this concrete failure.

The session recorded72 passing offline tests before the final precision change, five focused passing checks afterward, and a clean type check across18 application files. The coordinator stopped repeated broader cleanup at that milestone. Runtime prompt0.1.1 is frozen for the restarted development evaluation; no test success is presented as proof of live research quality.
