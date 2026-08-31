# ADR-001: Extend the existing graph through application-owned seams

Status: accepted by leo, 2026-08-31. Requirements: FR-001 through FR-003, INV-001, INV-002. The concrete plan and tests were approved at 12:05:17.791955 UTC before OpenCode's first implementation event at 12:06:32.695 UTC.

## Context and alternatives

TradingAgents v0.4.0 already provides multi-agent research, structured decisions, date-aware memory, checkpointing and price validation. The missing product workflow is portable evidence followed by explicit approval and paper execution. A complete graph rewrite would discard tested domain behavior and make the optimization baseline incomparable. Editing every upstream prompt and tool would distribute application-specific policy across many owners. A narrow application extension keeps the experimental boundary visible.

Candidate A modifies the entire graph and shared vendors. Candidate B subclasses/composes the existing graph and implements policy outside it. Candidate C builds a small new agent demo. The evaluation table selects B because it preserves genuine AI integration while keeping deterministic authority isolated. The original graph's full selected role sequence is retained in both experimental arms.

## Context layers and assembly

Layer1 identifies the instrument and analysis cutoff. Layer2 states standing constraints: use available evidence, retain source identity, distinguish unknown facts and keep execution advisory. Layer3 supplies frozen market/history/news knowledge. Layer4 holds current discussion and retrieved past context. Layer5 preserves resumable structured state. Layer6 gives the current agent task and expected output.

The assembly order is eligibility filtering, duplicate removal in compact mode, prioritization, budget accounting, compaction and final constraint reinjection. Baseline preserves original substantive prompt input. Compact can remove repeated paragraphs or shorten older discussion, while retaining symbol, date, price evidence, source IDs and current task. It also requests concise role output to reduce repeated prose passed to later agents. Fresh six-case runs have little past memory, so compact must apply to actual per-agent messages; changing only a memory string would leave the dominant token cost unchanged.

The call budget is configured for the experiment. Per-call maximum output bounds use the provider's existing max_tokens contract. Character estimates may guide context assembly but never replace provider-reported token usage. The model adapter checks before starting a request; a structured-output retry cannot create an extra request after the budget is exhausted. Critical constraints are re-injected after compaction. Factual quality is evaluated independently of brevity.

## Consequences and reopening conditions

Evidence packs contain prompts and responses and are larger than ordinary reports. Replay is fast because it reconstructs captured state; controlled reruns call the model and remain stochastic. The frozen provider must answer valid parameter variations from data, because an exact tool-transcript lookup would bias the comparison when compact changes tool arguments.

The approval boundary stays outside all model tools. The extension retains responsibility for current-ledger checks even if upstream research changes. Reopen this ADR if an upstream public interface cannot expose a material external read, if multiuser concurrency is added, or if compact cannot satisfy factual constraints without discarding agent roles. No such need justifies silently replacing the baseline.

## Affected paths

The accepted application scope includes `src/research_desk/config.py`, `graph_adapter.py`, `budget.py`, `evidence.py`, `context.py`, `models.py`, `replay.py`, `report.py`, `cli.py` and the application-owned `src/research_desk/eval/` adapters. `pyproject.toml` exposes the installed extension. These paths implement the already approved evidence, research-context and runtime-budget boundaries. The deterministic approval and ledger changes are specified more precisely in ADR-002. No upstream vendor implementation is replaced.
