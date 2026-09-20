# CHG-0038 Production Activation and Real Auto Reply E2E — 2026-09-20

Change ID: CHG-0038-websocket-registration-readiness
Status: VERIFYING

## Production activation

Canonical root cause:

```text
ROOT_CAUSE=NATIVE_WS_FALSE_HEALTH_AFTER_UNCONFIRMED_REGISTRATION
REGISTRATION_ACK_REQUIRED=true
UNCONFIRMED_REGISTRATION_MUST_NOT_MARK_CONNECTED=true
```

Activated immutable WebSocket image:

```text
NEW_WEBSOCKET_IMAGE=xianyu-chg0038-websocket:registration-readiness-20260920-r2
NEW_WEBSOCKET_IMAGE_ID=sha256:e9521294a50af7e4157dcf91321a9d02a32f045246bbaa73f91244f9e972d46a
LIVE_XIANYU_ASYNC_SHA256=6db8beb83d1c7090731404a1d8ec71f4e42b020116ada7f4c4324b384cc6374b
ACTIVATED_CONTAINER_ID=7a02c24ffc5429b1d07668406a5e52901b02b8403f0c52256bfd848d11daaf51
ACTIVATION_STARTED_AT=2026-09-20T03:11:59.609397574Z
```

Protected replacement preserved the previous image as the rollback anchor during the cutover. Final replacement completed with HTTP health 200 and secret_binding_preserved=true.

Post-activation readback:

```text
POST_SWITCH_ACTIVE_ACCOUNTS=8
POST_SWITCH_WS_CONNECTED=8
POST_SWITCH_TOKEN_READY=8
REGISTRATION_ACK_PROVEN_COUNT=8
MESSAGE_LOOP_READY_COUNT=8
HUMAN_QR_REQUIRED_COUNT=0
PLATFORM_VERIFICATION_REQUIRED_COUNT=0
ONLINE_ACCOUNT_DROPPED_COUNT=0
```

All eight active accounts logged the new matching registration acknowledgement before initialization completion and before entering the normal WebSocket message loop.

## Real registration rejection proof

Account 2217936413500 produced a real production registration rejection during the first post-activation connection attempt:

```text
REGISTRATION_RESPONSE_CODE=401
CONNECTED_AFTER_REJECT=false
EXISTING_RECONNECT_PATH_USED=true
LATER_REGISTRATION_ACK=success
LATER_MESSAGE_LOOP_READY=true
```

This is direct production proof that an unconfirmed/non-200 registration no longer marks the Native WebSocket as ready. No QR/password login, Cookie invalidation, Session rebuild, or alternate WebSocket owner was introduced.

## Organic post-activation Auto Reply E2E

The accepted E2E event occurred strictly after the new Runtime activation time.

```text
REAL_E2E_ACCOUNT=2221384086829
REAL_E2E_ITEM=1086370184047
REAL_E2E_INBOUND_AT=2026-09-20T11:20:44+08:00
MESSAGE_HANDLER_ENTERED=true
AUTO_REPLY_SERVICE_ENTERED=true
AUTO_REPLY_RULE_MATCHED=true
MATCHED_RULE_TYPE=default_item
REPLY_MODE=text_image
AUTO_REPLY_SEND_ATTEMPTED=true
IMAGE_SEND=success
TEXT_SEND=success
AUTO_REPLY_SEND_STATUS=success
SANITIZED_REPLY_ACTIVITY_ID=734
```

Runtime sequence:

```text
Native WS inbound
→ existing MessageHandler
→ existing AutoReplyService
→ item default-reply rule
→ image upload/send success
→ text send success
→ sanitized auto-reply activity: reply_sent / success / text_image
```

Two additional organic post-activation successful reply activities were also observed, including another event on the same item/account and one on account 2196106636. They are corroborating evidence only; the single event above is sufficient for acceptance.

No buyer message text, buyer identifier, Cookie, Token, Authorization, password, QR payload, or other customer-sensitive content is stored in this evidence.

## Final state-machine invariant

```text
REGISTRATION_FAILURE
→ existing reconnect path
→ MUST_NOT_MARK_CONNECTED

REGISTRATION_SUCCESS(code=200 + matching mid)
→ ackDiff
→ initialization complete
→ CONNECTED
→ message loop ready
```

AUTO_REPLY_REAL_E2E=PASS
PERMANENT_WEBSOCKET_RUNTIME_PATCH=PASS
