# Research Desk Analysis Report

- Company (legal identity): Apple Inc.
- Ticker: AAPL
- Analysis date: 2026-07-31
- Evidence latest close: 308.91 USD [source: market-aapl, market CSV as-of 2026-07-31]
- Official earnings source: src-aapl
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

# Research Desk Run Report: AAPL on 2026-07-31

- run_id: `run-c46913ab360b`
- outcome: `completed`
- signal: `Hold`
- context mode: `baseline`
- data mode: `frozen`
- analysts: market, news
- prompt version: `research-desk-0.1.2`
- created at: 2026-11-09T15:09:59.737482Z
- source pack: none (original run)
- budget max calls: 32

## Usage

- LLM calls: 13
- input tokens: 79611
- output tokens: 18286
- total tokens: 97897
- stop reason: completed

## Input snapshot

- instrument context chars: 392
- past context chars: 540
- identity: {'company_name': 'Apple Inc.', 'sector': 'Technology', 'industry': 'Consumer Electronics'}
- frozen tool data: 7 entries
- memory sources: frozen-pack

## Events

| kind | count |
|---|---|
| context_assembled | 1 |
| context_budget | 12 |
| data_read | 1 |
| llm_request | 13 |
| llm_response | 13 |
| run_end | 1 |
| run_start | 1 |
| tool_call | 26 |
| tool_result | 26 |