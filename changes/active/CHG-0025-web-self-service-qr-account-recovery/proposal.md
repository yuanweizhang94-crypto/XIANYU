# CHG-0025 Web Self-Service QR Account Recovery

Status: APPROVED

Change ID: CHG-0025-web-self-service-qr-account-recovery

CHG0025_SCOPE_APPROVED=true
NO_REAL_LOGIN_DURING_CHANGE=true
REAL_QR_CREATE_COUNT_EXPECTED=0
REAL_QR_SCAN_COUNT_EXPECTED=0
WEBSITE_USER_SELF_SCAN_READY_TARGET=true

## Execution contract

User outcome: allow the XIANYU website owner to recover one specific existing account later by opening that account's QR recovery action, scanning the official QR code manually, and having the existing XIANYU QR/Account/Cookie/WebSocket owners persist only that same account.

Confirmed blocker: the existing website QR UI and Backend QR owner are global add-account semantics. `/api/v1/qr-login/generate` is not target-account scoped, and successful QR protocol status is rendered as immediate login success before authoritative account readiness readback.

Smallest success test: deterministic owner-spy tests prove account-scoped generation/ownership, cross-account identity mismatch fail-closed before Cookie/Session/WebSocket mutation, read-only polling, explicit-only QR refresh, and no false-green until existing authoritative readiness reports connected + token_ready with no higher-priority blocker.

Stop condition: a second Login/QR/Session/Cookie/WebSocket owner is required; scanned identity cannot be validated before authoritative Cookie persistence; current production Frontend source authority cannot be proven; production activation becomes UNKNOWN; a healthy other account regresses; or real QR/password/Item Sync execution is required for proof.

## Development precheck

TASK_TYPE=DEVELOPMENT
FAILURE_REASON=EXISTING_QR_OWNER_NOT_ACCOUNT_SCOPED_PLUS_FRONTEND_FALSE_GREEN
RESPONSIBLE_LAYER=XIANYU_BACKEND_ROUTE_PLUS_EXISTING_FRONTEND_ACCOUNT_UI
CURRENT_UPSTREAM_CAPABILITY=QR_LOGIN_EXISTS_GLOBAL_ADD_ACCOUNT_SEMANTICS
CURRENT_LOCAL_CAPABILITY=QR_LOGIN_EXISTS_WITH_EXISTING_ACCOUNT_COOKIE_WEBSOCKET_OWNERS
CURRENT_RUNTIME_CAPABILITY=EXISTING_GLOBAL_QR_UI_AND_QR_ROUTE_ACTIVE
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=qr_login.generate/status route account binding + existing Accounts QR UI/readback
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=NO_TARGET_ACCOUNT_BINDING_AND_PROTOCOL_SUCCESS_IS_RENDERED_BEFORE_AUTHORITATIVE_READINESS
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false
REUSE_DECISION=PATCH_EXISTING_QR_OWNER_AND_EXISTING_FRONTEND_UI

## Upstream capability audit

The existing upstream/local XIANYU capability already provides the QR login owner and the Account/Cookie/Session/WebSocket continuation chain. CHG0025 does not create a replacement login system, QR engine, Session owner, Cookie owner, or WebSocket owner. The confirmed defect is limited to missing target-account binding in the existing QR route plus Frontend false-green behavior.

## Pinned upstream evidence

The pinned existing capability reused by this Change is the current QR owner `backend-web/app/services/qr_login/qr_login_manager` behind `POST /api/v1/qr-login/generate` and `GET /api/v1/qr-login/status/{session_id}`. Source/runtime authority is additionally locked by the recorded Backend route preimage SHA256 `1d84ac624fc6ce6393d8b744f7c1d4b95cfa89c44f78b906fa0e9be70e7e2bd1`, the accepted CHG0024 Backend lineage, and the CHG0025 source-authority evidence. No floating upstream implementation is silently adopted.

## Existing local implementation search

The existing implementation search found the already-active QR route/manager, `AccountService.upsert_account_from_qr`, authoritative Cookie validation/persistence, existing Session lifecycle, existing WebSocket start/restart, existing CHG0023 readiness, and the existing Accounts QR modal/readiness UI. These owners are reused rather than duplicated.

## Reuse decision

Decision: PATCH_UPSTREAM

The smallest repair is to patch the existing QR route for strict account scope and patch the existing Accounts UI/API adapter for target propagation and authoritative no-false-green readback. The underlying QR/Login/Session/Cookie/WebSocket execution owners remain unchanged.

## Duplicate implementation risk

Creating another login endpoint, QR manager, Session lifecycle, Cookie persistence path, WebSocket recovery owner, or independent readiness authority would duplicate existing capability and could allow cross-account writes or divergent authentication state. CHG0025 therefore keeps `NEW_LOGIN_OWNER_COUNT=0`, `NEW_QR_OWNER_COUNT=0`, `NEW_SESSION_OWNER_COUNT=0`, and `NEW_COOKIE_OWNER_COUNT=0`.

## Why upstream cannot satisfy the requirement

The existing upstream-native path is the correct owner but cannot satisfy the required website account-recovery safety as-is because QR generation is not bound to one existing target account and protocol success can be rendered before authoritative readiness readback. The defect is repaired in place; it does not justify a parallel implementation.

## Approved exception ADR

Not required. CHG0025 does not use `BUILD_LOCAL_EXCEPTION`, does not introduce a duplicate capability, and therefore requires no duplicate-implementation exception ADR.

## Component owner

Existing owners remain authoritative: `qr_login_manager` owns QR protocol state; the existing Backend QR route owns the account-scoped web boundary; `AccountService` and the authoritative Cookie service own account/Cookie persistence; the existing Session and WebSocket services retain their lifecycle ownership; the existing Accounts page/API adapter owns only web presentation and request/readback wiring.

## Retirement plan for overlapping local code

No overlapping local execution owner is introduced, so there is no parallel owner to retire. The CHG0025 Frontend/route delta remains a minimal patch around the existing owner chain; if upstream later provides equivalent account-scoped recovery and no-false-green behavior, this delta should be reviewed for retirement rather than expanded.

## Existing owner truth

EXISTING_QR_OWNER=`backend-web/app/services/qr_login/qr_login_manager`
EXISTING_QR_CREATE_ENTRYPOINT=`POST /api/v1/qr-login/generate`
EXISTING_QR_STATUS_ENTRYPOINT=`GET /api/v1/qr-login/status/{session_id}`
EXISTING_COOKIE_OWNER_REUSED=`AccountService.upsert_account_from_qr -> validate_and_commit_authoritative_cookie_candidate`
EXISTING_SESSION_OWNER_REUSED=true
EXISTING_WEBSOCKET_OWNER_REUSED=true
NEW_LOGIN_OWNER_COUNT=0
NEW_QR_OWNER_COUNT=0
NEW_SESSION_OWNER_COUNT=0
NEW_COOKIE_OWNER_COUNT=0
NEW_WEBSOCKET_OWNER_COUNT=0

Existing success chain remains:

```text
qr_login_manager
-> official QR result
-> get_session_cookies()
-> scanned unb
-> AccountService.upsert_account_from_qr()
-> authoritative Cookie validation/persistence
-> existing WebSocket start/restart
-> existing CHG0023 readiness
```

## Confirmed defects

### Defect A — target account is not bound

CURRENT_BACKEND_QR_ACCOUNT_SCOPE_STRICT=false
QR_ACCOUNT_SCOPE_STRICT_TARGET=true
QR_TARGET_ACCOUNT_OWNERSHIP_CHECK_TARGET=true

Current generation records only user/session ownership. Successful scan uses returned `unb` to upsert whichever account matches it. That cannot prove account A's recovery QR cannot write account B.

Required fix before any Cookie/Session/account/WebSocket write:

```text
session_id + owner_user_id + target_account_id
-> scanned_unb
-> compare against authoritative identity of target_account_id
-> exact match: continue existing owner chain
-> mismatch: QR_IDENTITY_TARGET_MISMATCH + no writes
```

Mismatch invariants:

```text
COOKIE_WRITE_COUNT=0
SESSION_WRITE_COUNT=0
ACCOUNT_UPDATE_COUNT=0
WEBSOCKET_ACTION_COUNT=0
```

### Defect B — protocol success can false-green

QR_FALSE_GREEN_FORBIDDEN=true

Current Frontend marks QR protocol `success`/`already_processed` as UI success immediately. New UI must enter `CHECKING_ACCOUNT_STATUS`, refresh the existing account details/readiness authority, and only show final success when no higher-priority blocker exists and Auto Reply readiness is ONLINE with the existing runtime connected/token-ready semantics.

No second readiness owner may be created.

## Source authority reconciliation

SOURCE_AUTHORITY_RECONCILIATION=PASS
EXACT_BASE_OBJECT_RECOVERED=true
HISTORICAL_BASE_64C245_CLASSIFICATION=LOCAL_HISTORICAL_PATCH_BASE_WORKTREE_OBJECT
HISTORICAL_BASE_64C245=`64c245bc85ac56e34339fa056b0e291a16a3843b`
FRONTEND_SOURCE_AUTHORITY_MODEL=EXACT_HISTORICAL_FRESH_APPLY_PLUS_EXACT_CURRENT_BUNDLE_MATCH
CONTENT_EQUIVALENT_BASE_USED=false

Current production Frontend lineage is the accepted `xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2` build. Independent historical Fresh Apply source trees still exist with HEAD exactly `64c245bc...`; their CHG0018 postimages match each other. Historical deployed build artifacts under `.runtime_frontend_restore` exactly match the currently served Accounts/main/shared bundles.

Authoritative CHG0025 Frontend preimages:

- `frontend/src/api/accounts.ts` SHA256 `71dcfde1ac53669261e4cbf19c781d3cd46f0c9ad69bfc0963240cd15b492268`
- `frontend/src/pages/accounts/Accounts.tsx` SHA256 `f31ece92d0d9570ea19477c29b1218bfd3b3e2aa365385ee20f9321af69fb5bf`
- `frontend/src/types/index.ts` SHA256 `71a0b5a41ed98ed773415d3f719822bbd31d3e02799dcfd357ce693404cf9087`

Current accepted CHG0024 Backend image is `xianyu-chg0024-backend-web:item-sync-no-auth-recovery-20260823-r1`.

Authoritative Backend QR route preimage:

- `backend-web/app/api/routes/qr_login.py` SHA256 `1d84ac624fc6ce6393d8b744f7c1d4b95cfa89c44f78b906fa0e9be70e7e2bd1`

## Allowed change scope

ALLOWED_CHANGE_SCOPE=
- `backend-web/app/api/routes/qr_login.py`
- `frontend/src/api/accounts.ts`
- `frontend/src/pages/accounts/Accounts.tsx`
- `frontend/src/types/index.ts` only if a type is actually required
- CHG0025 deterministic tests/evidence
- one exact CHG0025 vendor patch over the proven preimages
- minimal Backend + Frontend candidate/deployment only

FORBIDDEN_CHANGE_SCOPE=
- AccountService/Cookie validation algorithm
- Session lifecycle/renewal
- WebSocket core owner
- qr_login_manager unless route-level binding proves impossible
- Publisher
- Scheduler
- Chat
- Item Sync
- password login
- real QR creation/scan during this Change

## Runtime safety boundary

REAL_QR_CREATE_COUNT=0_REQUIRED
REAL_QR_SCAN_COUNT=0_REQUIRED
QR_SUCCESS_COUNT=0_REQUIRED
PASSWORD_LOGIN_ATTEMPTS=0_REQUIRED
REAL_MESSAGES_SENT=0_REQUIRED
ADDITIONAL_ITEM_SYNC_INVOCATIONS=0_REQUIRED
TOTAL_NEW_T7_ITEM_SYNC_BUSINESS_INVOCATIONS=1_REQUIRED

Negative controls must remain untouched:

- `2221422775489=HUMAN_QR_REQUIRED`
- `2221501265279=HUMAN_QR_REQUIRED`

No real QR is generated for either account during implementation or acceptance.

## T4 implementation checkpoint

BACKEND_IMPLEMENTATION_COMPLETE=true
FRONTEND_IMPLEMENTATION_COMPLETE=true
QR_ACCOUNT_SCOPE_STRICT=true
QR_TARGET_ACCOUNT_OWNERSHIP_CHECK=true
QR_SESSION_TARGET_IMMUTABLE=true
QR_IDENTITY_PREWRITE_GUARD=true
QR_FALSE_GREEN_FORBIDDEN=true
BACKEND_DETERMINISTIC_TESTS=10/10_PASS
FRONTEND_DETERMINISTIC_TESTS=18/18_PASS
REAL_QR_CREATE_COUNT=0
REAL_QR_SCAN_COUNT=0

Exact CHG0025 patch: `vendor/patches/xianyu-auto-reply/chg0025-web-self-service-qr-account-recovery.patch` SHA256 `f3ecaf30603ec593521fcc84b0cce5dac92d0da45da0514ddcf8d577ab6fe8e8`.
