# Research Desk Analysis Report

- Company (legal identity): Microsoft Corporation
- Ticker: MSFT
- Analysis date: 2026-07-30
- Evidence latest close: 451.10 USD [source: market-msft, market CSV as-of 2026-07-30]
- Official earnings source: src-msft
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

# Research Desk Run Report: MSFT on 2026-07-30

- run_id: `run-e663cb0910b1`
- outcome: `completed`
- signal: `REVIEW`
- context mode: `baseline`
- data mode: `frozen`
- analysts: market, news
- prompt version: `research-desk-0.1.2`
- created at: 2026-11-09T14:59:58.223395Z
- source pack: none (original run)
- budget max calls: 32

## Usage

- LLM calls: 16
- input tokens: 51721
- output tokens: 22752
- total tokens: 74473
- stop reason: completed

## Input snapshot

- instrument context chars: 408
- past context chars: 556
- identity: {'company_name': 'Microsoft Corporation', 'sector': 'Technology', 'industry': 'Software — Infrastructure'}
- frozen tool data: 7 entries
- memory sources: frozen-pack

## Events

| kind | count |
|---|---|
| context_assembled | 1 |
| context_budget | 15 |
| data_read | 1 |
| llm_request | 16 |
| llm_response | 16 |
| run_end | 1 |
| run_start | 1 |
| tool_call | 21 |
| tool_result | 21 |