# XIANYU — Desktop Migration Closure 2026-09-10

Status: `MIGRATION_COMPLETE`
Authority: post-cutover migration closure + current machine-role handoff

This file supersedes the machine-role / cutover status in `docs/DESKTOP_RECOVERY_HANDOFF_20260910.md`. The older recovery handoff remains historical evidence for reconstruction and TEST gates.

## 1. Final machine roles

```text
XIANYU_DESKTOP_MIGRATION_COMPLETE=true

DESKTOP_HOSTNAME=PC-20250528MGDP
DESKTOP_ROLE=PRIMARY
DESKTOP_PRODUCTION=true

LAPTOP_CURRENT_WINDOWS_HOSTNAME=WIN-PQGV23OBQET
LAPTOP_HISTORICAL_HOST_ID=HUAWEI-LAPTOP
LAPTOP_ROLE=STANDBY
LAPTOP_PRODUCTION=false

PRODUCTION_DOUBLE_RUN=false
LAPTOP_STANDBY_REACTIVATION_RISK=false
LAPTOP_ROLLBACK_CAPABILITY_PRESERVED=true
```

`WIN-PQGV23OBQET` and historical `HUAWEI-LAPTOP` are the same original Huawei laptop. Do not rename Windows to satisfy the historical logical host id.

From this closure onward, the desktop database is the current production business authority. The laptop database is only the last-cutover standby snapshot and must never be used to overwrite newer desktop production state unless a separate rollback decision is explicitly made.

```text
DESKTOP_DB_CURRENT_PRODUCTION_AUTHORITY=true
LAPTOP_DB_ROLE=STANDBY_LAST_CUTOVER_SNAPSHOT
```

## 2. Recovery / reconstruction closure

Immutable-image Source Authority V2 and byte-preserving recovery were completed before cutover.

```text
BACKEND_V2_SOURCE_FILES=357
BACKEND_V2_TREE_SHA256=24640d4056e9e099a4c7e6d6b106083ae397fc59b4511086e5da602bcc437bed

WEBSOCKET_V2_SOURCE_FILES=251
WEBSOCKET_V2_TREE_SHA256=5b242d9adcbb7073bd9a371f605a124193f1d1448b501a3c2ec15fb02ece3494

SCHEDULER_V2_SOURCE_FILES=231
SCHEDULER_V2_TREE_SHA256=7560296587d8a4446da8fd24a6ba968944909abd64c5c94aeb5cbccc2814cc91

FRONTEND_CONTEXT_FILE_COUNT=452
FRONTEND_CONTEXT_TREE_SHA256=247dda4b8b4db9aa78d1eded11f6d9aed8088a9a5b12fa863f88f1b3d3bcc961
FRONTEND_OCI_REVISION=5dd103e096cb921e979ae1a3923febe5c357fff8
```

Backend runtime dependency recovery also closed the missing OpenCV dependency using the exact historical runtime identity:

```text
PYTHON_VERSION=3.11.15
CV2_VERSION=5.0.0
OPENCV_DISTRIBUTION=opencv-python-headless
OPENCV_VERSION=5.0.0.93
BACKEND_RECOVERY_IMAGE_ID=sha256:5239e35c16e1c73b86c26277ab409dcb8219bb01fdeb6995d63539fb8500da3d
BACKEND_SOURCE_IDENTITY_V2_STILL_MATCH=true
```

Do not reopen Authority V2, byte supplement, cv2 recovery or image reconstruction without new direct runtime evidence.

## 3. TEST gate closure

Before production cutover, the desktop side-effect-disabled TEST Runtime passed the required gates.

```text
DESKTOP_TEST_MODE=PASS
DESKTOP_READY_FOR_CUTOVER=true

XIANYU_MYSQL=PASS
XIANYU_MYSQL_TABLE_COUNT=63
XIANYU_REDIS=PASS
XIANYU_BACKEND=PASS
XIANYU_FRONTEND=PASS
XIANYU_SESSION=PASS
XIANYU_PROFILE=PASS

XIANYU_DEFAULT_ACCOUNT=PASS
XIANYU_ONLINE_CHAT=PASS
XIANYU_AUTO_REPLY=PASS_TEST_TECHNICAL
XIANYU_PUBLISH=PASS_DRY_RUN
XIANYU_WEBSOCKET_TECHNICAL=PASS
XIANYU_SCHEDULER_TECHNICAL=PASS
```

Publisher dry-run used the real current publisher path with an in-memory TEST fixture and a fail-closed final MTOP submit guard. No platform submit occurred.

```text
PUBLISH_REQUEST_PREPARATION=PASS
FINAL_MTOP_SUBMIT_BOUNDARY_REACHED=true
FINAL_MTOP_SUBMIT_GUARD=PASS
PLATFORM_SUBMIT_COUNT=0
REAL_PRODUCT_PUBLISHED=false
```

## 4. Order authority reconciliation and final delta

The first cutover attempt correctly rolled back because desktop order business state was stale. Order authority was then proven and reconciled before the successful final cutover.

```text
ORDER_PRIMARY_TABLE=xy_orders
ORDER_PRIMARY_KEY=id
ORDER_PLATFORM_ORDER_ID_FIELD=order_no
ORDER_STATUS_FIELD=status
ORDER_UPDATED_AT_FIELD=updated_at
ORDER_BUSINESS_STATE_CLOSURE_PROVEN=true
REDIS_ORDER_AUTHORITY=false
```

The pre-sync and final-delta process used consistent snapshots, canonical hashes, per-row expected-before checks, transactions and rollback evidence. The final successful cutover freeze produced exact laptop/desktop business-state equality before desktop writers were started.

```text
FINAL2_LAPTOP_AUTHORITY_TIMESTAMP=2026-09-10 20:37:32.338326
FINAL2_LAPTOP_ORDER_TOTAL=12
FINAL2_DESKTOP_ORDER_TOTAL_BEFORE=12
FINAL2_ORDER_ID_MISSING_ON_DESKTOP=0
FINAL2_ORDER_ID_EXTRA_ON_DESKTOP=0
FINAL2_ORDER_ROWS_DIFFERENT=3
FINAL2_DELTA_ROW_COUNT=3
FINAL2_DELTA_OPTIMISTIC_CHECK=PASS
FINAL2_DELTA_TRANSACTION_COMMIT=PASS
FINAL2_ORDER_TOTAL_MATCH=true
FINAL2_ORDER_IDS_MATCH=true
FINAL2_ORDER_BUSINESS_STATE_MATCH=true
FINAL2_ORDER_RELATED_AUTHORITY_MATCH=true
FINAL2_LAPTOP_ORDER_BUSINESS_HASH=af3ee09817c17791a36ca16d30fe94b1ba8f2703484a1ec7fdf706c3833a58a9
FINAL2_DESKTOP_ORDER_BUSINESS_HASH=af3ee09817c17791a36ca16d30fe94b1ba8f2703484a1ec7fdf706c3833a58a9
```

After cutover, do not require the desktop and laptop order hashes to remain equal. New production activity belongs to the desktop PRIMARY.

Latest post-cutover desktop baseline captured during final acceptance:

```text
POST_CUTOVER_ORDER_TOTAL=12
POST_CUTOVER_ORDER_STATUS_AGG=cancelled=2,completed=4,refunded=4,refunding=2
POST_CUTOVER_ORDER_BUSINESS_HASH=9c649c5c8294fe1f574e5b7cb6ef8b36e4384b2e5492d4970e74c739bd47f200
```

This hash is a timestamped baseline, not a permanent expected value.

## 5. Scheduler production network closure

A prior cutover attempt rolled back because the desktop Scheduler container had only an internal Docker network and therefore no egress/DNS path to `h5api.m.goofish.com`.

The runtime-only fix preserved the accepted Scheduler image/source and attached an existing egress-capable bridge in addition to the internal XIANYU network.

```text
DESKTOP_SCHEDULER_EGRESS_NETWORK_RECOVERY=PASS
NETWORK_CHANGE_TYPE=MULTI_NETWORK_ATTACH_EXISTING_EGRESS_BRIDGE
MULTI_NETWORK_ATTACH=true
ACCEPTED_SCHEDULER_IMAGE_CHANGED=false
SCHEDULER_SOURCE_CHANGED=false

SCHEDULER_INTERNAL_CONNECTIVITY=PASS
SCHEDULER_EGRESS_CONNECTIVITY=PASS
DNS_RESOLVE_H5API_M_GOOFISH_COM=PASS
TCP_443_H5API_M_GOOFISH_COM=PASS
TLS_HANDSHAKE_H5API_M_GOOFISH_COM=PASS
```

Do not regress the desktop production Scheduler to an internal-only network.

## 6. Final production acceptance

The final production cutover and post-cutover runtime acceptance passed.

```text
XIANYU_FINAL_PRODUCTION_CUTOVER=PASS
XIANYU_DESKTOP_MIGRATION_COMPLETE=true

DESKTOP_BACKEND=PASS
DESKTOP_FRONTEND=PASS
DESKTOP_MYSQL=PASS
DESKTOP_MYSQL_TABLE_COUNT=63
DESKTOP_REDIS=PASS
DESKTOP_SESSION=PASS
DESKTOP_PROFILE=PASS

DESKTOP_ACCOUNT_TOTAL=13
DESKTOP_ACCOUNT_ENABLED=9
DESKTOP_ACCOUNT_LOGIN_READY=9
DESKTOP_ACCOUNT_CHAT_CONNECTED=7

DESKTOP_DEFAULT_ACCOUNT_ID=2196106636
DESKTOP_DEFAULT_ACCOUNT_LOGIN_READY=true
DESKTOP_DEFAULT_ACCOUNT_CHAT_READY=PASS

DESKTOP_WEBSOCKET_PRODUCTION=PASS
DESKTOP_AUTO_REPLY_PRODUCTION=PASS
DESKTOP_PUBLISH_RUNTIME_READY=PASS
DESKTOP_SCHEDULER_PRODUCTION=PASS

XIANYU_WEB_UI=http://127.0.0.1:19000/
XIANYU_ACCOUNTS_UI=http://127.0.0.1:19000/accounts
XIANYU_ONLINE_CHAT_UI=http://127.0.0.1:19000/online-chat-new
XIANYU_WEB_UI_VERIFIED_20260911=true

JOB_REGISTRY_COUNT=21
EXPECTED_PRODUCTION_JOB_SET_MATCH=true
UNEXPECTED_JOB_ENABLED_COUNT=0
UNEXPECTED_CATCHUP_JOB_COUNT=0
DUPLICATE_ORDER_PROCESSING_DETECTED=false
DUPLICATE_FULFILLMENT_DETECTED=false
```

The current desktop Web UI routes above were re-verified on 2026-09-11 and each returned HTTP 200. They are loopback-only desktop URLs unless a separate LAN/public exposure is explicitly configured.

No synthetic business side effects were used for cutover acceptance:

```text
CUTOVER_TEST_PRODUCT_PUBLISHED=false
ACTIVE_TEST_MESSAGE_SENT=false
REAL_PAYMENT=false
UNEXPECTED_PRODUCT_PUBLISHED=false
UNEXPECTED_CUSTOMER_MESSAGE_SENT=false
UNEXPECTED_ORDER_MUTATION=false
UNEXPECTED_PAYMENT=false
UNEXPECTED_AUTO_DELIVERY=false
```

## 7. Auto Reply / Chat / Publish current interpretation

At the post-cutover snapshot:

```text
ACCOUNT_TOTAL=13
ACCOUNT_ENABLED=9
ACCOUNT_LOGIN_READY=9
ACCOUNT_CHAT_CONNECTED=7
```

The production Auto Reply service itself passed. `CHAT_CONNECTED` is a real-time connection count and is not the same thing as `LOGIN_READY` or `AUTO_REPLY_CONFIGURED`; do not infer an exact per-account Auto Reply-ready count from the aggregate service PASS alone. Read current runtime and cross-match account state before reporting an exact number.

The production Publisher runtime is ready. The migration acceptance intentionally did not create a real test item; normal future publishing should use the formal XIANYU Publisher path and authoritative publish-status readback.

## 8. Non-migration account maintenance

The following account Session reauthentication was reported as pending after migration closure:

```text
2217936413500
2221501265279
```

Treat this as normal account/session maintenance, not as a migration blocker.

```text
ACCOUNT_SESSION_MAINTENANCE_PENDING=true
MIGRATION_BLOCKED_BY_ACCOUNT_REAUTH=false
```

Do not clear cookies, force QR login or change account enablement merely because this handoff lists the maintenance item. Re-read current authoritative account/session state first.

## 9. Production safety rules after migration

```text
ONE_PRODUCTION_PRIMARY_ONLY=true
CURRENT_XIANYU_PRIMARY=PC-20250528MGDP
CURRENT_XIANYU_STANDBY=WIN-PQGV23OBQET
PRODUCTION_DOUBLE_RUN=false
UNKNOWN_NEVER_BLIND_RETRY=true
```

The laptop must remain rollback-capable but its XIANYU production Scheduler/WebSocket/Auto Reply/order writers must not auto-reactivate while the desktop is PRIMARY.

If a future rollback is explicitly authorized, first stop and prove desktop production writers are inactive before restoring laptop production writers.

## 10. Git / local checkout note

A desktop-local docs commit `2f6618b8a5e46ed555df502b69420643af76438f` was created while the desktop Git transport was unavailable and was not pushed at that time.

This GitHub closure was written directly to the current remote branch after verifying the then-current remote main. Therefore the old local commit must NOT be blindly pushed later. The desktop checkout must first fetch the new remote main and safely reconcile/preserve any useful local-only evidence. No force push, no reset that discards unknown work, and no secrets/recovery packages in GitHub.

## 11. Current source of truth order

For future execution:

```text
current platform / current production Runtime
-> current XIANYU repository + current production handoff
-> this migration closure
-> older recovery handoff / migration packages
-> old chat summaries
```

The migration/recovery track is closed. Future XIANYU work should proceed as normal production operations or explicitly scoped account maintenance, not as another desktop recovery.
