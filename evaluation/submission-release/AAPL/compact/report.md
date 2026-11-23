# Research Desk Analysis Report

- Company (legal identity): Apple Inc.
- Ticker: AAPL
- Analysis date: 2026-07-31
- Evidence latest close: 308.91 USD [source: market-aapl, market CSV as-of 2026-07-31]
- Official earnings source: src-aapl
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

# Research Desk Run Report: AAPL on 2026-07-31

- run_id: `run-cc27914d6fa7`
- outcome: `completed`
- signal: `Underweight`
- context mode: `compact`
- data mode: `frozen`
- analysts: market, news
- prompt version: `research-desk-0.1.2`
- created at: 2026-11-22T14:04:13.996397Z
- source pack: none (original run)
- budget max calls: 32

## Usage

- LLM calls: 13
- input tokens: 53448
- output tokens: 8754
- total tokens: 62202
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
| tool_call | 16 |
| tool_result | 16 |

## Proposal

### Proposal `prop-89ab6186b1e7`

- status: `PENDING_REVIEW`
- run: `run-cc27914d6fa7`
- ticker: AAPL on 2026-07-31
- signal: Underweight
- side: sell
- price (from evidence): 308.9100036621094
- evidence id: b04b3fdd049078ed3a77f4b39ecf783a739d56dd32c2b793a1a97bca5608808d
- shares (operator): None
- proposal version: `862ba8ee244a597b`
- operator: n/a
- approved version: n/a
- reason: n/a