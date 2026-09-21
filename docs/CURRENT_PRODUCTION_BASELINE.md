# XIANYU Current Production Baseline

Authority timestamp: **2026-09-21 current delta; older dated verification sections are retained as historical snapshots**

AI/developer first-read Living Handoff: [`docs/AI_PROJECT_HANDOFF.md`](AI_PROJECT_HANDOFF.md).

This document records current production facts needed for normal XIANYU operation and future Repair/Development decisions. Root `AGENTS.md` remains the highest-priority behavioral rule; current GitHub/local/runtime verification remains authoritative over dated snapshot values.

## Repository and responsibility

- XIANYU: https://github.com/yuanweizhang94-crypto/XIANYU
- Upstream business source: https://github.com/zhinianboke/xianyu-auto-reply
- Execution infrastructure: https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL

```text
UPSTREAM_FIRST=true
BUSINESS_EXECUTION_BY_DEFAULT=true
REUSE_FIRST=true
CURRENT_RUNTIME_FIRST=true
```

Upstream provides the primary business capability source. XIANYU preserves local governance, safety fixes, production integration, validation and minimal enhancements. COMPANY_LOCAL_EXECUTION_TOOL is infrastructure/thin adapter and must not own XIANYU business logic.

## Formal product publish path

```text
User
→ ChatGPT
→ COMPANY_LOCAL_EXECUTION_TOOL
→ receive_attachment
→ xianyu_material_import
→ XIANYU Material / material_id
→ xianyu_publish_single
→ current XIANYU Backend
→ POST /api/v1/product-publish/publish/batch
→ PublishExecutorService
→ execute_single_publish
→ publish_single_item
→ XianyuPublisher
→ current account Session/Profile
→ Goofish official platform publish flow
```

Real publishing must not bypass this path with `run_program`, `container_run`, temporary scripts, direct imports, or a second Publisher.

## Category production state

The 2026-08-12 category issue is closed.

Observed real platform behavior included:

```text
UI_VISIBLE=true
UI_SELECTABLE=true
CLICK_SUCCEEDED=true
```

Root cause of the prior false failure:

```text
OVERRESTRICTIVE_SELECTED_CONFIRMED_GATE
```

The local gate incorrectly required immediate field-text equality after a click even when the real platform had already closed the popup, entered another category level, updated internal category state/breadcrumb, or changed active/checked state.

Current closure:

```text
PLATFORM_UI_FIRST_RESTORED=true
SINGLE_CATEGORY_STATE_MACHINE=true
MULTI_LEVEL_CATEGORY_SUPPORTED=true
LOCAL_SEMANTIC_HARD_GATE=false
MAX_CATEGORY_LEVELS=5
```

Current category authority is the actual platform UI state machine. Semantic/local logic may rank or assist but must not be a hard gate.

Supported category states:

```text
FINAL_SELECTED
NEXT_LEVEL_REQUIRED
CLICK_NOT_EFFECTIVE
PC_WEB_UNSUPPORTED
LOGIN_REQUIRED
PLATFORM_VERIFICATION_REQUIRED
```

Do not return `no_supported_category` solely from local mapping/semantic/selected-class misses.

## PC Web limitation

If Goofish explicitly states that the category is unsupported on PC Web:

```text
CATEGORY_WEB_UNSUPPORTED
→ FAIL_CLOSED
```

Do not force category IDs, use an inaccurate category, fabricate a category, or bypass the official restriction.

## Final real production verification — 2026-08-12

```text
HISTORICAL_SNAPSHOT_ONLY=true
```

Original five-item closure:

| Material | Final state | Authoritative result |
|---|---|---|
| 9 | SUCCESS | `platform_item_id=1075653752858` |
| 8 | SUCCESS | `platform_item_id=1074662425907` |
| 7 | SUCCESS | `platform_item_id=1073635950977` |
| 6 | SUCCESS | `platform_item_id=1073637026044` |
| 10 | CATEGORY_WEB_UNSUPPORTED | official PC-Web limitation; fail closed |

Current production conclusions at that dated validation point:

```text
PUBLISH_FLOW_FIXED=true
CATEGORY_STATE_MACHINE_FIXED=true
SESSION_FLOW_WORKING=true
REAL_PUBLISH_VERIFIED=true
REMAINING_SYSTEM_BLOCKER=NONE
```

A future ordinary failure must be classified from its new `failure_reason`; do not assume a recurrence of the old Publisher/category defect. Do not use this dated snapshot to skip current GitHub/local/runtime verification.

## Session production authority

For operations that genuinely require a browser/page session, readiness must come from the real upstream Session/browser state rather than Cookie/Profile/DB presence alone.

For **normal Direct/Personal Publish**, `REAL_BROWSER_LOGIN_READY` is not a publish gate. Current upstream publishing uses account-capability routing into `XianyuDirectPublisher / XianyuPersonalPublisher → MTOP`; Browser/Profile/Playwright readiness must not be reinserted in front of that normal path.

The following are not universal readiness proof by themselves:

```text
COOKIE_PRESENT
CANONICAL_PROFILE_PRESENT
ACCOUNT_RECORD_HEALTHY
```

Current production Session background maintenance baseline:

```text
API_COOKIE_RENEW_ENABLED=true
RENEW_INTERVAL_SECONDS=3600
```

Avoid overlapping Session scheduler/renewal owners.

If the real platform requires human QR interaction during normal business execution, skip that account and continue with a healthy account. Do not let one account block the batch.

### 2026-09-20 strong verification publish blocker closure

One production account returned:

```text
FAIL_BIZ_STRONG_VALID_VERIFY_INFO::用户未通过认证
```

even though account health reported `LOGIN_READY=true`, `ACCOUNT_ENABLED=true`, `ACCOUNT_ONLINE=true`, and the mobile account page showed user identity uploaded, real-person verification complete, and Alipay real-name verification complete.

The actual missing prerequisite was the Alipay transaction collection capability required by Xianyu before an item can be sold. After the user completed the in-app “开通支付宝收款功能 / 交易收款功能” verification, the same formal Publisher path immediately returned authoritative `SUCCESS` for that account without any Publisher/Session code change.

Current operational conclusion:

```text
STRONG_VALID_VERIFY_INFO_MAY_MEAN_PAYMENT_COLLECTION_CAPABILITY_NOT_OPEN
DO_NOT_ASSUME_REAL_NAME_AUTH_MISSING
CHECK_IN_APP_ALIPAY_TRANSACTION_COLLECTION_CAPABILITY_FIRST
NO_PUBLISHER_REPAIR_REQUIRED_WHEN_THIS_PLATFORM_GATE_IS_PRESENT
```

## Publish state semantics

Formal states:

```text
SUBMITTED
RUNNING
SUCCESS
FAILED
UNKNOWN
```

Backend HTTP 200 / “task submitted” means `SUBMITTED`, not `SUCCESS`.

`SUCCESS` requires one of:

```text
platform_item_id
item_url
AUTHORITATIVE_SYNC_CONFIRMED=true
```

`UNKNOWN` must never be blindly retried.

## 502 / timeout recovery

For side-effecting actions, a connector error cannot prove the remote/local operation did not execute.

```text
502 / timeout / connection error
→ STOP_NEW_EXECUTION
→ READ_ONLY_STATUS_RECOVERY
→ SUCCESS / FAILED / UNKNOWN
```

If `UNKNOWN`, do not execute the action again until authoritative state is recovered.

## Existing business capabilities

Without new direct evidence, treat these as existing capability families and reuse/repair the existing owner:

- Account
- Cookie
- Session
- canonical Profile
- Material
- Publisher
- Category
- Playwright
- Scheduler
- WebSocket
- Session Renew
- QR Login
- Browser Lock
- Publish Status
- Backend Auth
- Material Bridge

Do not create second implementations.

## Development decision rule

Before changing code, compare:

```text
CURRENT_UPSTREAM
vs
CURRENT_LOCAL
vs
CURRENT_RUNTIME
```

Only modify the existing implementation after proving the issue is not stale Runtime, configuration, Session/data/account state, incorrect invocation, or official platform limitation.

See `docs/AI_PROJECT_HANDOFF.md`, `AGENTS.md`, and `docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md` for the mandatory precheck.

## Auto Reply / Native WebSocket reconnect readiness — 2026-09-20

Production proved that transport health alone is not sufficient Auto Reply readiness. A buyer inbound could be visible in Online Chat while Native WS still reported connected=true and token_ready=true but produced no Native MessageHandler or AutoReplyService trace.

Canonical root cause:

```text
ROOT_CAUSE=NATIVE_WS_FALSE_HEALTH_AFTER_UNCONFIRMED_REGISTRATION
REGISTRATION_ACK_REQUIRED=true
UNCONFIRMED_REGISTRATION_MUST_NOT_MARK_CONNECTED=true
```

The existing upstream Native WebSocket owner sent /reg, waited a fixed sleep, sent ackDiff, and could then be reported CONNECTED without proving that the server accepted registration. Pinned upstream bda1a859df63fa5f24e51398fa80a23490bb6dfc contains the same gap.

CHG-0038 repairs only the existing owner: explicit reg_mid, bounded matching response wait, code=200 readiness gate, preservation of early frames, then the existing ackDiff. The pre-activation repository verification baseline was 683/683 PASS.

Permanent production activation is complete:

```text
CURRENT_WEBSOCKET_IMAGE=xianyu-chg0038-websocket:registration-readiness-20260920-r2
REGISTRATION_ACK_PROVEN_COUNT=8
MESSAGE_LOOP_READY_COUNT=8
POST_SWITCH_WS_CONNECTED=8
POST_SWITCH_TOKEN_READY=8
HUMAN_QR_REQUIRED_COUNT=0
PLATFORM_VERIFICATION_REQUIRED_COUNT=0
ONLINE_ACCOUNT_DROPPED_COUNT=0
```

Account 2217936413500 produced an initial real /reg response code=401. The new readiness gate did not allow CONNECTED; the existing reconnect path ran; the later attempt received a successful acknowledgement and entered the message loop.

Organic post-activation Auto Reply E2E is also proven. Account 2221384086829, item 1086370184047, received a buyer inbound after activation and traversed the existing Native MessageHandler → AutoReplyService → item default rule → image send success → text send success path. Sanitized reply activity recorded reply_sent / success / text_image.

```text
PERMANENT_WEBSOCKET_RUNTIME_PATCH=PASS
AUTO_REPLY_REAL_E2E=PASS
```

Full sanitized evidence: changes/archive/CHG-0038-websocket-registration-readiness/evidence/20260920-production-activation-and-real-e2e.md.

## 2026-09-20 CHG-0039 target-level Token invalidation recovery

CHG-0038 remains the current production WebSocket image. A later target-account recovery exposed a separate Token lifecycle defect: `restart(invalidate_token_cache=true)` writes an explicit cache invalidation marker, but startup `allow_expired=True` can immediately reuse that same Token. Account 2214313339860 reproduced the defect with the same Token fingerprint after explicit invalidation.

CHG-0039 is the current active source change and patches only `CookieTokenManager._get_cached_token()` so the explicit invalidation marker is treated as a cache miss before natural expired-cache fallback. The pinned upstream bda1a859 has the same gap. Source/repository verification is PASS, but the patch is not globally activated in production in this cycle.

Bounded target-only runtime recovery removed only 2214313339860's stale Token cache row and reused the existing single-account restart owner. The account then obtained a fresh Token generation at 2026-09-20 22:37:55, completed matching /reg ACK, connected, and entered the normal message loop. Organic buyer-message E2E remains pending.

Two related account incidents were separately classified: 701229202 had one newly published item missing its item-level default reply row; that single item config was repaired through the existing XIANYU item reply config owner. 1835476245 had platform-reported buyer activity with no retained Native buyer-body trace; its fresh Token remained unchanged and only its account-level socket/subscription generation was rebuilt. No global WebSocket restart or all-account Token invalidation was performed.

## 2026-09-21 current production runtime — CHG0040 + CHG0041

Current production components:

```text
BACKEND_IMAGE=xianyu-chg0040-backend-web:qr-cookie-enrichment-20260921-r3
WEBSOCKET_IMAGE=xianyu-chg0041-websocket:native-chat-rpc-20260921-r1
FRONTEND_IMAGE=xianyu-chg0018-frontend:chatnew-reconnect-convergence-20260919-r1
BACKEND_HEALTH=PASS
FRONTEND_HEALTH=PASS
WEBSOCKET_HEALTH=PASS
SCHEDULER_HEALTH=PASS
```

CHG0041 root cause was not a missing Account enable hook. The formal enable lifecycle already invoked the existing Native WebSocket owner and reached Token ready, matching /reg ACK and message-loop-ready. The actual first divergence was the current Backend shared-Native Chat RPC calling WebSocket internal endpoints that were absent from the CHG0039 image baseline and returned HTTP 404.

CHG0041 restores only the already-existing local Native Chat RPC surface onto the CHG0039 production preimage. The production WebSocket continues to preserve CHG0038 matching registration ACK readiness and CHG0039 explicit Token invalidation precedence. The Backend continues to preserve CHG0040 QR canonical browser Cookie enrichment.

Production closure for account 2219319284219:

```text
ACCOUNT_ENABLED=true
LOGIN_READY=true
HUMAN_QR_REQUIRED=false
WS_CONNECTED=true
TOKEN_READY=true
REGISTRATION_ACK=PASS
MESSAGE_LOOP_READY=true
NATIVE_CHAT_RPC_PRODUCTION_CALL=PASS
POST_FIX_CHAT_RPC_HTTP_STATUS=200
POST_FIX_CHAT_RPC_SUCCESS=true
CURRENT_ENABLED_ACCOUNT_COUNT=1
DISABLED_ACCOUNT_RUNTIME_COUNT=0
DUPLICATE_RUNTIME_COUNT=0
```

No manual account restart was used to create this PASS after CHG0041 activation. Full sanitized evidence is in `changes/archive/CHG-0041-native-chat-runtime-equivalence/`.

## Security

No secret values are part of this baseline. Never commit Cookie/Token/JWT/Authorization/password/API key/private key/QR payload/browser Profile secret/real customer message material.
