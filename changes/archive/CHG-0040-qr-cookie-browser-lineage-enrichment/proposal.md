# CHG-0040 QR Cookie Browser-Lineage Enrichment

Change ID: CHG-0040-qr-cookie-browser-lineage-enrichment
Status: ARCHIVED
Created: 2026-09-21
Owner task: multi_account_session_lifecycle_recovery

## User Outcome

Prevent newly QR-added or QR-recovered accounts from persisting a short passport-only Cookie lineage that can pass initial safe-MTOP checks yet hard-expire roughly one day later.

## Production evidence

Affected accounts 701229202 and 1835476245 were both created by QR on 2026-09-20 and both persisted 18-field Cookie lineages. In the same scheduled Session-maintenance batch on 2026-09-21, both transitioned to HUMAN_QR_REQUIRED with OFFICIAL_RENEWAL_FAILED_SAFE_MTOP_SESSION_EXPIRED, visible login UI and the same current and QR-required Cookie fingerprint.

Two current normal controls had 27 and 30 Cookie fields and remained REAL_BROWSER_LOGIN_READY.

The passport QR manager accumulates only Cookie fields present in its httpx h5api and passport responses and returns that set to AccountService.upsert_account_from_qr. For a new account, that candidate is directly persisted after safe-MTOP validation. No canonical Goofish browser enrichment occurs before persistence.

The existing CookieRenewBrowserService already owns the canonical persistent browser Profile, injects the candidate Cookie across Goofish, Taobao and Alipay domains, opens the real Goofish page, reads all browser cookies and merges them with the original fields.

## Scope

ALLOWED_CHANGE_SCOPE=backend-web/app/services/account_service.py QR upsert finalization; one incremental vendor patch; deterministic tests; sanitized evidence.
FORBIDDEN_CHANGE_SCOPE=AutoReplyService, reply rules, Publisher, product configuration, Token lifecycle, Native WS protocol, normal-account data, database schema.

GLOBAL_TOKEN_INVALIDATION=false
GLOBAL_ACCOUNT_RESTART=false
OTHER_ACCOUNT_DATA_WRITE=false

## Development precheck

TASK_TYPE=REPAIR
FAILURE_REASON=Fresh QR login persists passport/httpx response Cookies before the canonical browser lineage is established. Two new QR accounts retained only 18 Cookie fields and hard-expired together after initially passing hourly real-browser health.
RESPONSIBLE_LAYER=XIANYU upstream-native QR Account Session and Cookie lifecycle.
CURRENT_UPSTREAM_CAPABILITY=PARTIAL; upstream origin/main fdc8eb039be771456ecfbbbe43fa26f57feb3947 was fetched successfully on 2026-09-21 and still has the same passport Cookie collection and direct QR upsert behavior, while also already containing CookieRenewBrowserService.
CURRENT_LOCAL_CAPABILITY=PARTIAL; current runtime already has authoritative Cookie CAS, browser health persistence and browser-renew ownership, but QR finalization does not invoke browser enrichment before persistence.
CURRENT_RUNTIME_CAPABILITY=DEFECT_PROVEN; affected 18-field QR lineages hard-expired together while normal richer lineages remained browser-login ready.
CONFIGURATION_ISSUE=false
TOKEN_ISSUE=false
AUTO_REPLY_RULE_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=AccountService.upsert_account_from_qr only.
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=it validates and persists the QR passport candidate before establishing canonical browser Cookie lineage.
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=No new owner is required; insert one call to existing CookieRenewBrowserService before any authoritative QR Account or Cookie write.

## Upstream capability audit

The public upstream repository is zhinianboke/xianyu-auto-reply. Upstream origin/main at fdc8eb039be771456ecfbbbe43fa26f57feb3947 was fetched successfully and inspected directly. Its QR manager accumulates passport and h5api HTTP response Cookies and hands that candidate directly to AccountService.upsert_account_from_qr. It already contains CookieRenewBrowserService, but QR finalization does not call it before persistence.

## Pinned upstream evidence

UPSTREAM_REPOSITORY=zhinianboke/xianyu-auto-reply
UPSTREAM_COMMIT=fdc8eb039be771456ecfbbbe43fa26f57feb3947
UPSTREAM_EQUIVALENT_FIX_EXISTS=false
UPSTREAM_GAP=new QR account persists passport/httpx response Cookies without canonical browser Cookie enrichment before persistence

UPSTREAM_CHECKED=true
UPSTREAM_EQUIVALENT_FIX_EXISTS=false
LOCAL_DELTA_REASON=production proved that fresh QR passport-only Cookie lineage can hard-expire while richer canonical browser Cookie lineage remains valid
LOCAL_CHANGE_REQUIRED=true

## Existing local implementation search

Current production already has one authoritative browser owner, CookieRenewBrowserService, plus browser-health Cookie persistence and authoritative Cookie CAS. Current production does not have a QR-finalization call that establishes canonical browser Cookie lineage before the first durable QR Cookie write. Reuse the existing browser owner; do not create a second login, Session, Cookie or browser implementation.

## Why upstream cannot satisfy the requirement

The inspected upstream QR path has the same missing lifecycle edge: passport/httpx Cookie collection flows directly into AccountService QR persistence. The upstream browser-renew capability exists but is not invoked before QR persistence, so the production-proven short Cookie lineage remains possible.

## Approved exception ADR

Not applicable. Reuse decision is PATCH_UPSTREAM; no BUILD_LOCAL_EXCEPTION is requested.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No second QR owner, Session owner, Cookie store, browser broker, Token owner or reconnect manager is introduced.

## Component owner

AccountService remains the sole QR Account persistence owner. CookieRenewBrowserService remains the sole browser Cookie enrichment owner. validate_and_commit_authoritative_cookie_candidate remains the sole existing-account authoritative Cookie writer.

## Retirement plan for overlapping local code

Retire this patch when upstream QR finalization establishes and persists canonical browser Cookie lineage before reporting login success and equivalent regressions pass.

## Current-account recovery boundary

The already-expired affected Cookies were independently proven hard-expired with visible login UI, and neither affected account has stored username or password credentials. The qualified QR evidence correctly blocks blind renewal of the same Cookie lineage. One human QR per affected account is therefore required after the permanent fix is active; that scan will pass through the repaired enrichment path.
