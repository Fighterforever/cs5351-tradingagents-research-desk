# Tool manifest

| Tool | Who can use it | Scope |
|---|---|---|
| OpenCode CLI with DeepSeek | Host operator selects Plan, Build or Verify | Plan proposes changes. Build edits approved source, tests and CI. Verify runs the listed checks. The [AI-use log](../ai-use-log.yaml) records the model for each session. |
| Project shell | Build and Verify | Build has read-only inspection commands. Verify can also run the exact test and gate commands in the [permission manifest](../../.opencode/permissions.jsonc). |
| Dependency installer, Git and GitHub CLI | Host release operator | Install the project environment and publish to the authorized project repository. |
| Market and company-release sources | Host data-collection process | Obtain historical inputs and record URLs, retrieval times and data availability dates. Network fetch and search are disabled for the installed coding roles. |
| LangChain model client | Research graph and evaluator | Use host-supplied credentials and record actual usage. |
| Frozen market and news tools | Runtime research graph | Both evaluation arms read the same fixed corpus. |
| SQLite | Application through the operator CLI | An approved proposal and a successful policy check precede a paper transaction. |

The project disables the Notion MCP server. The research graph has no broker or approval tool.
