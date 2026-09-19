# XIANYU Online Chat account-cache fix — 2026-09-19

## Incident

The Online Chat UI showed a conversation under account `2221422775489` (remark: 华为8.19可用) that did not belong to that account.

Authoritative runtime evidence proved the customer message belonged to account `2804730247` and item `1083167295431`. The native Auto Reply pipeline processed that message successfully:

```text
ACCOUNT_ID=2804730247
ITEM_ID=1083167295431
AUTO_REPLY_LOG_ID=660
process_status=success
decision_reason=reply_sent
reply_mode=text_image
send_status=success
```

Account `2221422775489` itself remained healthy:

```text
LOGIN_READY=true
ACCOUNT_ONLINE=true
running=true
is_connected=true
token_ready=true
platform_verification_required=false
human_qr_required=false
```

The issue was therefore a frontend display/cache ownership defect, not an Auto Reply failure.

## Root cause

The existing 2026-08-29 account-switch convergence patch already protects the visible UI from late asynchronous responses by account/request generation.

However, the production ChatNew bundle still had one follow-up gap:

- a fresh non-append conversation response updated visible React state;
- the per-account conversation cache was only refreshed later by the state-sync path when the visible list was non-empty;
- when authoritative server truth was an empty conversation list, an older stale cache entry could survive;
- switching back to that account could restore the stale rows before/around revalidation.

Backend forwarding was separately verified to remain account-scoped:

```text
ImSessionManager._ws_clients[account_id]
→ _forward_to_frontend()
→ only that account's registered frontend WebSockets
```

No cross-account backend broadcast was found.

## Fix

The production ChatNew bundle now treats every successful server conversation read as authoritative for that account's cache, including an empty list.

Non-append refresh:

```text
fresh server conversations
→ convsCacheRef.current[accountId] = fresh truth
→ setConversations(fresh truth)
```

Append refresh:

```text
existing visible rows + fresh page
→ convsCacheRef.current[accountId] = merged rows
→ setConversations(merged rows)
```

This preserves the existing request-generation guards and does not change message sending, Auto Reply, Publisher, Session, Token, QR, database schema, or backend WebSocket routing.

## Runtime activation

```text
BASE_FRONTEND_IMAGE=
xianyu-chg0018-frontend:full-cachebust-20260918-r2

ACTIVATED_FRONTEND_IMAGE=
xianyu-chg0018-frontend:chatnew-account-cachefix-20260919-r1

BASE_CHATNEW_SHA256=
7d58515be1e86a9370b8fcce91a08943e4c9df253838477f0eba4e92e0294843

FIXED_CHATNEW_SHA256=
5a55733f22d0b18b56b1c2ffb7a02a4c55a8e3d8cfab39adb952ae1ea28bc79b

FRONTEND_STATUS=running|healthy
ONLINE_CHAT_HTTP=200
CACHEFIX_CHUNK_HTTP=200
```

The image inherits the current production frontend and changes only:

1. one new ChatNew chunk with the cache-truth delta;
2. the existing import-map target for ChatNew.

All other frontend assets remain inherited unchanged.

## Reproducible persistence

The exact production hotfix is persisted as a hash-locked transformer:

```text
scripts/patch_chatnew_account_cachefix_20260919.py
```

It fails closed unless the input bundle SHA matches the known production preimage and verifies the exact fixed output SHA.

Regression tests:

```text
tests/unit/test_chatnew_account_cachefix_20260919.py
```

The older artifact `online-chat-account-switch-convergence-20260829.patch` is not rewritten. This fix is a follow-up to that locked historical patch.

No Cookie, Token, Authorization header, password, QR payload, buyer identifier, or customer message content is stored in this document.
