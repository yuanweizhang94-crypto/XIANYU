Run ID: CHG17-GEMINI-LIVE-20260731T081613Z-LDEK

Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
Verdict: RUNTIME_SAFETY_BLOCK

## Scope

This run continued the approved CHG-0017 live validation after the Gemini AI
provider was configured for ACCOUNT-A in the isolated latest-upstream candidate
runtime.

No business code, Token implementation, WebSocket implementation, sender
implementation, AI provider implementation, Docker compose source, or tracked
upstream source was modified during this run.

## Provider Gate

- Gemini model discovery: passed.
- Gemini provider test: passed.
- Selected model: gemini-3.6-flash.
- Sender invocation during provider test: 0.
- Platform message sends during provider test: 0.
- Secret values recorded in repository evidence: no.

## Runtime Setup

- Candidate management runtime: started.
- Candidate websocket runtime: started.
- ACCOUNT-A native account start count: 1.
- ACCOUNT-A native connection: connected.
- Browser launches observed by this run: 0.
- Token algorithm changed: no.
- Token cache cleared: no.
- Cookie cleared: no.
- OWNER_TEST_ACCOUNT_B automatic reply task: not started.
- CHG-0010 worker: stopped.
- Scheduler: stopped.
- Docker pilot websocket: stopped.

## Controlled Test Trigger

The upstream-native online chat send route was located, but it required an
already connected online-chat conversation context. To avoid creating a second
sender or expanding the test runtime, the run switched to the approved
OWNER_TEST_MESSAGES_REQUIRED path and asked the project owner to send the four
approved test messages from OWNER_TEST_ACCOUNT_B.

Message contents are not recorded in this evidence.

## Blocker

The live runtime exceeded the approved 20 minute validation window before the
owner-message result audit completed. During the cleanup audit, the isolated
candidate database showed new automatic-reply processing rows, but zero
successful sends.

A database audit attempt used an ORM path that printed a full account identifier
in an exception traceback. No Cookie, Token, API key, Device ID, UNB, customer
message body, chat ID, item ID, or platform verification URL was printed. The
run was failed closed immediately after this output-boundary violation.

## Masked Audit Summary

- new_auto_reply_rows: 5
- new_successful_sends: 0
- new_failed_rows: 0
- new_skipped_rows: 5
- keyword_success_rows: 0
- ai_expected_success_rows: 0
- context_user_rows: 0
- context_assistant_rows: 0
- non_allowlist_new_rows: 4
- distinct_new_senders: 2
- auto_reply_total_delta: 5
- auto_reply_success_delta: 0
- ai_total_delta: 0
- ai_assistant_delta: 0
- default_reply_records_delta: 0

## Cleanup

- ACCOUNT-A stop request count: 1.
- ACCOUNT-A stop result: success.
- Candidate AI enabled after cleanup: false.
- Candidate Gemini API key retained in candidate DB after cleanup: false.
- Temporary keyword rules active after cleanup: 0.
- Local Gemini env file after cleanup: deleted.
- Candidate websocket after cleanup: stopped.
- Candidate backend/frontend after cleanup: stopped.
- Candidate MySQL after offline audit: stopped.
- Port 18090 after cleanup: closed.
- Port 8090 after cleanup: closed.
- Port 28090 after cleanup: closed.
- Port 28089 after cleanup: closed.
- CHG-0010 worker after cleanup: stopped.
- Host manual-listener after cleanup: stopped.
- Project-owned browser/profile residuals: 0.
- Quiet period: 120 seconds completed.
- Runtime reactivation during quiet period: none observed.

## Result

T12 is not passed.
T13 is not executed.
CHG-0017 remains IMPLEMENTING.

The smallest next action is to inspect the skipped automatic-reply decisions and
the sender allowlist mapping using masked identifiers only, then rerun a new
owner-approved controlled validation window after the allowlist/account mapping
is corrected.
