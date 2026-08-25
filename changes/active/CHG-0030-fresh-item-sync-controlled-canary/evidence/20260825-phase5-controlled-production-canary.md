# CHG-0030 Phase 5 controlled production canary evidence

Date: 2026-08-25

Authorization:

```text
ONE_CONTROLLED_FRESH_ITEM_SYNC_CANARY=APPROVED
MAX_ITEM_SYNC_INVOCATIONS=1
SELECTED_MASKED_ACCOUNT=22*********60
```

No browser/UI/CDP, publish/edit/offline/delete, message send, auto-reply enablement, QR, reconnect, account mutation, config change, service restart, or second owner was authorized or performed.

## Final pre-invocation gate

Timestamp:

```text
2026-08-25T03:42:11.3097869Z
```

Runtime:

```text
Backend image=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2
Backend image_id=sha256:f877b7273b2f4e23ff5f0dd5e599dbf860c1e83bc801fca8a26bea815cae4573
Backend health=HTTP_200 RestartCount=0
WebSocket health=HTTP_200 RestartCount=0 image_id=sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256
Scheduler health=HTTP_200 RestartCount=0 image_id=sha256:ab70f051e962a3138103de969e6976e13c923da86d9222eabf2b9223394331e8
Frontend health=HTTP_200 RestartCount=0 image_id=sha256:71cfebe276e3d5ca84db01cd9ed1e6b70211dedf75cbe1b3da210b19e19da416
```

Selected-account capability:

```text
MASKED_ACCOUNT=22*********60
STATE=READY
ITEM_SYNC_ELIGIBLE=true
FAIL_CLOSED=false
DISABLED=false
CHECKING_STATE=REAL_BROWSER_LOGIN_READY
CHECKING_ACTIVE=false
PLATFORM_VERIFICATION_SOURCE=none
PLATFORM_VERIFICATION_EVIDENCE_TYPE=NONE
PLATFORM_VERIFICATION_REQUIRED=false
SESSION_COOKIE_LINEAGE=MATCH
TOKEN_READY=true
```

`PLATFORM_VERIFICATION_SOURCE=none` is accepted only because the classifier returned authoritative `PLATFORM_VERIFICATION_EVIDENCE_TYPE=NONE` and `PLATFORM_VERIFICATION_REQUIRED=false`.

Catalog/lock baseline:

```text
XY_CATALOG_ITEMS_ROWS_BEFORE=20
DUPLICATE_GROUPS_BEFORE=0
DUPLICATE_ROWS_BEFORE=0
REDIS_LOCK_item_sync_ACCOUNT_EXISTS_BEFORE=false
```

Pre-invocation marker/safety baseline since `2026-08-25T03:42:11.3097869Z`:

```text
CHG0030_ITEM_SYNC_OPERATION_ACCEPTED=0
CHG0030_ITEM_SYNC_TERMINAL_READBACK=0
GET_ALL_FROM_ACCOUNT=0
FETCH_ALL_ITEMS_FROM_ACCOUNT=0
PUBLISH_ITEM=0
SEND_MESSAGE=0
QR_LOGIN=0
RECONNECT=0
BATCH_OFFLINE=0
BATCH_DELETE=0
ACCOUNT_MUTATION=0
PLAYWRIGHT=0
BROWSER=0
```

Gate result:

```text
FINAL_PRE_INVOCATION_GATE=PASS
```

## One invocation

Invocation start/end:

```text
STARTED_UTC=2026-08-25T03:42:41.3373867Z
COMPLETED_UTC=2026-08-25T03:42:44.1873658Z
```

Adapter path:

```text
COMPANY_MCP_TOOL=xianyu_item_sync
BACKEND_ROUTE=/api/v1/items/get-all-from-account?no_auth_recovery=true
OWNER=ItemService.fetch_all_items_from_account
MCP_INVOCATION_COUNT=1
PAGE_SIZE_SUPPLIED=20
MAX_PAGES_SUPPLIED=OMITTED
```

The invocation argument omitted `max_pages`. The current COMPANY adapter defaulted `max_pages` to `20` before calling Backend; this did not cap the selected account incompletely because the terminal Backend marker records `full_active_list_confirmed=true`.

Sanitized immediate adapter result:

```text
ok=true
status=SUCCESS
account_id=22*********60
message=获取到 20 个商品
total=20
saved_count=20
pages=1
diagnostics.backend_path=/api/v1/items/get-all-from-account
diagnostics.source=XIANYU_ItemService.fetch_all_items_from_account
diagnostics.credentials_exposed=false
```

No retry was attempted.

## Backend marker recovery

Exact marker filtering since invocation start:

```text
CHG0030_ITEM_SYNC_OPERATION_ACCEPTED_COUNT=1
CHG0030_ITEM_SYNC_TERMINAL_READBACK_COUNT=1
```

Recovered operation identity:

```text
OPERATION_ID=item_sync_e7ca45174a64408e80b8d72a95d2f37f
REQUEST_ID=item_sync_e7ca45174a64408e80b8d72a95d2f37f
MASKED_ACCOUNT=22*********60
```

Accepted marker facts:

```text
OWNER=ItemService.fetch_all_items_from_account
PAGE_SIZE=20
MAX_PAGES=20
RETRY_ALLOWED=false
```

Terminal marker facts:

```text
TERMINAL_STATE=SUCCESS
DURABLE_CHECKED=true
ACCOUNT_ROW_COUNT=20
RESPONSE_TOTAL_COUNT=20
MATCHED_RESPONSE_ITEM_COUNT=20
DUPLICATE_COUNT=0
FAILURE_REASON=None
SKIPPED=false
FULL_ACTIVE_LIST_CONFIRMED=true
RETRY_ALLOWED=false
```

Durable readback contract:

```text
SOURCE=xy_catalog_items
QUERY_SUCCESS=true
CHECKED=true
RECONCILED=true
UNIQUE_CONTRACT=account_id,item_id
```

The deployed r2 terminal log records `durable_checked=true` plus the measured account, response, matched-item, duplicate, skipped, and full-list facts. In the r2 route implementation, that terminal state is reachable only after `_read_item_sync_durable_state` completes the read-only `xy_catalog_items` queries successfully and returns `checked=true`/`reconciled=true` from `source=xy_catalog_items`.

## Post-invocation readback

Selected account catalog after:

```text
XY_CATALOG_ITEMS_ROWS_AFTER=20
DUPLICATE_GROUPS_AFTER=0
DUPLICATE_ROWS_AFTER=0
REDIS_LOCK_item_sync_ACCOUNT_EXISTS_AFTER=false
```

Service health/restarts after:

```text
Backend health=HTTP_200 RestartCount=0 image_id=sha256:f877b7273b2f4e23ff5f0dd5e599dbf860c1e83bc801fca8a26bea815cae4573
WebSocket health=HTTP_200 RestartCount=0 image_id=sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256
Scheduler health=HTTP_200 RestartCount=0 image_id=sha256:ab70f051e962a3138103de969e6976e13c923da86d9222eabf2b9223394331e8
Frontend health=HTTP_200 RestartCount=0 image_id=sha256:71cfebe276e3d5ca84db01cd9ed1e6b70211dedf75cbe1b3da210b19e19da416
```

Post-invocation safety and targeted regression signals since invocation start:

```text
CHG0030_ITEM_SYNC_OPERATION_ACCEPTED=1
CHG0030_ITEM_SYNC_TERMINAL_READBACK=1
PUBLISH_ITEM=0
SEND_MESSAGE=0
AUTO_REPLY=0
QR_LOGIN=0
RECONNECT=0
BATCH_OFFLINE=0
BATCH_DELETE=0
ACCOUNT_MUTATION=0
PLAYWRIGHT=0
CDP=0
BROWSER=0
AUTO_REPLY_ENABLE=0
```

Online-chat regression signal: WebSocket health remained HTTP 200 and RestartCount remained 0.

Publish regression signal: no publish marker was present and Backend health/RestartCount remained stable.

Auto-reply/message regression signal: no auto-reply or send-message marker was present and WebSocket health/RestartCount remained stable.

## Result

```text
ONE_CONTROLLED_FRESH_ITEM_SYNC_CANARY=PASS
ITEM_SYNC_INVOCATION_COUNT=1
TERMINAL_SUCCESS=true
DURABLE_TRUTH_CONFIRMED=true
DUPLICATE_COUNT=0
EXCLUDED_SIDE_EFFECT_COUNTERS_ZERO=true
NO_RETRY_CONFIRMED=true
```
