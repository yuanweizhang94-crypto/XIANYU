# CHG-0018 Disabled Item and Session Convergence Evidence

Date: 2026-08-14
Scope: read-only item status convergence, existing Session lifecycle convergence, disabled-account business isolation, existing WebSocket recovery, and production UI status visibility.
Reuse decision: PATCH_UPSTREAM

## Execution contract

User outcome: disabled accounts continue read-only item/session status synchronization; pending item status receives one bounded authoritative retry after Session convergence; auto-reply disconnection does not imply QR; only the authoritative Session lifecycle may classify HUMAN_QR_REQUIRED.

Confirmed blockers:

1. The existing `fetch_items` scheduler excluded disabled/inactive/suspended accounts, so disabling business activity also froze their local item status forever.
2. `NOT_IN_ACTIVE_LIST` detail probing could stop at `session_or_verification_required` without first converging the existing Session lifecycle and retrying once.
3. The production `api_cookie_renew` scheduler had drifted from the existing WebSocket Session lifecycle and still contained legacy behavior that could re-enable a disabled account after renewal.
4. Scheduler Session maintenance used the generic short-timeout/retry HTTP client. A browser lifecycle request can legitimately wait for the canonical browser slot longer than that timeout; client retries created overlapping server-side maintenance and browser/Profile contention.
5. When an authoritative item classification was intentionally preserved, the UI-facing metadata kept the generic `not_seen_after_complete_active_list_sync` reason instead of the real Session/platform blocker.

Smallest success test: reuse the existing `fetch_items`, `ItemService`, WebSocket `/internal/session/health` and `/internal/session/maintain`, canonical Profile, DB Cookie, browser lock, existing WebSocket task manager, and sole Scheduler; make disabled accounts read-only participants without business restart; bound Session convergence and item retry; expose the final reason/source/check time; verify natural production samples with zero platform write actions.

## Root cause

`ROOT_CAUSE_DISABLED_ACCOUNT_ITEMS_STALE=DISABLED_ACCOUNT_SKIPPED_BY_READ_ONLY_ITEM_SYNC`

The stale disabled-account product display was not a frontend cache root cause. The Backend catalog itself was stale because the only scheduled item-sync owner selected business-enabled accounts only. The frontend manual status flow already re-requests Backend data and does not rely on `window.location.reload()`.

The long-running pending-item root cause was a combination of missing Session convergence before the bounded authoritative retry and a production Scheduler drift that used a short-timeout/retry path for long-running Session maintenance.

Runtime evidence of the retry/maintenance contention before cleanup:

- WebSocket remained HTTP 200 but reached approximately 1.26 GiB memory and 20,049 PIDs.
- The existing WebSocket container was stopped and started once, without changing its image or creating a second WebSocket manager, solely to clear legacy in-flight maintenance processes.
- Immediately after that operational cleanup, the same WebSocket container was HTTP 200 with 12 PIDs and approximately 180.7 MiB memory.
- The repaired Scheduler now performs one bounded Session request with no generic HTTP retry: active maintain timeout 420 seconds; disabled read-only health timeout 180 seconds.

## Reused existing ownership

No parallel execution system was added.

- Item synchronization owner: existing `fetch_items` Scheduler task.
- Item state owner: existing `ItemService` / `ItemInfoManager` / catalog metadata.
- Session lifecycle owner: existing WebSocket `/internal/session/health` and `/internal/session/maintain`.
- Scheduled Session owner: existing `api_cookie_renew` task.
- Canonical browser state: existing persistent Profile and browser lock.
- Cookie authority: existing authoritative DB Cookie.
- Auto-reply connection owner: existing WebSocket account task manager.
- Publish owner: existing PublishExecutor/Publisher path with a new fail-closed disabled-account guard before Publisher execution.

`NEW_SCHEDULER_CREATED=false`
`NEW_ITEM_MONITOR_CREATED=false`
`NEW_SESSION_SYSTEM_CREATED=false`
`NEW_PROFILE_SYSTEM_CREATED=false`
`SECOND_PUBLISHER_CREATED=false`
`MYSQL_SCHEMA_CHANGED=false`

## Final semantics

Disabled account:

- Business side effects remain disabled.
- Read-only item sync is allowed through the existing `fetch_items` task.
- Read-only Session health is allowed through the existing hourly `api_cookie_renew` owner.
- Disabled Session health uses `allow_renew=false` and never starts auto-reply.
- Real publish is fail-closed with `ACCOUNT_BUSINESS_DISABLED` before the Publisher.
- Historical catalog records are retained; they are not deleted merely because the account or platform item is inactive.

Enabled account:

- Existing Session lifecycle may maintain/renew the Session.
- If `REAL_BROWSER_LOGIN_READY`, the existing WebSocket task status is checked and the existing start endpoint may be used when the account is still active and disconnected.
- `AUTO_REPLY` readiness remains independent from Browser Session readiness.

QR/platform semantics:

- WebSocket disconnected does not equal `HUMAN_QR_REQUIRED`.
- `SESSION_CHECK_PENDING`, Cookie presence, Profile presence, temporary network failure, or token/cache failure do not equal `HUMAN_QR_REQUIRED`.
- `PLATFORM_VERIFICATION_REQUIRED` remains distinct from `HUMAN_QR_REQUIRED`.
- Only the existing authoritative Session lifecycle may classify `HUMAN_QR_REQUIRED`.

Pending-item semantics:

- Complete official active-list success is required before missing items are reconciled.
- Partial/failed sync does not mass-mark missing items.
- Missing from active list remains `NOT_IN_ACTIVE_LIST`; it is never automatically inferred as platform delisted.
- One bounded Session convergence and one authoritative retry are permitted.
- If the previous item status must be preserved, `platform_status_reason`, `platform_status_source`, and `last_status_check_at` are still persisted so the UI explains the blocker.

## Scheduled Session owner

Production task configuration observed:

- `api_cookie_renew`: enabled, interval 3600 seconds.
- `cookies_refresh`: disabled.
- `login_renew`: disabled.
- `token_renewal`: disabled.
- `fetch_items`: enabled, interval 1200 seconds.

`SESSION_MAINTENANCE_OWNER=api_cookie_renew`
`SESSION_MAINTENANCE_INTERVAL=3600s`

The repaired `api_cookie_renew` task remains the sole scheduled Session owner. It processes all non-deleted accounts once per configured cycle:

- active account -> existing `/internal/session/maintain`, bounded 420 seconds, no generic retry;
- disabled account -> existing `/internal/session/health`, bounded 180 seconds, no renewal and no auto-reply start.

A Cookie change can legitimately set a fresh `SESSION_CHECK_PENDING` state. That is a request for the next bounded check, not a permanent QR classification. The same hourly owner converges it again.

## Production natural sample A: disabled account

Sample account: `2221422775489`

- `ACCOUNT_ENABLED=false`
- `ACCOUNT_ONLINE=false`
- local historical items before: 5
- official active-item count: 0
- complete official active-list result: true
- active items after: 0
- `NOT_IN_ACTIVE_LIST` after: 5
- confirmed OFFLINE: 0
- confirmed SOLD: 0
- confirmed PLATFORM_DELISTED: 0
- WebSocket task: `running=false`, `connected=false`
- read-only sync executed successfully
- real platform write actions: 0

All five historical items remain visible as `NOT_IN_ACTIVE_LIST` rather than falsely remaining ACTIVE. Their latest authoritative-blocker metadata is:

- reason: `human_qr_required_for_authoritative_item_check`
- source: `session_maintenance`
- `last_status_check_at`: populated

The official active list proves that none of the five is currently active. Finer OFFLINE/SOLD/DELETED/PLATFORM_DELISTED classification is intentionally not guessed because the authoritative browser detail path currently requires the user to restore the browser login state.

The disabled account's Session health independently converged to `HUMAN_QR_REQUIRED` with the canonical Profile present, but the disabled business connection remained stopped.

## Production natural sample B: enabled account with pending item

Sample account: `2196106636`

Before final sync:

- total local items: 5
- ACTIVE: 4
- `NOT_IN_ACTIVE_LIST`: 1

Final read-only sync:

- official active-item count: 4
- complete official active-list result: true
- pending item checked authoritatively: 1
- finer authoritative statuses confirmed: 0
- pending after: 1

The remaining item is now stored as:

- status: `NOT_IN_ACTIVE_LIST`
- reason: `human_qr_required_for_authoritative_item_check`
- source: `session_maintenance`
- `last_status_check_at`: populated

The Session lifecycle used the existing DB Cookie and canonical persistent Profile. The browser health result for this natural account was:

- state: `HUMAN_QR_REQUIRED`
- `REAL_BROWSER_LOGIN_READY=false`
- `HUMAN_QR_REQUIRED=true`
- `PLATFORM_VERIFICATION_REQUIRED=false`
- `PROFILE_PRESENT=true`
- reason: `LOGIN_OR_QR_UI_VISIBLE`

Therefore the system correctly preserves `NOT_IN_ACTIVE_LIST` rather than inventing OFFLINE/SOLD/PLATFORM_DELISTED.

## Production natural sample C: auto-reply offline recovery

Sample account: `2196106636`

Before runtime cleanup, the existing WebSocket task reported `running=true` but `connected=false` while legacy overlapping Session maintenance had created severe process pressure.

After clearing the legacy in-flight WebSocket processes by restarting the same existing WebSocket container, the existing WebSocket manager restored the enabled account connection without a QR scan:

- `running=true`
- `connected=true`
- read-only account status: `ACCOUNT_ENABLED=true`, `ACCOUNT_ONLINE=true`, `LOGIN_READY=true`

At the same time, the independent Browser Session health was `HUMAN_QR_REQUIRED`. This is direct natural evidence that auto-reply/WebSocket connectivity and Browser Session QR state are separate capabilities.

Disabled accounts remained `running=false`, `connected=false` even when their read-only Browser Session health was `REAL_BROWSER_LOGIN_READY`.

## PENDING convergence evidence

Historical pending/unchecked natural accounts were checked through the existing read-only browser-health path. Observed converged outcomes included:

- disabled `1992416548` -> `REAL_BROWSER_LOGIN_READY`
- disabled `2804730247` -> `REAL_BROWSER_LOGIN_READY`
- disabled `2221384086829` -> `REAL_BROWSER_LOGIN_READY`
- disabled `1951966327` -> `REAL_BROWSER_LOGIN_READY`
- active natural accounts also converged to explicit `HUMAN_QR_REQUIRED` when official login/QR UI was visible.

After those checks, a small number of active accounts re-entered fresh `SESSION_CHECK_PENDING` because their Cookie changed after/during health; one explicitly recorded `COOKIE_CHANGED_DURING_HEALTH_CHECK`. This is expected lifecycle behavior and is now bounded by the same hourly owner instead of remaining permanently unchecked.

## Frontend/runtime verification

The production frontend keeps the existing CHG-0020 main asset and overlays only the affected route chunks.

Live route chunks were verified to contain:

- item status tooltip: reason, source, last check time;
- disabled account auto-reply display: `停用`;
- disabled-account explanation that read-only Session/item checks continue.

Manual item status flows already re-fetch Backend item/account data; `window.location.reload()` is not used as the repair.

Final observed service health:

- Frontend: HTTP 200
- Backend: HTTP 200
- WebSocket: HTTP 200
- Scheduler: HTTP 200
- active Scheduler executors: 1

Deployment scope:

- Backend changed: yes
- Scheduler changed: yes
- Frontend changed: yes
- WebSocket source/image changed: no
- WebSocket operational restart: yes, one existing container only, to clear the legacy maintenance process backlog
- MySQL changed: no
- Redis changed: no

Final production images:

- Backend: `xianyu-chg0018-backend-web:item-session-convergence-20260814-r3`
- Scheduler: `xianyu-chg0018-scheduler:item-session-convergence-20260814-r3`
- Frontend: `xianyu-chg0020-frontend:item-session-convergence-20260814`
- WebSocket: existing `xianyu-chg0018-websocket:session-lifecycle-20260812-r2`

## Safety and side effects

Since the beginning of this production repair window:

- `xy_publish_logs=0`
- `xy_auto_reply_message_logs=0`

No test created or modified a platform item and no test sent a message.

- `REAL_PRODUCTS_PUBLISHED=0`
- `REAL_PRODUCTS_RELISTED=0`
- `REAL_PRODUCTS_OFFLINED_BY_TEST=0`
- `REAL_MESSAGES_SENT=0`
- `APPEALS_SUBMITTED=0`
- `QR_SCANS_TRIGGERED_BY_TEST=0`

No Cookie, Token, Authorization value, password, API key, private key, browser Profile content, or customer-message content is included in this evidence.

## Validation

Focused production-change tests on the implementation/clean patch state:

- `tests/test_chg0018_disabled_item_session_convergence.py`
- `tests/test_chg0018_authoritative_platform_status.py`
- `tests/test_chg0018_chat_auth_convergence.py`
- `tests/test_chg0018_consumer_readiness.py`
- result: `35 passed`

Other validation:

- targeted Python `py_compile`: PASS
- frontend `npm --prefix frontend run build`: PASS
- cumulative source `git diff --check`: PASS
- root `python scripts/verify_repository.py`: repository verification passed, `595 passed`, 1 warning

## Vendor patch

Patch base:

`64c245bc85ac56e34339fa056b0e291a16a3843b`

Cumulative vendor patch:

`vendor/patches/xianyu-auto-reply/64c245-chg0018-item-session-convergence.patch`

SHA256:

`951205B029CCFC73C4AFCFE04A5150F610F7391E3BC5C86C0B0A8A965AD08EB3`

Validation:

- `PATCH_CLEAN_APPLY=PASS`
- clean-base focused tests after patch apply: `35 passed`
- clean-base targeted `py_compile`: PASS
- `CONTENT_EQUIVALENCE_IGNORING_CRLF=PASS`
- `PATCH_BYTE_EQUIVALENCE=CRLF_DIFF_ONLY`
- exact-byte differences after apply were limited to two test files because of Windows CRLF/LF conversion; normalized content was identical.

This cumulative patch intentionally preserves the already-validated authoritative platform-status changes and includes the existing Session-lifecycle source on which the new bounded convergence depends. It does not modify the previously locked authoritative patch artifact.
