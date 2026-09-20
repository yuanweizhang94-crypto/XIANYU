# 2026-09-20 Target-account recovery evidence

All values are sanitized. No Token, Cookie, buyer body, secret, or credential value is stored.

## Maru / 2214313339860

Before recovery:

```text
LAST_PROVEN_BUYER_PUSH=2026-09-20 10:40:56
OLD_TOKEN_GENERATION=2026-09-20 10:00:48
OLD_TOKEN_SHA12=f0a26cb28e07
OLD_DEVICE_SHA12=d1a3ecdcb5aa
TOKEN_REFRESH_STATE=success_from_cache
REGISTRATION_ACK=PASS
HEARTBEAT=PASS
```

A single-account restart with invalidate_token_cache=true at 21:55 still logged the same cached Token fingerprint. The cache row had expire_at == renew_expire_at == updated_at, proving the explicit invalidation marker was being consumed by startup expired-cache fallback.

Bounded target-only state recovery:

```text
TARGET_CACHE_ROW_DELETED=1
OTHER_CACHE_ROWS_TOUCHED=0
RESTART_INVALIDATE_TOKEN_CACHE=false
TOKEN_CACHE_MISS=true
TOKEN_API_RESPONSE=SUCCESS
NEW_TOKEN_GENERATION=2026-09-20 22:37:55
NEW_TOKEN_SHA12=2edfb21da80d
NEW_DEVICE_SHA12=edeb5f6fc4c4
TOKEN_CHANGED=true
REGISTRATION_ACK=PASS
CONNECTED_AT=2026-09-20 22:37:56
MESSAGE_LOOP_READY=true
```

No real buyer inbound occurred after this recovery during the observation window, so buyer E2E is pending.

## Zhulin / 701229202

The pre-cutoff 21:01:25 buyer message reached Native WS, MessageHandler and AutoReplyService with should_skip=false. Rule selection then logged that the account had no default reply for item 1085612069277. The account had six successful published items but only five default-reply rows. Existing formal xianyu_item_reply_config was used to add the missing item rule with the existing reply text/image. Readback confirmed default_reply_enabled=true, reply_once=false and reply_image_configured=true.

Earlier 20:01:25 and 20:02:23 buyer messages on item 1085607233517 completed image+text reply successfully. The 18:33 manual-pause case remains a separate historical message-specific event.

## Siya / 1835476245

Authority mapping: 1835476245 / （思雅）.

Pre-cutoff retained Native logs contain zero buyer-body messages for this account, while the user confirmed platform-visible buyer messages existed before the later manual reply. Token generation was fresh (2026-09-20 13:51:45, token_refresh_state=success), so this was not classified as a stale-Token case.

Target-only Native restart with token cache preserved:

```text
OLD_SOCKET_CONNECTED_AT=2026-09-20 13:51:46
NEW_SOCKET_ATTEMPT_AT=2026-09-20 22:35:24
REGISTRATION_ACK_AT=2026-09-20 22:35:25
CONNECTED_AT=2026-09-20 22:35:26
TOKEN_SHA12=90f251dc7b75_UNCHANGED
MESSAGE_LOOP_READY=true
INITIAL_FRAMES=113,299,5097
```

The four successful published items exactly match four enabled text/image-ready default-reply rows. No configuration gap was found. Real buyer E2E remains pending natural inbound.
