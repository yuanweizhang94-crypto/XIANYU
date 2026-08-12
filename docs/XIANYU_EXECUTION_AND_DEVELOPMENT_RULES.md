# XIANYU Execution and Development Rules

Baseline: **2026-08-12 22:33 Asia/Taipei (UTC+8)**

Priority: **P1 authoritative development/operation rule set**. Root `AGENTS.md` is P0 and MUST be read first.

## 1. Core principles

```text
UPSTREAM_FIRST=true
LOCAL_EXISTING_CAPABILITY_FIRST=true
CURRENT_RUNTIME_FIRST=true
REUSE_FIRST=true
MINIMAL_PATCH_ONLY=true
NO_PARALLEL_IMPLEMENTATION=true
NO_DUPLICATE_DEVELOPMENT=true
NO_BYPASS=true
BUSINESS_EXECUTION_BY_DEFAULT=true
PLATFORM_UI_IS_AUTHORITATIVE=true
PLATFORM_LIMITATION_FAIL_CLOSED=true
UNKNOWN_NEVER_BLIND_RETRY=true
DIFF_BASED_SYNC=true
```

XIANYU user repository: https://github.com/yuanweizhang94-crypto/XIANYU

Business upstream: https://github.com/zhinianboke/xianyu-auto-reply

Execution infrastructure: https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL

Upstream is a reference and capability source. Do not modify upstream as part of XIANYU work.

## 2. Mandatory pre-code proof

Before any code modification, prove:

1. Current upstream does not already provide the capability/fix.
2. Current local XIANYU does not already implement the capability/fix.
3. Current production Runtime is running the expected source/image/container/configuration.
4. The observed failure is not only configuration, stale Runtime, unloaded patch, service restart, scheduler state, Session/account state, material/data state, backend authentication, browser lock, incorrect invocation, or official platform limitation.
5. The problem can only be correctly solved by modifying the existing implementation.

If any proof is missing:

```text
NEW_IMPLEMENTATION_ALLOWED=false
DO_NOT_WRITE_CODE=true
```

Do not create a parallel implementation or workaround around the formal XIANYU flow.

## 3. DEVELOPMENT_PRECHECK

Every Repair/Development must record:

```text
DEVELOPMENT_PRECHECK
1. TASK_TYPE=BUSINESS_EXECUTION / REPAIR / DEVELOPMENT
2. FAILURE_REASON=
3. RESPONSIBLE_LAYER=
4. CURRENT_UPSTREAM_CAPABILITY=
5. CURRENT_LOCAL_CAPABILITY=
6. CURRENT_RUNTIME_CAPABILITY=
7. CONFIGURATION_ISSUE=
8. SESSION_OR_DATA_ISSUE=
9. OFFICIAL_PLATFORM_LIMITATION=
10. MINIMAL_EXISTING_FUNCTION_TO_CHANGE=
11. WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=
12. WHY_NEW_IMPLEMENTATION_IS_REQUIRED=
```

If upstream/local capability exists, or Runtime is stale only, default to reuse/configuration correction/runtime activation/minimal existing-function repair.

## 4. Normal business execution is the default

User requests such as:

- 发布商品
- 继续发布
- 发布这些图片
- 查询发布状态

are `BUSINESS_EXECUTION` by default.

Do not automatically escalate to audit, upstream research, source-wide investigation, development, Canary, refactor, Docker rebuild, or source modification.

Escalation requires direct evidence from the formal business path of a system-level failure.

## 5. Formal product publish flow

```text
receive_attachment
→ xianyu_material_import
→ xianyu_publish_single
→ XIANYU Backend
→ POST /api/v1/product-publish/publish/batch
→ PublishExecutorService
→ execute_single_publish
→ publish_single_item
→ XianyuPublisher
→ Goofish official platform flow
```

Real publish must not use:

- `run_program`
- `container_run`
- temporary Python/Node scripts
- direct import `execute_single_publish`
- direct import Publisher
- a second Playwright publisher
- direct bypass of XIANYU Backend

## 6. Existing capability ownership

The following capability families already exist. Without new direct evidence, do not implement a second copy:

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

If a bug exists, repair the existing owner.

## 7. Upstream First correct behavior

`UPSTREAM_FIRST` means:

```text
read current upstream
→ understand upstream native capability
→ compare current local
→ identify local enhancements/safety behavior
→ sync only truly missing deltas
```

It does not mean full-file upstream overwrite.

XIANYU may contain Publisher safety behavior ahead of upstream. Preserve local safety fixes unless current evidence proves they are obsolete.

`DIFF_BASED_SYNC=true`.

## 8. Runtime First

For “source is fixed but behavior still fails”, verify:

```text
CURRENT_SOURCE
CURRENT_IMAGE
CURRENT_CONTAINER
CURRENT_RUNTIME
```

If `IMAGE_BAKED_SOURCE=true`, after a source change:

```text
rebuild only necessary image
→ replace only necessary container
→ health check
→ verify runtime source
```

Never leave Runtime stale, retry a real product, then add another patch because the previous fix appeared ineffective.

## 9. Patch discipline

If the same problem has already been patched twice and remains unresolved: STOP.

Mandatory next action:

```text
CURRENT_UPSTREAM
vs
CURRENT_LOCAL
vs
CURRENT_RUNTIME
```

Then one closure:

```text
ROOT_CAUSE
→ SINGLE_STATE_MACHINE
→ REMOVE_DUPLICATE_PATHS
→ TARGETED_TESTS
→ REGRESSION_TESTS
→ RUNTIME_ACTIVATION
→ STOP
```

Correct sequence:

```text
Observe
→ Classify
→ Compare
→ Root Cause
→ Minimal Patch
→ Tests
→ Activate
→ Stop
```

Forbidden sequence:

```text
Patch
→ Try
→ Patch
→ Try
→ Patch
→ Try
```

## 10. Category incident and permanent lesson

On **2026-08-12**, category selection was confirmed to have real platform candidates with:

```text
UI_VISIBLE=true
UI_SELECTABLE=true
CLICK_SUCCEEDED=true
```

The local post-CHG-0018 logic then used `SELECTED_CONFIRMED` as an over-restrictive gate and required the category field text to immediately equal the clicked candidate. The platform could already have advanced by closing the popup, entering a next level, updating internal state/breadcrumb, or changing active/checked state, while local logic still returned false and ultimately `no_supported_category`.

Root cause:

```text
OVERRESTRICTIVE_SELECTED_CONFIRMED_GATE
```

Final closure:

```text
PLATFORM_UI_FIRST_RESTORED=true
SINGLE_CATEGORY_STATE_MACHINE=true
MULTI_LEVEL_CATEGORY_SUPPORTED=true
LOCAL_SEMANTIC_HARD_GATE=false
```

Without new direct platform evidence, do not reintroduce `SELECTED_CONFIRMED` as a semantic hard gate and do not develop a second category selector.

## 11. Current category state machine

Authority: `PLATFORM_UI`.

If platform auto-selects a category, reuse it.

Otherwise:

```text
read real platform candidates
→ semantic logic may rank/assist only
→ click real candidate
→ observe real UI transition/state
```

Supported states:

```text
FINAL_SELECTED
NEXT_LEVEL_REQUIRED
CLICK_NOT_EFFECTIVE
PC_WEB_UNSUPPORTED
LOGIN_REQUIRED
PLATFORM_VERIFICATION_REQUIRED
```

`MAX_CATEGORY_LEVELS=5`.

Do not return `no_supported_category` solely from:

```text
LOCAL_MAPPING_MISS
SEMANTIC_GATE_MISS
SELECTED_CLASS_NOT_FOUND
```

## 12. PC Web official limitation

If the platform explicitly shows “网页版暂不支持发布此分类”:

```text
CATEGORY_WEB_UNSUPPORTED
→ FAIL_CLOSED
```

Forbidden:

- force `categoryId`
- force `channelCatId`
- choose a false/irrelevant category
- fabricate category state
- bypass the official limitation

This is `OFFICIAL_PLATFORM_LIMITATION`, not a development request.

## 13. Real publish verification baseline

The 2026-08-12 final controlled production verification of the original five items produced:

```text
Material 9  → SUCCESS → platform_item_id=1075653752858
Material 8  → SUCCESS → platform_item_id=1074662425907
Material 7  → SUCCESS → platform_item_id=1073635950977
Material 6  → SUCCESS → platform_item_id=1073637026044
Material 10 → CATEGORY_WEB_UNSUPPORTED
```

Therefore:

```text
PUBLISH_FLOW_FIXED=true
CATEGORY_STATE_MACHINE_FIXED=true
SESSION_FLOW_WORKING=true
REAL_PUBLISH_VERIFIED=true
REMAINING_SYSTEM_BLOCKER=NONE
```

For later ordinary failures, read the new `failure_reason`. Do not assume “Publisher is broken again”.

## 14. Session production rule

Final account readiness authority:

```text
REAL_BROWSER_LOGIN_READY
```

Do not equate Cookie presence, Profile presence, or DB `healthy` with a valid platform Session.

Current production Session maintenance uses the established background renewal path:

```text
API_COOKIE_RENEW_ENABLED=true
RENEW_INTERVAL_SECONDS=3600
```

Do not enable multiple overlapping Session schedulers.

If a real page requires human QR verification during normal business execution:

```text
skip account
→ use next healthy account
```

One unhealthy account must not block the whole batch.

## 15. Publish status semantics

HTTP 200 and “task submitted” mean only `SUBMITTED`.

Formal states:

```text
SUBMITTED
RUNNING
SUCCESS
FAILED
UNKNOWN
```

`SUCCESS` requires at least one:

```text
platform_item_id exists
item_url exists
AUTHORITATIVE_SYNC_CONFIRMED=true
```

`UNKNOWN` is never blindly retried.

## 16. 502 / timeout rule

A 502/timeout/connection error cannot prove a side-effecting Windows action did not run.

For real publish, Git mutation, or file mutation:

```text
STOP_NEW_EXECUTION
→ READ_ONLY_STATUS_RECOVERY
→ SUCCESS / FAILED / UNKNOWN
```

If `UNKNOWN`, do not execute again.

## 17. Responsibility-layer classification

```text
MCP / Proxy / Runner
→ COMPANY_LOCAL_EXECUTION_TOOL

Attachment persistence
→ COMPANY_LOCAL_EXECUTION_TOOL

Business Adapter transport
→ COMPANY_LOCAL_EXECUTION_TOOL

Material / Publisher / Category / Session / Profile / Account / Scheduler
→ XIANYU

QR / Slider / Face / official verification
→ Official Platform / Human Interaction

CATEGORY_WEB_UNSUPPORTED
→ Official Platform Limitation
```

Do not fix a failure in the wrong repository/layer.

## 18. Change scope

Before Repair/Development:

```text
ALLOWED_CHANGE_SCOPE=
FORBIDDEN_CHANGE_SCOPE=
```

Example for a category defect:

Allowed: Publisher category state machine, related tests, necessary Runtime activation.

Forbidden unless separately evidenced: Material, Session, Business Adapter, Scheduler, WebSocket, Database.

No “while we are here” optimization.

## 19. Test discipline

Repair must follow:

```text
TARGETED_TESTS
→ RELATED_REGRESSION_TESTS
→ REPOSITORY_VERIFY
→ RUNTIME_ACTIVATION
```

Real product actions are not a substitute for tests.

During Repair:

```text
REAL_PRODUCT_ACTIONS=0
```

After tests and Runtime activation complete, stop development. Real publish belongs to a separate normal business task.

## 20. Permanent prohibited patterns

- duplicate development
- parallel architecture
- second Publisher
- second Login
- second Renew
- second Profile Manager
- second Material system
- second Category system
- second Business Adapter
- temporary real-publish bypass
- evidence-free global refactor
- evidence-free broad source changes
- repeated real-product Canary trial-and-error
- blind retry after UNKNOWN
- full-file upstream overwrite that removes local enhancements/safety fixes

## 21. Documentation priority

```text
P0 /AGENTS.md
P1 /README.md AI/Developer entrypoint
P1 /docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md
P1 /docs/CURRENT_PRODUCTION_BASELINE.md
P2 architecture / ADR / history / archived Change records
```

Any AI starts with `FIRST_READ=AGENTS.md`.

## 22. Security

Never store or commit Cookie values, Tokens, JWTs, Authorization headers, passwords, API keys, private keys, QR payloads, browser Profile secrets, real customer messages, or other secret material.
