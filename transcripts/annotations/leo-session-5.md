# Message serialization and usage capture

A completed pilot exposed an export failure and missing token counters. This session repaired the evidence boundary.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-14: Preserve messages and token counts

A live AAPL pilot completed 15 model calls and 27 tool calls but failed during evidence export on nested `HumanMessage` objects, while `sanitize_secrets` redacted numeric token usage fields matching the substring `token`.

> Convert actual Pydantic BaseModel values (including LangChain HumanMessage, AIMessage and ToolMessage) to JSON-native structured dictionaries using their supported model_dump(mode='json') API, then recursively sanitize.

Dumping Pydantic message models to structured JSON and restricting redaction to explicit credential key patterns preserved full message state and token accounting across directory and ZIP exports.

OpenCode updated `sanitize_secrets` in `src/research_desk/evidence.py` and added parameterized directory and ZIP roundtrip replay tests in `test/offline/test_evidence_message_roundtrip.py`. Verification passed all 10 tests across the new regression and `test_at01_replay.py`.

Result: [evidence.py](../../src/research_desk/evidence.py), [test_evidence_message_roundtrip.py](../../test/offline/test_evidence_message_roundtrip.py).

Source: [project-evidence-fix.full.json](../project-evidence-fix.full.json), message `msg_057e8247e001TQpLNGBYcerJBS`, JSON pointer `/messages/0`. Session: `ses_fa817dbb4ffescaq14SFvAqA2I`.

Prompt: [project-evidence-fix.md](../prompts/project-evidence-fix.md).
