# Architecture candidate evaluation

Scores are design judgments by leo on a1–5 scale, not benchmark measurements. Weights sum to1.0.

| Criterion | Weight | A: edit core graph | B: application seams | C: replacement demo |
|---|---:|---:|---:|---:|
| Preserve baseline behavior |0.25|3|5|1|
| Deterministic authority boundary |0.25|3|5|4|
| Evidence capture completeness |0.20|5|4|4|
| Delivery scope |0.15|2|4|5|
| Upstream maintainability |0.15|2|5|2|
| Weighted design score |1.00|3.10|4.65|3.10|

Candidate B is selected. Direct identity and returns reads require narrow subclass seams because ordinary tool callbacks do not capture them. Candidate A becomes reasonable only if upstream contracts fundamentally prevent required capture. Candidate C cannot establish that the new workflow extends a real existing system and gives a weak comparison baseline.
