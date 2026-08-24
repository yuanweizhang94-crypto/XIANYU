# CHG-0027 Session Transient Classification and QR Cooldown Lineage

Status: ARCHIVED

Change ID: CHG-0027-session-transient-classification-qr-cooldown-lineage

## User outcome

Stop transient Session-renew transport failures from being rendered as permanent Session expiration, invalidate only stale pre-QR Session-expired cooldown after a successful authoritative QR Cookie lineage change, then complete the final enabled-account runtime/UI audit without real messages, real publishing, Item Sync, password login, manual reconnect, or QR execution.

## Confirmed blockers

1. Existing Backend capability composition treats any `SESSION_RENEW_FAILED` as fatal even when the underlying evidence is `SAFE_MTOP_NETWORK_ERROR`; current authoritative Cookie validation for Zhou (`2217936413500`) is `AUTH_VALID`, so the current `Session已失效` rendering is a proven false red.
2. Existing `_session_expired_cooldown` stores only `account_id -> timestamp`; the Scheduler therefore continues consuming a pre-QR Session-expired cooldown after a successful authoritative QR Cookie commit creates a new Session lineage.

## Smallest success test

Deterministic tests prove transient renew evidence cannot produce `SESSION_EXPIRED/LOGIN_REQUIRED/PVR`, explicit expired evidence still blocks, newer AUTH_VALID wins over stale transient failure, and a Session-expired cooldown is valid only for the Cookie fingerprint lineage that created it. New QR lineage invalidates only that account's old Session-expired cooldown; unrelated cooldowns/blockers remain unchanged.

## Stop condition

Stop if a new Session/Cookie/QR/WebSocket/Chat/Publisher owner is required, if repair needs a Session schema migration or global Scheduler redesign, if production replacement is UNKNOWN and cannot be resolved read-only, if an unrelated business defect is discovered, or if a real QR/message/publish/Item Sync action becomes necessary for proof.

## Development precheck

TASK_TYPE=REPAIR
FAILURE_REASON=TRANSIENT_SESSION_RENEW_FAILURE_MISCLASSIFIED_AS_FATAL__SESSION_EXPIRED_COOLDOWN_NOT_BOUND_TO_COOKIE_LINEAGE
RESPONSIBLE_LAYER=XIANYU_EXISTING_SESSION_STATUS_CONSUMERS_AND_EXISTING_SESSION_EXPIRED_COOLDOWN_UTILITY
CURRENT_UPSTREAM_CAPABILITY=EXISTS
CURRENT_LOCAL_CAPABILITY=EXISTS_WITH_CONFIRMED_COMPOSITION_AND_LINEAGE_DEFECTS
CURRENT_RUNTIME_CAPABILITY=CHG0026_R5_BACKEND_ACTIVE__EXISTING_SCHEDULER_ACTIVE
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=existing session failure classifier/capability composition + existing session-expired cooldown record/check
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=SESSION_RENEW_FAILED_IS_TREATED_AS_INTRINSICALLY_FATAL_AND_COOLDOWN_HAS_NO_AUTHORITATIVE_LINEAGE_MARKER
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false
REUSE_DECISION=PATCH_UPSTREAM

## Upstream evidence

Pinned upstream checkout: `D:/xianyu-upstream-pilot` at `bda1a859df63fa5f24e51398fa80a23490bb6dfc`; current upstream main was fresh-read as `29dc831d4498f3174f0502c989a352ef59815553` for comparison only. Existing Account/Session/Cookie/QR/WebSocket/Chat/Publisher/Scheduler owners are retained.

Relevant existing paths include `common/utils/cookie_refresh.py`, `backend-web/app/api/routes/cookies.py`, `backend-web/app/api/routes/chat_new.py`, existing QR/Account services, and Scheduler tasks that consume `is_account_session_cooled`.

## Current source/runtime authority

PRE_CHANGE_MAIN_SHA=`b1f020c27644fde58e1fb6b247b18c8ebce8e343`
CURRENT_PRODUCTION_BACKEND=`xianyu-chg0026-backend-web:qr-dual-chat-platform-evidence-20260824-r5`
CONTROLLED_SOURCE=`D:/xianyu-chg0026-source`

The controlled source hashes for current `cookies.py`, `qr_login.py`, and `im_session_manager.py` were compared directly with the running R5 Backend container and matched byte-for-byte before CHG0027 source edits.

## Reuse decision

Decision: PATCH_UPSTREAM

No new Session, Cookie, QR, Chat, WebSocket, Publisher, Scheduler, credential-version, or capability owner is created. Existing `cookie_fingerprint()` is reused as the Session-lineage marker.

## Allowed scope

- existing Backend Session/capability classification consumers
- existing `common/utils/cookie_refresh.py` Session-expired cooldown record/check
- only the minimal existing call sites required to supply current authoritative Cookie lineage
- deterministic tests and sanitized evidence
- minimal Backend/Scheduler candidate and serial deployment only if their source changes
- final read-only account/Auto Reply/Chat/Publisher/UI audit
- CHG0026 governance archive migration

## Forbidden scope

Session/QR/WebSocket/Chat/Publisher redesign, new owner/service/table/schema, Frontend hardcoded workaround, account-specific code, platform-verification bypass, real QR, password login, manual Chat connect, Cookie/Token refresh for acceptance, real outbound messages, real product publishing/modification, Item Sync, unrelated governance debt.

ACCOUNT_SPECIFIC_HARDCODE_COUNT=0
NEW_SESSION_OWNER=false
NEW_COOKIE_OWNER=false
NEW_CHAT_OWNER=false
NEW_WEBSOCKET_OWNER=false
NEW_PUBLISH_OWNER=false

## Scoped production acceptance and follow-up split

CHG0027_SCOPED_PRODUCTION_ACCEPTANCE=PASS
DEFECT_A_ACCEPTANCE=PASS
DEFECT_B_ACCEPTANCE=PASS
PRODUCTION_FREEZE=true

The accepted CHG0027 scope is limited to evidence-based transient/fatal Session classification and Cookie-lineage-bound Session-expired cooldown. Backend and Scheduler source fixes were serially deployed and accepted without QR, reconnect, Item Sync, real message, or real publish actions.

Publisher readiness remains an independent pre-existing capability gap: the existing consumers can report lazy `RETRY_LATER`, but no current READY producer was found. It is classified `PUBLISH_READINESS_LAZY_PENDING_NO_READY_PRODUCER` and must be audited upstream/current-owner first in a later Change; CHG0027 must not add a writer.

Real website rendering remains blocked by the current authorized Browser owner, which returns `URL_PORT_BLOCKED` for the fixed production Frontend target. Static bundle/runtime wiring, Accounts consumer mapping, Chat state mapping, and the four-second conditional polling contract are accepted. Browser permission or infrastructure work is a separate fixed-target, read-only prerequisite and must not be mixed with Publisher source work.

ACCOUNT_RUNTIME_OVERALL_ACCEPTANCE=PARTIAL__FOLLOWUP_REQUIRED
FOLLOWUP_DEFECTS_EXPLICITLY_PERSISTED=true

## Upstream capability audit

The original upstream feature description and the existing Account, Session, Cookie, QR, WebSocket, Chat, Publisher, and Scheduler owners were inspected before repair. The native workflow and current owner paths already exist; CHG0027 repairs only confirmed classification and cooldown-lineage defects in those paths.

## Pinned upstream evidence

Pinned upstream checkout: `D:/xianyu-upstream-pilot` at `bda1a859df63fa5f24e51398fa80a23490bb6dfc`. Current upstream main `29dc831d4498f3174f0502c989a352ef59815553` was comparison evidence only and was not silently adopted.

## Existing local implementation search

Current production R5 source, accepted CHG0026 governance, `common/utils/cookie_refresh.py`, Backend capability composition, QR routes, Chat status composition, Publisher consumers, Scheduler cooldown consumers, targeted tests, and retained runtime evidence were searched. No parallel owner or existing READY producer was substituted.

## Duplicate implementation risk

Risk is controlled by reusing `cookie_fingerprint()` and patching the existing classification/cooldown owners. A second Session service, Cookie manager, QR owner, Chat owner, Publisher, Scheduler, table, schema, or writer remains forbidden.

## Why upstream cannot satisfy the requirement

The existing path treats the lifecycle outcome `SESSION_RENEW_FAILED` as intrinsically fatal in consumers and stores Session-expired cooldown as only `account_id -> timestamp`; those confirmed defects require the minimal upstream-path patch recorded by this Change.

## Approved exception ADR

Not applicable. The decision is `PATCH_UPSTREAM`, not `BUILD_LOCAL_EXCEPTION`.

## Component owner

Existing upstream Backend Session/capability composition and existing common/Scheduler Session-expired cooldown utilities remain the execution owners. XIANYU owns only the formal patch and sanitized evidence.

## Retirement plan for overlapping local code

No overlapping local runtime component is introduced. The patch should be reviewed for retirement when upstream provides equivalent evidence-based classification and Cookie-lineage cooldown semantics.
