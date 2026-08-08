# CHG-0017 runtime safety block

Run ID: `CHG17-DELIVERY-20260731T062755Z-GSLF`

## Scope

- Active Change: `CHG-0017-upstream-native-auto-ai-delivery`
- Status at run start: `IMPLEMENTING`
- Started candidate management services: yes
- Started candidate websocket-only service: yes
- Started `ACCOUNT-A`: yes, exactly once
- Started `OWNER_TEST_ACCOUNT_B` automatic-reply task: no
- Messages sent: `0`
- Secrets or full account identifiers recorded: no

## T8 Result

- `token.api_mode`: `remote`
- Remote Token connectivity: success
- Real remote Token event: `remote_token` / `success`
- Token present after start: yes
- Device ID present after start: yes
- WebSocket state: `connected`
- Stable observation: `60 seconds`
- Browser launch signal: no
- Send signal: no
- Auto-reply log delta during T8: `0`
- AI message delta during T8: `0`
- Successful send delta during T8: `0`

## Isolation Finding

Latest upstream candidate did not expose an existing sender allowlist or test-mode
isolation control for live automatic-reply sending. Random keyword isolation was
insufficient for AI validation because enabling AI could answer a non-whitelist
inbound message during the live window.

A minimal default-off upstream candidate patch was prepared locally after
stopping `ACCOUNT-A` and all candidate services:

- `websocket/app/services/xianyu/auto_reply_service.py`
- `tests/test_chg0017_reply_allowlist.py`

Patch behavior:

- Default upstream behavior is unchanged when the gate is not enabled.
- When enabled, automatic reply sending is denied before sender invocation unless
  both the receiver account and inbound sender match the configured allowlist.
- Denied messages are recorded as skipped with decision reason
  `chg0017_allowlist_denied`.
- No new Token, WebSocket, sender, AI, keyword, default-reply, or worker
  implementation was added.

Targeted candidate test:

- `python -m unittest tests.test_chg0017_reply_allowlist -v`
- Result: passed, `4` tests.

## Stop Reason

The run stopped because the current execution contract forbids a second
`ACCOUNT-A` start in this live attempt. Continuing after the post-T8 isolation
patch would require starting `ACCOUNT-A` again. No second start was performed.

Verdict: `RUNTIME_SAFETY_BLOCK`

## Cleanup

- `ACCOUNT-A` stop called once: yes
- Candidate websocket stopped: yes
- Candidate backend/frontend/mysql/redis stopped: yes
- Ports `18090`, `8090`, `28090`, `28089`: closed
- Quiet period: `120 seconds`
- Auto-reply log delta after quiet period: `0`
- Successful send delta after quiet period: `0`
- AI message delta after quiet period: `0`
- Default reply record delta after quiet period: `0`
- Active keyword rules after quiet period: `0`
- Enabled default replies after quiet period: `0`

## Next Minimal Action

Project owner must explicitly authorize a fresh controlled CHG-0017 live attempt
using the prepared default-off allowlist gate before `ACCOUNT-A` is started
again. The next attempt should start from zero-send baseline, enable the
allowlist only for `ACCOUNT-A` and `OWNER_TEST_ACCOUNT_B`, then run the approved
keyword and AI tests without exceeding the 8-reply cap.
