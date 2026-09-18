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
