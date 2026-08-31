# Annotated OpenCode session 5: preserving real messages and provider usage

Session: ses_fa817dbb4ffescaq14SFvAqA2I. Full native record: project-evidence-fix.full.json. Original events: project-evidence-fix.raw.jsonl. Prompt: prompts/project-evidence-fix.md. This was a separate bounded OpenCode session owned by the coordinating workflow.

The intervention followed a real completed AAPL pilot whose export failed on a LangChain HumanMessage. At the same time, inspection found that an overbroad secret filter had removed numeric input_tokens/output_tokens. The completed report survived, but the missing measurements were not reconstructed or used in the cost comparison.

The prompt limited the repair to evidence.py and a real-message roundtrip regression. OpenCode serializes actual message structures and distinguishes credential fields from usage counters. The new regression passes real HumanMessage, AIMessage and ToolMessage objects through directory and ZIP exports, then replays with sockets blocked. An initial assertion incorrectly treated the declared CallRecord model as a dictionary; the saved session retains the failure and correction to its declared fields.

Verification recorded two new roundtrip passes and eight existing replay passes. The later development packs contain real numeric usage and complete terminal state. This is evidence of a repaired boundary, while the original incomplete pilot remains preserved.

