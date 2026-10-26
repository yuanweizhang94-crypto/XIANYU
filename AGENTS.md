# XIANYU — Current Agent Rules

DATE=2026-10-26
STATUS=CURRENT_CANONICAL_ROOT_RULES
PRIORITY=HIGHEST_FOR_THIS_REPOSITORY

XIANYU is the authority for the user's Xianyu business implementation and production behavior.

## Context and takeover

Canonical cross-project policy:
`AI-/governance/EXECUTION_CONTEXT_AND_ROTATION_POLICY.md`.

Project Commander/failover reads broadly as needed. Ordinary bounded Executor reads:

```text
XIANYU_LATEST_MAIN
+ EXACT_COMMAND
+ EXACT_CURRENT_CHECKPOINT_OR_RESULT
+ DIRECT_DEPENDENCY_CONTRACT_ONLY_WHEN_REQUIRED
```

Do **not** require every new Executor to fully restore ZIDONGZHUA + COMPANY + XIANYU + AI24.

For broad ZIDONGZHUA/XIANYU Commander reconciliation only, use the current Commander-aware protocol:
`zidongzhua/docs/UNIVERSAL_AI_HANDOFF_PROTOCOL.md`.

## Business execution default

Requests such as publish/query/update/status are business execution by default.

```text
BUSINESS_EXECUTION_BY_DEFAULT=true
UPSTREAM_FIRST=true
LOCAL_EXISTING_CAPABILITY_FIRST=true
CURRENT_RUNTIME_FIRST=true
REUSE_FIRST=true
MINIMAL_PATCH_ONLY=true
NO_PARALLEL_IMPLEMENTATION=true
NO_BYPASS=true
UNKNOWN_NEVER_BLIND_RETRY=true
PLATFORM_UI_IS_AUTHORITATIVE=true
```

Do not convert normal business execution into broad development/audit work without direct system-failure evidence.

## Ownership

XIANYU owns Xianyu business semantics such as Account, Session/Cookie lifecycle, Profile, Material, Publisher, Category, WebSocket, Auto Reply, Orders and Scheduler.

COMPANY owns shared execution transport/tools/thin adapters. ZIDONGZHUA owns business operating state and decisions.

```text
XIANYU_BUSINESS_LOGIC_STAYS_IN_XIANYU=true
COMPANY_THIN_ADAPTER_ONLY=true
ZIDONGZHUA_OPERATING_STATE_STAYS_IN_ZIDONGZHUA=true
```

## Pre-code proof

Before modifying XIANYU source, determine:

```text
TASK_TYPE=BUSINESS_EXECUTION|REPAIR|DEVELOPMENT
CURRENT_UPSTREAM_CAPABILITY=
CURRENT_LOCAL_CAPABILITY=
CURRENT_RUNTIME_CAPABILITY=
CONFIG_SESSION_DATA_ONLY=
OFFICIAL_PLATFORM_LIMITATION=
MINIMAL_EXISTING_OWNER_TO_CHANGE=
WHY_SOURCE_CHANGE_IS_REQUIRED=
```

If current capability exists or runtime/config/session/data is the real issue, reuse/repair/reconcile instead of creating another implementation.

## Production truth

Static documents must not hard-code current account counts, session counts, PID, tool count or other fast-moving production facts as current authority.

```text
FRESH_RUNTIME_AND_PLATFORM > STATIC_SNAPSHOT
```

Use `docs/AI_PROJECT_HANDOFF.md` and `docs/CURRENT_PRODUCTION_BASELINE.md` as durable capability/history references, then read fresh Runtime for current production state.

## Persistence

Update only materially affected repositories:
- XIANYU implementation/runtime fact → XIANYU;
- COMPANY tool/transport contract → COMPANY;
- business operating state → ZIDONGZHUA.

No empty commits and no forced three-repository sync for unrelated changes.

## Security

Never commit Cookie/Token/JWT/Authorization/password/API key/private key/QR payload/browser-profile secret/customer-private data.

The previous long-form `AGENTS.md` is preserved under `archive/20261026/` and no longer acts as current root authority.
