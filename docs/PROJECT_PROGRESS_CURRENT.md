# XIANYU Current Progress

For the complete current project recovery history, read:

`docs/PROJECT_PROGRESS_2026-08-18.md`

For the concise final state, read:

`docs/PROJECT_PROGRESS_2026-08-18_SUMMARY.md`

Current business state:

`AUTO_REPLY_READY=true; PUBLISH_READY=true; CHAT_OPTIONAL=true; PRODUCTION_BUSINESS_READY=true`

## 2026-09-18 ASTRA Publisher Session repair

Current Git/Runtime verification on `PC-20250528MGDP` proved two separate facts:

1. The formal Publisher capability for accounts `1992416548` and `2196106636` is currently valid. Both canonical Cookies passed the Publisher-equivalent MTOP auth probe and `detect_publish_account_capability`.
2. WebSocket process-local state remained stale after an authoritative renewal had already succeeded. The successful `renew_auth_valid` branch updated the authoritative Cookie but did not clear the old `platform_verification_required / FAIL_SYS_USER_VALIDATE` in-memory marker.

The production repair is intentionally minimal:

```text
renew_auth_valid
→ authoritative Cookie commit
→ clear persisted PVR marker
→ _clear_platform_verification_required()
→ last_token_refresh_status=success
```

The independent internal route bug is also fixed:

```text
OLD: instance.token_manager.trigger_refresh()
NEW: instance.refresh_token()
```

Activated WebSocket image:

```text
xianyu-chg0035-websocket:publish-session-fix-20260918-r1
```

Post-activation readback for both target accounts:

```text
CONNECTED=true
TOKEN_READY=true
PLATFORM_VERIFICATION_REQUIRED=false
HUMAN_QR_REQUIRED=false
PUBLISH_READY=true
```

Formal real ASTRA verification:

```text
1992416548 / material 108
FINAL_STATUS=SUCCESS
PLATFORM_ITEM_ID=1086163872502
AUTHORITATIVE_SYNC_CONFIRMED=true

2196106636 / material 109
PUBLISH_PREFLIGHT=PASS
PUBLISH_READY=true

INITIAL_ATTEMPT=FAILED
FAILURE_REASON=FAIL_BIZ_SHOP_IMPROVE_PACK_QUERY_EXP
INITIAL_PRODUCT_CREATED=false

AUTHORITATIVE_NO_ITEM_PROOF=PASS
CONTROLLED_REAL_RETRY=1
FINAL_STATUS=SUCCESS
PLATFORM_ITEM_ID=1086172352322
AUTHORITATIVE_SYNC_CONFIRMED=true
```

The Fish Shop failure was traced to the final `mtop.idle.pc.backend.idleitem.publish` request. The platform returned `FAIL_BIZ_SHOP_IMPROVE_PACK_QUERY_EXP` with `account_invalid=false` and a retry-later message. Current upstream contains no dedicated fix or separate no-write pack-query endpoint, while the current Runtime already carries the more complete Fish Shop publish path. After publish-log, operation-store, item-sync, and catalog readback proved no item had been created, one controlled retry succeeded. The failure is therefore classified as a platform-side transient business failure rather than a Session, Token, QR, platform-verification, or local Publisher implementation defect.

Full closure evidence: `docs/ASTRA_PUBLISH_CLOSURE_20260918.md`.

## 2026-09-19 Online Chat account-cache ownership follow-up

A customer conversation appeared under account `2221422775489` (华为8.19可用), but Runtime evidence proved the message actually belonged to account `2804730247` and item `1083167295431`. Auto Reply itself succeeded (`AUTO_REPLY_LOG_ID=660`, `send_status=success`).

Backend ChatNew WebSocket forwarding was verified to remain strictly account-scoped. The remaining defect was frontend cache convergence: the existing 2026-08-29 request-generation guard rejected stale async responses, but an authoritative empty conversation response did not overwrite an older per-account conversation cache entry.

Production fix:

```text
fresh conversation server truth
→ always replace convsCacheRef.current[accountId]
→ including an empty conversation list
→ then update visible conversations
```

Activated frontend image:

```text
xianyu-chg0018-frontend:chatnew-account-cachefix-20260919-r1
```

Runtime readback:

```text
FRONTEND_STATUS=running|healthy
ONLINE_CHAT_HTTP=200
CACHEFIX_CHUNK_HTTP=200
```

Exact production hotfix persistence:

```text
scripts/patch_chatnew_account_cachefix_20260919.py
BASE_CHATNEW_SHA256=7d58515be1e86a9370b8fcce91a08943e4c9df253838477f0eba4e92e0294843
FIXED_CHATNEW_SHA256=5a55733f22d0b18b56b1c2ffb7a02a4c55a8e3d8cfab39adb952ae1ea28bc79b
```

Full evidence: `docs/ONLINE_CHAT_ACCOUNT_CACHE_FIX_20260919.md`.

## 2026-09-19 multi-account publish balancing rule

Future ordinary multi-account publish batches must carry account-balance state across batches instead of restarting from a fixed first account.

```text
PUBLISH_ACCOUNT_ROTATION_REQUIRED=true
PUBLISH_ACCOUNT_BALANCING_REQUIRED=true
STRICT_SELECTED_ACCOUNT_AFTER_ASSIGNMENT=true
```

The balance metric is authoritative successful real publishes only. Current adoption baseline from `ASTRA-R2-20260919`:

```text
1992416548      = 2
2804730247      = 2
2214313339860   = 2
2196106636      = 2
2221422775489   = 1
2221384086829   = 1
```

Therefore, if these six accounts remain publish-ready, the next automatically assigned products must prioritize:

```text
2221422775489
2221384086829
```

until the carried counts are level again.

The balancing rule applies before account assignment only. It never overrides UNKNOWN/no-blind-retry or strict selected-account safety after a real operation exists.

Full policy: `docs/PUBLISH_ACCOUNT_ROTATION_POLICY_20260919.md`.

## 2026-09-19 Online Chat account-status spinner convergence

Production proved that an actually usable Chat account could still be returned as `SESSION_CHECKING`:

```text
ACCOUNT_ID=2221422775489
Native WS connected=true
token_ready=true
Chat conversations=SUCCESS
runtime_connected=true

/chat-new/accounts:
connected=false
chat_state=SESSION_CHECKING
session_state=SESSION_CHECK_PENDING
```

The production ChatNew bundle also loaded the account list only once on mount, so a transient checking value could remain indefinitely in React state after Backend truth changed.

Frontend-only repair:

```text
RUNTIME_IMAGE=
xianyu-chg0018-frontend:chatnew-spinner-convergence-20260919-r1

5-second silent account-state reconciliation
+ runtime_connected Chat truth convergence
+ disabled-account terminal rendering
+ idempotent existing Chat owner connect for Native-WS-ready accounts
```

No Backend/WebSocket restart occurred. No real Session, Token, Cookie, QR, account-enabled-state, Redis Session, Auto Reply, Publisher, order, or item mutation occurred.

Regression:

```text
21 passed
BASE_CHATNEW_SHA256=
5a55733f22d0b18b56b1c2ffb7a02a4c55a8e3d8cfab39adb952ae1ea28bc79b

FIXED_CHATNEW_SHA256=
4345c358b1d7539b38ab0cff0d714b839632d248ba9bceac5f0f8b094aa303a1
```

Final live state after the last Native-WS-ready account received exactly one existing Chat-owner connect:

```text
ACCOUNT_ROWS=13
ACTIVE_ACCOUNTS=10
NATIVE_WS_CONNECTED=10/10
CHAT_RUNTIME_CONNECTED=10/10

UI_CONNECTED=10
UI_LOGIN_REQUIRED=0
UI_DISABLED=3
UI_SPINNER=0
```

The final production CASE_8 was also exercised: a newly Native-ready account had no Chat owner, received one existing `/chat-new/connect/{account_id}` call, then returned conversation `SUCCESS`. The other nine connected accounts were not reconnected.

Full evidence: `docs/ONLINE_CHAT_SPINNER_CONVERGENCE_20260919.md`.

## 2026-09-19 Online Chat reconnect convergence follow-up

A later live incident on account `2217936413500` proved that the previous `autoChatOnce` safety latch was too strict.

Observed sequence:

```text
19:14:12 Native WS keepalive ping timeout
→ Native WS disconnect
19:14:38 WebSocket re-established
19:14:39 connection registration completed
→ Native WS connected=true
→ token_ready=true
→ login remained valid

but:
ChatNew owner missing
conversations=账号未连接
```

Root cause:

```text
initial automatic Chat connect
→ account stored forever in autoChatOnce
→ later Native WS disconnect/recovery
→ Chat owner lost
→ frontend permanently refuses another automatic Chat connect
```

The Frontend-only fix replaces the one-shot latch with a cooldown-based guard:

```text
autoChatRetryAt
already connected/runtime_connected → no-op
connect in flight → no-op
Native WS/token not ready → no-op
terminal login/verification gate → no-op
Chat owner missing → existing /chat-new/connect/{account_id}
retry cooldown=15 seconds
```

Activated Runtime:

```text
xianyu-chg0018-frontend:chatnew-reconnect-convergence-20260919-r1

BASE_CHATNEW_SHA256=
4345c358b1d7539b38ab0cff0d714b839632d248ba9bceac5f0f8b094aa303a1

FIXED_CHATNEW_SHA256=
326750c9383b392e58f6f864906359d2c7b2f6377519d698adf46852ca2c1d6e
```

Account `2217936413500` was recovered through the existing Chat owner without restarting Backend/WebSocket, and its conversation API returned `SUCCESS`.

Auto Reply configuration was verified still present for its published products: image + text, enabled, `reply_once=false`. Native WebSocket source re-enters the message loop after reconnect; no post-reconnect inbound buyer-message event was present in Runtime logs during the incident.

Regression: `30 passed` across the new reconnect suite and all previous Online Chat convergence suites.

Full evidence: `docs/ONLINE_CHAT_RECONNECT_RECOVERY_20260919.md`.
