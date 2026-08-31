# Annotated OpenCode session7: accurate evaluation inputs and mandatory fields

Session: ses_fa80b1435ffeLfgOoIjVIDIpKP. Complete native export: project-report-check.full.json.gz. Prompt: prompts/project-report-check-fix.md. The original event turns are project-report-check-fix.raw.jsonl, project-report-check-focus.raw.jsonl and project-report-number-fix.raw.jsonl. The gzip preserves the full84.8MB native record losslessly; the original JSON parsed successfully and the configured credential was absent.

Intervention1 tightened frozen_price_used. The first implementation only looked for the close in input evidence. The corrected check also requires the expected price to appear as a complete monetary value in generated report text. The real tests cover missing/wrong prices and numerical boundaries, including negative values and thousands separators. The repair strengthens measurement without changing the LLM scoring rubric.

Intervention2 retained role and stage headings when assembling a research report for the judge. Analyst and trader opinions remain visible, including disagreement with the final portfolio decision. Only a byte-identical duplicate risk/final terminal field is omitted. The operation does not rewrite any generated sentence or hide an unfavorable intermediate opinion.

Intervention3 stopped repeated exploration and constrained the continuation to the two actual owner functions and their focused tests. The final run recorded24 focused parameterized passes, with16 existing live-fix tests also passing earlier. The measurement source was frozen before the final judgments; evaluation/final/measurement-provenance.json records the actual source provenance. All initial development judgments remain unchanged in their archived directory.
