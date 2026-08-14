# Disabled Item Visibility and Business Capability UI Closeout

Date: 2026-08-14

## Execution Contract

User outcome: Disabled accounts keep historical catalog/session data and background read-only sync, but their items are excluded from normal item list/search/pagination/count/manual fetch; the account table exposes authoritative Auto Reply, Chat, and Publish business capability states instead of requiring users to infer from Browser Session internals.

Confirmed blocker: `ItemService.list_items()` and `list_items_paginated()` join `XYAccount` without the default `status == active` visibility condition, and the paginated count can avoid the account join entirely. The account API already has WebSocket connectivity, Session consumer readiness, and platform restriction facts, but the frontend renders these internal facts as separate columns instead of one Backend-owned three-capability view.

Smallest success test: Keep Scheduler disabled-account read-only sync unchanged; make normal catalog queries and manual fetch active-only at the Backend; reuse existing readiness/platform restriction facts to emit `business_capabilities`; make the Account UI show `账号状态 / 自动回复 / 在线聊天 / 发布商品`; validate natural disabled 8.19 samples retain DB history while normal visibility is zero, validate enabled account capability states independently, then run focused tests, repository verification, cumulative vendor-patch clean apply, production health, SSH-443 push, and remote-SHA equality.

Reuse decision: PATCH_UPSTREAM.
Duplicate-development risk: LOW if existing ItemService queries, Session consumer readiness, WebSocket connectivity, Chat readiness and platform restriction metadata remain the sole sources; no second state store or scheduler is permitted.
Rollback: revert only the active-account catalog visibility condition, business-capability serializer/UI mapping, and manual-fetch guard while leaving historical catalog rows and background read-only sync untouched.

## Safety boundary

- No product publish/relist/offline action.
- No message send.
- No QR scan or login bypass.
- No Cookie mutation for acceptance.
- No database schema changes.
- No new Session, Chat, WebSocket manager, Scheduler, Item Sync, or status database.

## Root cause and minimal implementation

- `ROOT_CAUSE_DISABLED_ITEMS_VISIBLE=CATALOG_QUERY_DOES_NOT_FILTER_DISABLED_ACCOUNT`.
- Normal catalog list/paginated/search/count now use the same `XYAccount.status == active` visibility condition in the existing `ItemService` query path.
- Historical `XYCatalogItem` rows are not deleted.
- Existing Scheduler `fetch_items` remains unchanged and continues read-only sync for non-deleted accounts, including disabled accounts.
- Manual page/full fetch rejects a specifically disabled account with `ACCOUNT_DISABLED`; all-account manual fetch only selects active accounts.
- The existing account details API now emits `business_capabilities.auto_reply/chat/publish` using existing WebSocket connectivity, Chat readiness, Session lifecycle and platform restriction facts. No new persistence store is added.
- Auto Reply does not inspect Browser Session QR state. Chat does not infer readiness from Browser Session. Publish keeps explicit disabled/restricted/platform-verification/QR/recovering/checking/ready precedence.
- Account UI main columns are `账号状态 / 自动回复 / 在线聊天 / 发布商品`; Browser Session and platform restriction remain diagnostic tooltip data.
- Account status changes dispatch a frontend invalidation event so Items refetches account options and item data without `window.location.reload()`.

## Focused and build verification

- Source `git diff --check`: PASS.
- Python compile for touched Backend paths: PASS.
- Focused tests: `68 passed`.
- Frontend source build: PASS.
- Current production-source frontend build (same CHG-0020 source lineage as the running `index-CHEc0Nuw.js` bundle): PASS.
- Cumulative Patch base: `64c245bc85ac56e34339fa056b0e291a16a3843b`.
- Cumulative Patch: `vendor/patches/xianyu-auto-reply/64c245-chg0018-disabled-item-visibility-business-capabilities.patch`.
- Patch SHA256: `2E00B55FB534C8F37A692D4C804CF92E7CD9C04213112D1B81A32C199E9D8AFF`.
- Patch file count: 31.
- Independent clean-base `git apply --check`: PASS.
- Independent apply: PASS.
- Focused tests after clean apply: `68 passed`.
- `CONTENT_EQUIVALENCE_IGNORING_CRLF=PASS`.
- `PATCH_BYTE_EQUIVALENCE=CRLF_DIFF_ONLY`.

## Production natural acceptance

- Production pre-fix normal catalog total: 30.
- Production active-account catalog history count: 17.
- Production post-fix normal visible total: 17.
- Production all catalog history count remains 30.
- Disabled `8.19` samples and historical item counts:
  - `2221384086829`: 7 history rows, 0 normal visible, 0 search-visible.
  - `1992416548`: 1 history row, 0 normal visible, 0 search-visible.
  - `2804730247`: 0 history rows, 0 normal visible, 0 search-visible.
  - `2221422775489`: 5 history rows, 0 normal visible, 0 search-visible.
- Manual full fetch for disabled sample `2221384086829`: `ACCOUNT_DISABLED`, with no platform item-fetch execution.
- Six enabled accounts were restored through the existing WebSocket start/reconnect path without QR or container restart; all six ended `AUTO_REPLY=ONLINE`.
- A real Chat read-only acceptance attempt through the existing `get_or_connect` path exposed a runtime side effect: expired IM Token handling merged a response Cookie field into the authoritative DB Cookie before Chat connection failed on platform validation. Therefore this evidence does **not** claim `ACCOUNT_COOKIE_MODIFIED_BY_TEST=false`; six account Cookie fingerprints changed during that probe. No Cookie contents are recorded here.
- The same real Chat probe returned Session-expiry evidence followed by `FAIL_SYS_USER_VALIDATE` platform-validation evidence for all six enabled accounts. No messages were sent. The verified existing Chat readiness recorder was synchronized into the Backend runtime and records this as `PLATFORM_VERIFICATION_REQUIRED` without using Browser QR as the source.
- Final enabled-account business state snapshot:
  - `2214313339860`: Auto Reply `ONLINE`; Chat `PLATFORM_VERIFICATION_REQUIRED`; Publish `CHECKING`.
  - `2219319284219`: Auto Reply `ONLINE`; Chat `PLATFORM_VERIFICATION_REQUIRED`; Publish `CHECKING`.
  - `2196106636`: Auto Reply `ONLINE`; Chat `PLATFORM_VERIFICATION_REQUIRED`; Publish `CHECKING`.
  - `2217936413500`: Auto Reply `ONLINE`; Chat `PLATFORM_VERIFICATION_REQUIRED`; Publish `CHECKING`.
  - `1034641456`: Auto Reply `ONLINE`; Chat `PLATFORM_VERIFICATION_REQUIRED`; Publish `CHECKING`.
  - `2858469041`: Auto Reply `ONLINE`; Chat `PLATFORM_VERIFICATION_REQUIRED`; Publish `CHECKING`.
- Disabled-account business capability sample: `DISABLED / DISABLED / DISABLED`.
- Frontend deployed from the existing CHG-0020 production-source lineage; served Account bundle contains the four main labels and capability tooltip fields, and served Items bundle contains the account-visibility invalidation/refetch event.
- Production health after deploy: Frontend 200, Backend 200, WebSocket 200, Scheduler 200.
- `ACTIVE_SCHEDULER_EXECUTORS=1`.
- Existing WebSocket `init=true` PID reaper remains enabled; WebSocket code/container was not redeployed for this task.
- Scheduler code/container was not redeployed for this task.
- MySQL/Redis were not restarted and schema was not changed.
- Runtime side-effect log check from 2026-08-14 11:04 local: `xy_publish_logs=0`, `xy_auto_reply_message_logs=0`.
- `REAL_PRODUCTS_PUBLISHED=0`, `REAL_MESSAGES_SENT=0`, `QR_SCANS_TRIGGERED_BY_TEST=0`.
- Root repository verification: `595 passed, 1 warning`; repository verification passed.

## Acceptance caveat

The item-visibility and three-capability product behavior is implemented and production-verified. However, the task-level requirement `ACCOUNT_COOKIE_MODIFIED_BY_TEST=false` was violated by the existing Chat `get_or_connect` acceptance path itself. The code did not add a new Chat system and the account-list API does not invoke this path automatically, but this acceptance side effect must remain explicitly recorded rather than being reported as false.
