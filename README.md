# XIANYU

> ## IMPORTANT — AI / Developer Execution Rules
>
> Before changing or operating XIANYU, read:
>
> 1. [`AGENTS.md`](AGENTS.md)
> 2. [`docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md`](docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md)
> 3. [`docs/CURRENT_PRODUCTION_BASELINE.md`](docs/CURRENT_PRODUCTION_BASELINE.md)
>
> Mandatory: `UPSTREAM_FIRST`, `LOCAL_EXISTING_CAPABILITY_FIRST`, `CURRENT_RUNTIME_FIRST`, `REUSE_FIRST`, `MINIMAL_PATCH_ONLY`, `NO_PARALLEL_IMPLEMENTATION`, `NO_DUPLICATE_DEVELOPMENT`, `NO_BYPASS`.
>
> Do not create a new implementation until current upstream, current local, and current production runtime capabilities have been verified. Normal requests such as publishing products or querying publish state are `BUSINESS_EXECUTION` by default, not development.

## Project role

XIANYU uses `zhinianboke/xianyu-auto-reply` as the primary business capability source and execution foundation. XIANYU adds safety governance, minimal patches, validation, release control, evidence, CI, operations, and production hardening around the formal business path.

- User repository: https://github.com/yuanweizhang94-crypto/XIANYU
- Upstream business source: https://github.com/zhinianboke/xianyu-auto-reply
- Execution infrastructure: https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL

`UPSTREAM_FIRST=true` does **not** mean overwriting local files with upstream. Read upstream, compare local enhancements/safety fixes, compare current runtime, and sync only the missing delta. `DIFF_BASED_SYNC=true`.

## Formal business execution

For normal product publishing:

```text
receive_attachment
→ xianyu_material_import
→ xianyu_publish_single
→ XIANYU Backend
→ PublishExecutorService
→ XianyuPublisher
→ Goofish official platform flow
```

Do not use `run_program`, `container_run`, temporary scripts, direct imports, or a second publisher to bypass the formal Backend path for real publishing.

Publish state is authoritative only through `SUBMITTED / RUNNING / SUCCESS / FAILED / UNKNOWN`. HTTP 200 alone is not success. `SUCCESS` requires `platform_item_id`, `item_url`, or `AUTHORITATIVE_SYNC_CONFIRMED=true`. `UNKNOWN` is never blindly retried.

## Development gate

Before code is written, compare:

```text
CURRENT_UPSTREAM
vs
CURRENT_LOCAL
vs
CURRENT_RUNTIME
```

The AI/developer must prove the capability is not already available, the runtime is not merely stale/misconfigured, the issue is not Session/data/configuration/platform limitation, and modification to the existing implementation is actually required. Otherwise:

```text
NEW_IMPLEMENTATION_ALLOWED=false
DO_NOT_WRITE_CODE=true
```

Full precheck and scope rules: [`docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md`](docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md).

## Current production baseline

The current production authority, including the 2026-08-12 category-state-machine closure, real publish verification, Session rules, status semantics, and official PC-Web limitation behavior, is recorded in:

- [`docs/CURRENT_PRODUCTION_BASELINE.md`](docs/CURRENT_PRODUCTION_BASELINE.md)

Historical Change records, ADRs, capability matrices, archived evidence, and older phase notes remain useful as historical evidence, but they do not override `AGENTS.md` or the current production baseline.

## Existing capability ownership

Without new direct evidence, do not build second implementations of Account, Cookie, Session, canonical Profile, Material, Publisher, Category, Playwright, Scheduler, WebSocket, Session Renew, QR Login, Browser Lock, Publish Status, Backend Auth, or Material Bridge.

If an existing capability has a defect, repair the existing owner with a minimal patch.

## Platform category authority

`PLATFORM_UI_IS_AUTHORITATIVE=true`.

Use platform auto-selection when available; otherwise read and click real platform candidates and advance through the actual UI state machine. Local semantic logic may rank candidates but must not become a hard gate.

If the platform states that PC Web does not support a category, return `CATEGORY_WEB_UNSUPPORTED` and fail closed. Never force category IDs or choose a false category to bypass the restriction.

## Repository verification

For Repair/Development, use targeted tests, related regression tests, repository verification, then activate only the necessary runtime component. Do not use repeated real-product attempts as a substitute for tests.

## Security

Never commit Cookies, Tokens, JWTs, Authorization headers, passwords, API keys, private keys, QR payloads, browser Profiles, real customer messages, or other secret material.

## Documentation priority

- P0: `AGENTS.md`
- P1: this README AI/developer entrypoint
- P1: `docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md`
- P1: `docs/CURRENT_PRODUCTION_BASELINE.md`
- P2: architecture/history/ADR/archive evidence

`FIRST_READ=AGENTS.md`.
