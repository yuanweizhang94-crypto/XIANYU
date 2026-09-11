# XIANYU

> ## IMPORTANT — AI / Developer Entry Point
>
> Before operating, repairing, or modifying XIANYU, read:
>
> 1. [`AGENTS.md`](AGENTS.md)
> 2. [`docs/AI_PROJECT_HANDOFF.md`](docs/AI_PROJECT_HANDOFF.md)
> 3. [`docs/DESKTOP_MIGRATION_CLOSURE_20260910.md`](docs/DESKTOP_MIGRATION_CLOSURE_20260910.md) for the completed desktop migration and current machine authority
> 4. [`docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md`](docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md)
> 5. [`docs/CURRENT_PRODUCTION_BASELINE.md`](docs/CURRENT_PRODUCTION_BASELINE.md)
>
> `FIRST_READ=docs/AI_PROJECT_HANDOFF.md`
>
> Mandatory: `UPSTREAM_FIRST`, `LOCAL_EXISTING_CAPABILITY_FIRST`, `CURRENT_RUNTIME_FIRST`, `REUSE_FIRST`, `MINIMAL_PATCH_ONLY`, `NO_PARALLEL_IMPLEMENTATION`, `NO_DUPLICATE_DEVELOPMENT`, `NO_BYPASS`.
>
> Do not create a new implementation until current upstream, current local, and current production runtime capabilities have been verified. Normal requests such as publishing products or querying publish state are `BUSINESS_EXECUTION` by default, not development.

## 2026-09-10 desktop migration closure

The migration from the original Huawei laptop to desktop `PC-20250528MGDP` is complete. The desktop is the current XIANYU production PRIMARY and the laptop is rollback-capable STANDBY.

Current migration authority:

[`docs/DESKTOP_MIGRATION_CLOSURE_20260910.md`](docs/DESKTOP_MIGRATION_CLOSURE_20260910.md)

```text
XIANYU_DESKTOP_MIGRATION_COMPLETE=true
DESKTOP_ROLE=PRIMARY
DESKTOP_PRODUCTION=true
LAPTOP_ROLE=STANDBY
LAPTOP_PRODUCTION=false
PRODUCTION_DOUBLE_RUN=false
```

Do not run laptop and desktop production Scheduler/WebSocket/Auto Reply simultaneously.

## Current XIANYU Web UI

Verified on the desktop production host on 2026-09-11:

```text
XIANYU_WEB_UI=http://127.0.0.1:19000/
XIANYU_ACCOUNTS_UI=http://127.0.0.1:19000/accounts
XIANYU_ONLINE_CHAT_UI=http://127.0.0.1:19000/online-chat-new
```

All three routes returned HTTP 200 during verification. These are loopback URLs for the desktop host; `127.0.0.1` is not a public Internet address and works only from that machine unless a separate LAN/public exposure is explicitly configured.

## Project role

XIANYU uses `zhinianboke/xianyu-auto-reply` as the primary business capability source and execution foundation. XIANYU adds safety governance, minimal patches, validation, release control, evidence, CI, operations, and production hardening around the formal business path.

- User repository: https://github.com/yuanweizhang94-crypto/XIANYU
- XIANYU Upstream: https://github.com/zhinianboke/xianyu-auto-reply
- Execution Infrastructure: https://github.com/yuanweizhang94-crypto/COMPANY_LOCAL_EXECUTION_TOOL
- Global machine handoff: https://github.com/yuanweizhang94-crypto/AI-/blob/main/projects/MACHINE_HANDOFF_20260910.md

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

The current executable Change, when one exists, must be the uniquely dynamically discovered active change directory under `changes/active/`; archived Change directories are historical evidence and must never be treated as executable work.

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

Full cross-project handoff and pre-code proof gate: [`docs/AI_PROJECT_HANDOFF.md`](docs/AI_PROJECT_HANDOFF.md).

Completed desktop migration authority: [`docs/DESKTOP_MIGRATION_CLOSURE_20260910.md`](docs/DESKTOP_MIGRATION_CLOSURE_20260910.md). Historical recovery evidence remains in [`docs/DESKTOP_RECOVERY_HANDOFF_20260910.md`](docs/DESKTOP_RECOVERY_HANDOFF_20260910.md).

Full XIANYU-specific precheck and scope rules: [`docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md`](docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md).

## Current production baseline

The current production authority, including category-state-machine closure, real publish verification, Session rules, status semantics, and official PC-Web limitation behavior, is recorded in:

- [`docs/CURRENT_PRODUCTION_BASELINE.md`](docs/CURRENT_PRODUCTION_BASELINE.md)

The desktop migration is complete. Interpret this dated production baseline together with the current migration closure and current Runtime; the desktop production Runtime is now authoritative.

Historical Change records, ADRs, capability matrices, archived evidence, and older phase notes remain useful as historical evidence, but they do not override current GitHub/local/runtime checks, `AGENTS.md`, the Living Handoff, or the current production baseline.

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

Never commit Cookies, Tokens, JWTs, Authorization headers, passwords, API keys, private keys, QR payloads, browser Profiles, real customer messages, migration data packages, or other secret material.

## Documentation priority

- P0: `AGENTS.md`
- P1: `docs/AI_PROJECT_HANDOFF.md`
- P1: `docs/DESKTOP_MIGRATION_CLOSURE_20260910.md` for current desktop/laptop machine authority
- P1: this README AI/developer entrypoint
- P1: `docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md`
- P1: `docs/CURRENT_PRODUCTION_BASELINE.md`
- P2: architecture/history/ADR/archive evidence

`FIRST_READ=docs/AI_PROJECT_HANDOFF.md`.
