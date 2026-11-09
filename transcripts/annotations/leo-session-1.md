# Offline implementation

The first session established the offline application and its integration with the upstream research graph.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-01: Build the first working application

The initial implementation required a complete offline Research Desk package integrated with the upstream TradingAgents graph, evidence packs, policy ledger, budget controls, and documentation deliverables.

> Implement a clean integration seam with TradingAgentsGraph: normal live run should use its actual graph, selected analysts, researchers, managers, trader and risk debate.

Connecting directly to the real upstream graph and enforcing deterministic ledger policies established a valid baseline for reproducible offline replay and subsequent live comparisons.

OpenCode created the `src/research_desk` package, offline test suite, and initial architecture and requirements files. The session passed 47 offline extension tests and 696 combined tests with 71 subtests.

Result: [pyproject.toml](../../pyproject.toml), [graph_adapter.py](../../src/research_desk/graph_adapter.py), [evidence.py](../../src/research_desk/evidence.py), [policy.py](../../src/research_desk/policy.py), [test_integration_seam.py](../../test/offline/test_integration_seam.py).

Source: [project-01.full.json](../project-01.full.json), message `msg_057b6c6c3001AL4FZng9VdvW70`, JSON pointer `/messages/0`. Session: `ses_fa849396effeNN2dsVIpTIaax8`.

Prompt: [project-01-offline.md](../prompts/project-01-offline.md).
