# XIANYU Current Production Baseline

Authority timestamp: **2026-08-12 22:33 Asia/Taipei (UTC+8)**

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

## Security

No secret values are part of this baseline. Never commit Cookie/Token/JWT/Authorization/password/API key/private key/QR payload/browser Profile secret/real customer message material.
