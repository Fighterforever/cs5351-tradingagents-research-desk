# Research Desk Analysis Report

- Company (legal identity): Apple Inc.
- Ticker: AAPL
- Analysis date: 2026-07-31
- Evidence latest close: 308.91 USD [source: market-aapl, market CSV as-of 2026-07-31]
- Official earnings source: src-aapl
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

# Research Desk Run Report: AAPL on 2026-07-31

- run_id: `run-ad25c78521e6`
- outcome: `completed`
- signal: `Underweight`
- context mode: `baseline`
- data mode: `frozen`
- analysts: market, news
- prompt version: `research-desk-0.1.2`
- created at: 2026-11-22T14:02:48.728746Z
- source pack: none (original run)
- budget max calls: 32

## Usage

- LLM calls: 14
- input tokens: 83766
- output tokens: 19966
- total tokens: 103732
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
| context_budget | 13 |
| data_read | 1 |
| llm_request | 14 |
| llm_response | 14 |
| run_end | 1 |
| run_start | 1 |
| tool_call | 26 |
| tool_result | 26 |

## Proposal

### Proposal `prop-c434394ae262`

- status: `PENDING_REVIEW`
- run: `run-ad25c78521e6`
- ticker: AAPL on 2026-07-31
- signal: Underweight
- side: sell
- price (from evidence): 308.9100036621094
- evidence id: 5a7658834fe286971d4bfc4e4e25a7daa704f7de7fe521d8a9bd55b25d5adce8
- shares (operator): None
- proposal version: `910bcb79e3c60701`
- operator: n/a
- approved version: n/a
- reason: n/a