# Annotated OpenCode session6: common per-role evidence grounding

Session: ses_fa80e5e8bffei1CBiJ8vadPRtm. Complete native export: project-09.full.json.gz. Original events: project-09.raw.jsonl and project-10.raw.jsonl. Prompts: prompts/project-09-grounding.md and prompts/project-10-grounding-precision.md. The gzip is lossless; decompress it to recover the exact full JSON. The native export exceeded GitHub's single-file size limit, so compression preserves content without broad redaction. An exact credential scan found no configured key in the export.

Intervention1 responded to the actual two-case citation failure. The coordinator required a shared grounding layer at every real LLM request, including bound tool and structured-output paths. Both modes receive identical source/fact instructions. Baseline history remains uncompressed, the actual upstream role graph remains intact, and the compact target stays600 tokens with the same provider cap.

Intervention2 required a plain delegate composed with real LangChain Runnables, replacing dynamic class mutation. Tests invoke the actual preprocessor paths with recording Runnables and preserve assistant/tool identifiers. The first fake bindings were not Runnable-compatible; the recorded failure led to correcting the test doubles against the real contract.

Intervention3 caught illustrative numeric facts and a hardcoded source ticker in the newly generated prompt. Those examples could contaminate another stock's analysis. The follow-up removed fabricated numeric examples, registered only sources that actually exist, and left unknown live facts unknown. The final response contract requests the real ticker, date and frozen close where available. An additional no-corpus/other-ticker test guards this concrete failure.

The session recorded72 passing offline tests before the final precision change, five focused passing checks afterward, and a clean type check across18 application files. The coordinator stopped repeated broader cleanup at that milestone. Runtime prompt0.1.1 is frozen for the restarted development evaluation; no test success is presented as proof of live research quality.
