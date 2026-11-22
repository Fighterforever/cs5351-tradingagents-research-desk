# Research Desk Analysis Report

- Company (legal identity): Microsoft Corporation
- Ticker: MSFT
- Analysis date: 2026-07-30
- Evidence latest close: 451.10 USD [source: market-msft, market CSV as-of 2026-07-30]
- Official earnings source: src-msft
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

# Research Desk Run Report: MSFT on 2026-07-30

- run_id: `run-0f3d91fc8c7c`
- outcome: `completed`
- signal: `Overweight`
- context mode: `baseline`
- data mode: `frozen`
- analysts: market, news
- prompt version: `research-desk-0.1.2`
- created at: 2026-11-22T14:02:22.362578Z
- source pack: none (original run)
- budget max calls: 32

## Usage

- LLM calls: 14
- input tokens: 81327
- output tokens: 17336
- total tokens: 98663
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
| context_budget | 13 |
| data_read | 1 |
| llm_request | 14 |
| llm_response | 14 |
| run_end | 1 |
| run_start | 1 |
| tool_call | 23 |
| tool_result | 23 |

## Proposal

### Proposal `prop-b9c6d03b16de`

- status: `PENDING_REVIEW`
- run: `run-0f3d91fc8c7c`
- ticker: MSFT on 2026-07-30
- signal: Overweight
- side: buy
- price (from evidence): 451.1000061035156
- evidence id: e21cd05ce3b11d77ff08e8e2d6a3c257b1518870dfed0ee8623bd8dc169517cb
- shares (operator): None
- proposal version: `dfdf806b060ddd51`
- operator: n/a
- approved version: n/a
- reason: n/a