# CHG-0022 WebSocket Token Network Classification

Status: ARCHIVED

Change ID: CHG-0022-websocket-token-network-classification

## Execution contract

User outcome: ordinary network/DNS failures must not invalidate an otherwise valid Auto Reply Token or trigger a paid remote `xianyu_token` storm.

Confirmed blocker: the existing WebSocket owner classifies pre-connect DNS/reset/timeout failures as Token/Auth failures when `was_connected=false`, then uses short attempt duration as sufficient evidence to invalidate Token cache.

Smallest success test: DNS/gaierror/reset/timeout stay on the existing network backoff path without Token invalidation or paid remote Token acquisition, while explicit existing Token/Session rejection semantics still invalidate/refresh through the current Token/Session owner.

## DEVELOPMENT_PRECHECK

TASK_TYPE=REPAIR
FAILURE_REASON=NETWORK/DNS failure is amplified by incorrect pre-connect network/auth classification plus short-failure Token invalidation.
RESPONSIBLE_LAYER=XIANYU existing WebSocket owner.
CURRENT_UPSTREAM_CAPABILITY=EXISTS_WITH_CONFIRMED_DEFECT.
CURRENT_LOCAL_CAPABILITY=EXISTS_WITH_CONFIRMED_DEFECT_IN_PRODUCTION_RUNTIME.
CURRENT_RUNTIME_CAPABILITY=RUNNING_EXISTING_OWNER_WITH_CONFIRMED_DEFECT.
CONFIGURATION_ISSUE=false.
SESSION_OR_DATA_ISSUE=false.
OFFICIAL_PLATFORM_LIMITATION=false.
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=`websocket/app/services/xianyu/xianyu_async.py` existing reconnect exception branch only.
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=its current network classifier excludes DNS and requires `was_connected=true`, and its short-attempt branch invalidates Token without authentication evidence.
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false; this Change patches the existing owner only.

## Upstream capability audit

Current upstream `origin/main@9cbb3725b7e91daec33cb824a3ff4bd84acdcb12` was fetched and inspected. Its `xianyu_async.py` still has the same `is_network_type_error and was_connected` gate, does not classify `gaierror`/DNS resolution failure, and still clears Token cache when `attempt_duration < 15`. No newer upstream commit containing an equivalent repair was found in the fetched main history; targeted public GitHub searches also found no matching upstream issue/fix.

## Pinned upstream evidence

Pinned patch/test base: `9cbb3725b7e91daec33cb824a3ff4bd84acdcb12`. Relevant source: `websocket/app/services/xianyu/xianyu_async.py`. Production comparison source is the currently running `xianyu_chg0017_websocket` file with pre-change SHA256 `fe795325e14050957b01714c26dffa135479f3d182df39301f6a9ad5fdb77797`.

## Existing local implementation search

Current recovery branch, archived Changes, vendor patches, and tests were searched for `gaierror`, `attempt_duration`, `was_connected`, and `_delete_cached_token`; no existing tracked equivalent fix was found. Historical Auto Reply/Session fixes remain authoritative and must be preserved.

## Reuse decision

Decision: PATCH_UPSTREAM

The existing WebSocket owner, connection manager, Token cache, Token API owner, Session authority, network exponential backoff and jitter are retained. No new service, state machine, Token owner, auth probe, cache, scheduler, or worker is created.

## Duplicate implementation risk

LOW if the change remains inside the current reconnect exception branch and tests only. HIGH if a second network/auth classifier, Token owner, Session owner, or reconnect worker is introduced; those are forbidden.

## Why upstream cannot satisfy the requirement

Latest upstream contains the defective classification itself and has no equivalent fix to adopt/configure. The smallest auditable correction is therefore a patch to that path.

## Approved exception ADR

Not applicable. This is `PATCH_UPSTREAM`, not `BUILD_LOCAL_EXCEPTION`.

## Component owner

The existing `XianyuAsync` WebSocket reconnect loop remains the sole connection owner. Existing `CookieTokenManager`/Token response semantics remain the Token invalidation owner.

## Retirement plan for overlapping local code

No overlapping owner is introduced. If upstream later ships an equivalent verified repair, this patch should be reviewed for retirement/adoption.

## Scope

ALLOWED_CHANGE_SCOPE=`xianyu_async.py` reconnect network/auth classification; targeted/regression tests; patch/evidence/governance for this Change; WebSocket-only runtime activation after tests.

FORBIDDEN_CHANGE_SCOPE=Token TTL; Token DB schema/cache architecture; `remote_token_api`; `im_token_api` contract; Session/Cookie owners; Chat; Auto Reply owner; Scheduler; Backend; Publisher; COMPANY/JZAI/Wallet/Payment/OKX; QR actions; real messages/products/payments.
