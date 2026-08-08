# CHG17-GO-LIVE-20260731T1431Z Masked Report

Verdict: DELIVERY_READY

## Scope

- Account: ACCOUNT-A
- Test sender: OWNER_TEST_ACCOUNT_B
- Candidate upstream: D:/xianyu-upstream-delivery-chg0017
- Draft PR: #26
- PR state after run: Draft, Open, Unmerged

No Cookie, Token, API key, Device ID, UNB, full account ID, full chat/session
ID, full item ID, customer message body, AI reply body, verification URL, or
database credential is recorded in this evidence.

## Configuration

- secret_present: true
- secret_length: 53
- secret source: gitignored local secret file
- provider_type: gemini
- base_url: https://generativelanguage.googleapis.com
- model_name: gemini-3.6-flash
- model_name has `models/` prefix: false
- api_key: present_redacted
- custom prompt present: true
- active keyword rules: 0
- enabled default replies: 0
- enabled filters: 0

## Provider Test

- provider_test: pass
- assistant content generated: true
- HTTP 404: false
- sender invocation: 0
- platform send: 0
- API key in captured logs/errors: false

## Controlled Runtime Tests

- ACCOUNT-A native task start: success
- ACCOUNT-A final connection: connected
- OWNER_TEST_ACCOUNT_B official IM connect: success
- OWNER_TEST_ACCOUNT_B conversation with ACCOUNT-A: found

### Context

- official B send: true
- ACCOUNT-A autoreply log delta: 1
- successful send delta: 1
- assistant delta: 1
- reply_strategy: ai
- send_status: success
- context_used: true

### Duplicate Protection

- official B sends: 2
- platform send results: 2 success
- autoreply log delta: 2
- successful reply delta: 1
- assistant delta: 1
- duplicate detected: true
- second reply sent: false

### Stop

- ACCOUNT-A stop: success
- stopped state observed: true
- official B send while stopped: true
- autoreply log delta while stopped: 0
- successful send delta while stopped: 0
- assistant delta while stopped: 0
- ACCOUNT-A restart: success
- reconnected: true
- post-restart unexpected log delta: 0
- post-restart unexpected AI delta: 0

### Reconnect

- precondition: connected
- official B send after reconnect: true
- autoreply log delta: 1
- successful send delta: 1
- assistant delta: 1
- reply_strategy: ai
- send_status: success
- final connection: connected

## Rollback Drill

- AI temporarily disabled: true
- ACCOUNT-A stop success: true
- websocket stop/start used existing compose: true
- log delta during stopped state: 0
- successful send delta during stopped state: 0
- assistant delta during stopped state: 0
- AI restored: true
- ACCOUNT-A restored: running
- ACCOUNT-A final connection: connected

## Final Audit

- candidate MySQL: running
- candidate Redis: running
- candidate backend: running and healthy
- candidate websocket: running and healthy
- backend health: reachable on http://127.0.0.1:28089/health
- ACCOUNT-A task: running
- ACCOUNT-A connection: connected
- AI enabled: true
- provider_type: gemini
- base_url: https://generativelanguage.googleapis.com
- model_name: gemini-3.6-flash
- api_key: present_redacted
- active keyword rules: 0
- enabled default replies: 0
- enabled filters: 0
- non-whitelist successful reply sends: 0
- proactive customer sends by CHG-0017: 0
- verify_repository local noise: non_blocking_documented

## Operational Boundary

CHG-0017 validates and enables upstream-native ACCOUNT-A AI automatic reply
through the controlled candidate runtime. It does not validate image replies,
order/refund/shipping/rating/listing mutation behavior, non-whitelist customer
outreach, or a second automatic reply executor.
