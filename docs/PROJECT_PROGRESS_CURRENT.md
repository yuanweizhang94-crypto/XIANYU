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
