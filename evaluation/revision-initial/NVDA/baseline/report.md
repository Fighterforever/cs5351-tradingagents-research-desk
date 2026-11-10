# Research Desk Analysis Report

- Company (legal identity): NVIDIA Corporation
- Ticker: NVDA
- Analysis date: 2026-08-27
- Evidence latest close: 227.98 USD [source: market-nvda, market CSV as-of 2026-08-27]
- Official earnings source: src-nvda
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

# Research Desk Run Report: NVDA on 2026-08-27

- run_id: `run-3e4be6a2c07d`
- outcome: `completed`
- signal: `REVIEW`
- context mode: `baseline`
- data mode: `frozen`
- analysts: market, news
- prompt version: `research-desk-0.1.2`
- created at: 2026-11-09T14:59:35.361122Z
- source pack: none (original run)
- budget max calls: 32

## Usage

- LLM calls: 15
- input tokens: 46106
- output tokens: 22272
- total tokens: 68378
- stop reason: completed

## Input snapshot

- instrument context chars: 394
- past context chars: 543
- identity: {'company_name': 'NVIDIA Corporation', 'sector': 'Technology', 'industry': 'Semiconductors'}
- frozen tool data: 7 entries
- memory sources: frozen-pack

## Events

| kind | count |
|---|---|
| context_assembled | 1 |
| context_budget | 14 |
| data_read | 1 |
| llm_request | 15 |
| llm_response | 15 |
| run_end | 1 |
| run_start | 1 |
| tool_call | 18 |
| tool_result | 18 |