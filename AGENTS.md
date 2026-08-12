# XIANYU AI EXECUTION RULES

PRIORITY=HIGHEST

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

> FIRST_READ=AGENTS.md. These rules apply to every AI, Codex/ChatGPT agent, automation agent, and developer before operating, developing, repairing, or troubleshooting XIANYU.

## Mandatory before writing code

Before any code modification, the AI MUST prove all of the following:

1. The current upstream does not already provide the required capability.
2. The current XIANYU local code does not already provide the required capability.
3. The current production runtime is actually running the expected current code.
4. The problem is not caused only by configuration, stale runtime/image/container, an unloaded patch, service/scheduler state, Session/account state, material/data state, backend authentication, browser lock, an incorrect invocation, or an official platform limitation.
5. A modification to the existing implementation is actually necessary.

If any condition is not proven:

NEW_IMPLEMENTATION_ALLOWED=false
DO_NOT_WRITE_CODE=true

Do not create a parallel implementation. Do not build a workaround around the formal XIANYU flow.

## Mandatory development precheck

Before Repair or Development, record:

```text
DEVELOPMENT_PRECHECK
TASK_TYPE=BUSINESS_EXECUTION / REPAIR / DEVELOPMENT
FAILURE_REASON=
RESPONSIBLE_LAYER=
CURRENT_UPSTREAM_CAPABILITY=
CURRENT_LOCAL_CAPABILITY=
CURRENT_RUNTIME_CAPABILITY=
CONFIGURATION_ISSUE=
SESSION_OR_DATA_ISSUE=
OFFICIAL_PLATFORM_LIMITATION=
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=
```

If `CURRENT_UPSTREAM_CAPABILITY=EXISTS`, `CURRENT_LOCAL_CAPABILITY=EXISTS`, or `CURRENT_RUNTIME_CAPABILITY=STALE_ONLY`, default to:

```text
NEW_IMPLEMENTATION_ALLOWED=false
```

Prefer `REUSE`, `CONFIG_FIX`, `RUNTIME_ACTIVATION`, or `MINIMAL_EXISTING_FUNCTION_FIX`.

## Task classification is mandatory

User requests such as “发布商品”, “继续发布”, “发布这些图片”, or “查询发布状态” are BUSINESS_EXECUTION by default. Do not automatically turn normal business execution into audit, development, Canary, refactor, upstream sync, broad source search, Docker rebuild, or source modification.

Only escalate when a formal business call returns a system-level failure with direct evidence.

## Formal business execution path

```text
receive_attachment
→ xianyu_material_import
→ xianyu_publish_single
→ XIANYU Backend
→ PublishExecutorService
→ XianyuPublisher
→ Goofish official platform flow
```

Normal real business execution must not use:

- `run_program` for real publish
- `container_run` for real publish
- temporary Python/Node publish scripts
- direct import of `execute_single_publish`
- direct import of Publisher
- a second Playwright publisher
- direct bypass of the formal Backend

## Existing capability first

The following capability families already exist and MUST NOT be reimplemented without new direct evidence that the existing implementation is absent or fundamentally unusable:

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

If one contains a defect, repair the existing implementation. Do not copy, bypass, or build a parallel owner.

## Upstream First means compare, not overwrite

Upstream business source: https://github.com/zhinianboke/xianyu-auto-reply

Correct order:

```text
READ CURRENT UPSTREAM
→ UNDERSTAND NATIVE CAPABILITY
→ COMPARE CURRENT LOCAL
→ PRESERVE LOCAL SAFETY/ENHANCEMENTS
→ SYNC ONLY THE ACTUALLY MISSING PART
```

Never overwrite an entire local file merely because upstream has a version of it. XIANYU may contain local safety behavior that is ahead of upstream. `DIFF_BASED_SYNC=true`.

## Runtime First

When source appears fixed but behavior still fails, verify:

```text
CURRENT_SOURCE
CURRENT_IMAGE
CURRENT_CONTAINER
CURRENT_RUNTIME
```

If source is image-baked, activate only the necessary image/container, perform health checks, and verify runtime source. Never use real product retries to discover that a patch was never loaded.

## Stop Patch → Try → Patch → Try

If the same issue has already received two fixes without resolution: STOP. Do not add a third isolated patch.

Perform a complete comparison:

```text
CURRENT_UPSTREAM
vs
CURRENT_LOCAL
vs
CURRENT_RUNTIME
```

Then complete one controlled closure:

```text
ROOT_CAUSE
→ SINGLE_STATE_MACHINE
→ REMOVE_DUPLICATE_PATHS
→ TARGETED_TESTS
→ REGRESSION_TESTS
→ RUNTIME_ACTIVATION
→ STOP
```

Preferred sequence: Observe → Classify → Compare → Root Cause → Minimal Patch → Tests → Activate → Stop.

## Category authority

PLATFORM_UI_IS_AUTHORITATIVE=true.

Current formal category model:

```text
platform auto-selected category → reuse it
otherwise:
read real platform candidates
→ semantic logic may rank/assist only
→ click a real candidate
→ observe UI state machine
```

Supported states:

- `FINAL_SELECTED`
- `NEXT_LEVEL_REQUIRED`
- `CLICK_NOT_EFFECTIVE`
- `PC_WEB_UNSUPPORTED`
- `LOGIN_REQUIRED`
- `PLATFORM_VERIFICATION_REQUIRED`

`MAX_CATEGORY_LEVELS=5`.

Do not return `no_supported_category` solely because of `LOCAL_MAPPING_MISS`, `SEMANTIC_GATE_MISS`, or `SELECTED_CLASS_NOT_FOUND`.

Do not reintroduce `SELECTED_CONFIRMED` as a local semantic hard gate without new platform evidence. Do not create a second category selector.

## Official PC Web limitation

If the platform explicitly reports “网页版暂不支持发布此分类”:

```text
CATEGORY_WEB_UNSUPPORTED
→ FAIL_CLOSED
```

Do not force `categoryId`, force `channelCatId`, select an incorrect category, fabricate a category, or bypass the platform restriction. This is an `OFFICIAL_PLATFORM_LIMITATION`, not a new development requirement.

## Publish status semantics

HTTP 200 is not publish success.

Formal states:

- `SUBMITTED`
- `RUNNING`
- `SUCCESS`
- `FAILED`
- `UNKNOWN`

`SUCCESS` requires at least one authoritative signal:

- `platform_item_id`, or
- `item_url`, or
- `AUTHORITATIVE_SYNC_CONFIRMED=true`.

`UNKNOWN` must never trigger a blind retry.

## 502 / timeout with side effects

A connector 502, timeout, or connection error does not prove the Windows/platform action did not execute.

For publish, Git, or file mutation:

```text
STOP_NEW_EXECUTION
→ READ_ONLY_STATUS_RECOVERY
→ SUCCESS / FAILED / UNKNOWN
```

If `UNKNOWN`, do not execute again until authoritative state is recovered.

## Session authority

Final account publish readiness is `REAL_BROWSER_LOGIN_READY`, not merely Cookie presence, Profile presence, or a database `healthy` flag.

Production Session maintenance uses the established Session renewal path. Do not create overlapping schedulers or a second renewal system.

If a real page requires human QR verification during normal business execution, skip that account and use another healthy account. One account must not block the whole batch.

## Change scope discipline

Every Repair/Development must define:

```text
ALLOWED_CHANGE_SCOPE=
FORBIDDEN_CHANGE_SCOPE=
```

Do not perform “while we are here” optimizations. Do not cross responsibility layers.

## Testing discipline

Repair sequence:

```text
TARGETED_TESTS
→ RELATED_REGRESSION_TESTS
→ REPOSITORY_VERIFY
→ RUNTIME_ACTIVATION
→ STOP
```

Do not substitute real product actions for tests. During Repair, default `REAL_PRODUCT_ACTIONS=0`. After tests and runtime activation are complete, stop development; execute real publishing only as a separate normal business task.

## Responsibility layers

- MCP / Proxy / Runner: `COMPANY_LOCAL_EXECUTION_TOOL`
- Attachment persistence: `COMPANY_LOCAL_EXECUTION_TOOL`
- Business Adapter transport: `COMPANY_LOCAL_EXECUTION_TOOL`
- Material / Publisher / Category / Session / Profile / Account / Scheduler: `XIANYU`
- QR / Slider / Face / official verification: `Official Platform / Human Interaction`
- `CATEGORY_WEB_UNSUPPORTED`: `Official Platform Limitation`

Execution infrastructure: https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL

Do not develop across layers to hide the actual owner of a failure.

## Permanent prohibited development patterns

- duplicate wheels
- parallel architecture
- second Publisher
- second Login
- second Session Renew
- second Profile Manager
- second Material system
- second Category system
- second Business Adapter
- temporary publish bypass
- evidence-free global refactor
- evidence-free large source modification
- repeated real-product Canary trial-and-error
- blind retry of UNKNOWN
- whole-file upstream overwrite that removes local safety improvements

## Security

Never commit Cookie values, Tokens, JWTs, Authorization headers, passwords, API keys, private keys, QR payloads, browser Profiles, real customer messages, or other secret material. Use state names and redacted placeholders only.

## Required reading

1. `AGENTS.md`
2. `docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md`
3. `docs/CURRENT_PRODUCTION_BASELINE.md`
4. `docs/UPSTREAM_FIRST_POLICY.md`
5. `docs/UPSTREAM_CAPABILITY_MATRIX.md`
6. Current active Change/spec/acceptance files only when the task is actually Repair/Development and such a Change is applicable.

No lower-priority historical document may weaken these P0 rules.
