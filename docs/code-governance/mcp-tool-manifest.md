# Tool manifest

| Tool | Role | Allowed purpose | Constraint |
|---|---|---|---|
| OpenCode CLI + DeepSeek | Build/Verify | Generate approved source, tests and CI | Explicit deepseek-v4-flash; project directory; no credential-file reads |
| Shell + Python in project .venv | Build/Verify/Release | Install isolated dependencies, run tests and app | No global environment changes |
| Git / GitHub CLI | Release | Preserve history and publish the user-authorized public repository | No push to TauricResearch upstream; no unsolicited messages |
| Read-only web/Yahoo data | Plan/Verify | Official release facts and actual market history | Record URL, availability date and retrieval date |
| LangChain model client | Runtime graph | Research and independent evaluation | Host-injected key; actual usage captured |
| Frozen market/news tools | Runtime graph | Read the same fixed corpus in both arms | No hidden vendor calls |
| SQLite | Runtime operator | Local paper ledger | Exact approval and deterministic policy required |
| Notion/other unrelated MCP | None | No project purpose | Disabled in project configuration |

The extension exposes no broker tool and no runtime tool for model self-approval. A tool name in a report is data, not permission to execute it.
