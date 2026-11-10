# Report measurement and complete observations

Four prompts improved report assembly and retained complete tool observations for evaluation.

[Participant and evidence index](../59072966-Liyu-MA.md). Entry numbers identify recorded prompts. Test counts below describe the corresponding development turn.

## I-17: Define report and price checks

Initial development evaluations revealed that `_report_text` concatenated agent outputs without role headings, duplicated identical risk and portfolio decisions, and checked `frozen_price_used` only against input evidence.

> Preserve authentic role/stage titles for market/news/social/fundamentals, research manager, trader proposal, risk manager and final portfolio decision. Keep all actual opinions and original content.

Labeling each agent stage, deduplicating only byte-identical terminal decisions, and verifying that the frozen close price appears in the generated report text prevented false judge conflicts and unverified price passes.

In this turn, OpenCode inspected `src/research_desk/eval/live.py`, upstream reporting conventions, and fixture structures to prepare the implementation completed in the next turn.

Result: [live.py](../../src/research_desk/eval/live.py), [test_evaluation_report_checks.py](../../test/offline/test_evaluation_report_checks.py).

Source: [project-report-check.full.json.gz](../project-report-check.full.json.gz), message `msg_057f4ebfa001mul7ZW3hDp6REI`, JSON pointer `/messages/0`. Session: `ses_fa80b1435ffeLfgOoIjVIDIpKP`.

Prompt: [project-report-check-fix.md](../prompts/project-report-check-fix.md).

## I-18: Implement the two measurement repairs

After reading the relevant reporting and evaluation files in the prior turn, the agent needed a direct instruction to stop exploring and write the two measurement fixes and their regression tests.

> Implement the two requested function changes now in eval/live.py, add only the focused regression file, run it and ruff on the two files, then stop.

The two owner functions already contained the necessary inputs. A bounded follow-up kept the repair focused on report assembly and price measurement.

OpenCode updated `src/research_desk/eval/live.py` and created `test/offline/test_evaluation_report_checks.py`. Verification passed 20 new report-check tests and 16 existing live-fix tests.

Result: [live.py](../../src/research_desk/eval/live.py), [test_evaluation_report_checks.py](../../test/offline/test_evaluation_report_checks.py).

Source: [project-report-check.full.json.gz](../project-report-check.full.json.gz), message `msg_057f8527f001r563E00o2BDptA`, JSON pointer `/messages/35`. Session: `ses_fa80b1435ffeLfgOoIjVIDIpKP`.

## I-19: Match signed and multi-digit prices

Review of `_PRICE_TOKEN_RE` in `src/research_desk/eval/live.py` showed that the regular expression missed ungrouped four-digit numbers such as `1234.50` and stripped leading minus signs from negative numbers.

> Fix only numeric token matching/normalization in live.py so ungrouped integers of any length work, correctly grouped comma amounts work, and signs remain part of the numeric value.

Capturing optional signs inside the numeric token and matching both ungrouped integers and comma-grouped thousands guaranteed exact Decimal comparisons for reported prices.

OpenCode updated the price token regex in `src/research_desk/eval/live.py` and added four boundary assertions in `test/offline/test_evaluation_report_checks.py`, reaching 24 passing tests in that module.

Result: [live.py](../../src/research_desk/eval/live.py), [test_evaluation_report_checks.py](../../test/offline/test_evaluation_report_checks.py).

Source: [project-report-check.full.json.gz](../project-report-check.full.json.gz), message `msg_057fb5d840011lq7JQaffU0S3K`, JSON pointer `/messages/53`. Session: `ses_fa80b1435ffeLfgOoIjVIDIpKP`.

## I-20: Retain every observed tool result

The evaluation judge read observed tool outputs from `input.data_snapshot`, a dictionary keyed by tool name that overwrote earlier indicator calls whenever a tool was invoked multiple times.

> Extend only eval/live.py judge input plumbing so the judge receives all actual nonempty tool_result payload result strings from pack.events, retaining event/source context; identical repeated outputs may be deduplicated, but different outputs from the same tool must survive.

Extracting `tool_result` payloads in event order from `pack.events` ensured that the judge saw every distinct technical indicator observation produced during the research run.

OpenCode added `_observed_tools_text(events)` in `src/research_desk/eval/live.py` and updated `test/offline/test_evaluation_report_checks.py` and `test/offline/test_live_fixes.py` to verify multi-call indicator retention.

Result: [live.py](../../src/research_desk/eval/live.py), [test_evaluation_report_checks.py](../../test/offline/test_evaluation_report_checks.py), [test_live_fixes.py](../../test/offline/test_live_fixes.py).

Source: [project-report-check.full.json.gz](../project-report-check.full.json.gz), message `msg_05800ec90001aaWvxmwNDIwJz1`, JSON pointer `/messages/59`. Session: `ses_fa80b1435ffeLfgOoIjVIDIpKP`.
