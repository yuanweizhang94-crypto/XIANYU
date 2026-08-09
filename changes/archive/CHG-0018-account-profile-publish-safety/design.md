# CHG-0018 Design

Status: ARCHIVED

Change ID: CHG-0018-account-profile-publish-safety

## Design

P0 changes account credential handling without changing production account data. Account list/detail responses must not expose raw `login_password`. Existing `has_password` semantics are checked before reuse; if incompatible, a separate credential-presence field is added. The existing account edit page gains a deliberate credential-editing mode or equivalent safe surface; default edit mode does not load, show, or submit passwords.

P0 also changes password refresh failures so `no_credentials` and `bad_credentials` use existing login logs, cooldowns, notifications, and failure classifications without modifying `XYAccount.status`.

P1 keeps the current publisher and publish steps. Publish execution passes authoritative `account_id` directly to the publisher or as a backward-compatible optional keyword. Profile code reads the latest Cookie from the authoritative account record and must not accept arbitrary `account_id` plus caller-provided Cookie pairs.

P2 separates API Cookie renewal from Profile initialization. API renewal writes Cookie and releases its task resources, then checks Profile presence. Existing healthy Profiles are not opened. Missing Profiles may initialize after locks are released; unhealthy existing Profiles return diagnostics unless the user explicitly repairs them.

P3 extracts a shared `preflight_publish_form(context)` or equivalent from CHG-0017 diagnostics. Preflight-only opens and closes one Profile context. Formal publish opens one Profile context, runs shared preflight, and if ready continues filling and publishing inside the same context.

P4 first confirms the existing responsibilities of `run_browser_task`, account locks, and global browser slots. Only publish, preflight, and Profile initialization are changed where missing or proven duplicate. Cookie renewal and password login are not refactored for symmetry.

The auto-polish hardening stays inside pinned upstream scheduler services. `day_switch_task` fail-closes Redis read/update failures before resetting polish state. `polish_task` checks platform-day readiness before item processing, supports optional internal account scope and per-account item limit for canaries, masks account/item identifiers in touched polish logs, treats duplicate polish responses as successful same-day completion, and only schedules existing password login recovery when complete automatic-login credentials exist.

The real batch publish recovery keeps the upstream-native publisher as the only executor. The backend batch service now passes authoritative `account_id` and `owner_id` into `XianyuPublisher.publish_item`, and each concrete publish attempt opens the canonical persistent Profile, runs shared preflight, publishes in the same context, then closes it. The canonical Profile root is provided by the existing Cookie browser renewal/Profile service and is mounted into both backend and websocket containers as the same persistent `browser_data` volume.

Publish-page readiness is classified by a single 60-second polling path. The preflight no longer visits the login page first or treats arbitrary controls as a ready form. It returns specific existing-style failure reasons for `login_required`, `manual_verification_required`, `runtime_profile_path_mismatch`, `browser_busy`, `publish_page_load_failed`, and `publish_form_timeout`.

Runtime enablement keeps the existing scheduler process model. The production canary enables only `day_switch`, `fetch_items`, and `polish` in `xy_scheduled_tasks`; all order, delivery, direct-message, token-renewal, and unrelated scheduler tasks remain disabled.

The exact-item/no-retry extension remains inside the same upstream-native scheduler and item-list methods. `PolishTaskService.execute` accepts default-off `platform_item_ids` and a backward-compatible `retry_on_token_expiry=True` control. Exact item scope is applied in the existing SQL `SELECT` together with account ownership, active account, `auto_polish`, session cooldown, unpolished state, and item limit. Item-list Token recovery is bounded to one retry; any rotated Cookie fields are persisted through the existing `merge_account_cookie_fields` path so later polish does not reload stale account Cookie state. The polish MTop method itself remains single-request and non-recursive; `PolishTaskService` may perform one native item-list auth recovery and one final polish retry only for explicit Session/Token expiry. No service, HTTP API, scheduler task, model, table, Cookie manager, Token system, or execution owner is added.

Final production verification confirmed the lifecycle in the existing execution path: account `2219319284219` and four exact platform item IDs each returned explicit `SUCCESS::调用成功` on one polish request and each transitioned `is_polished=false -> true`, with zero auth failures and zero out-of-scope requests. The final Vendor Patch SHA256 is `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`, and the production Scheduler image is `xianyu-chg0018-scheduler:56d62e2-94c8682`.

Production global polish is re-enabled only through the existing scheduled-task management path; its interval is unchanged and `day_switch` remains enabled. One natural Scheduler cycle demonstrated that explicit successes continue normally, Session-expired accounts perform at most one bounded recovery attempt and stop that account on failure, later accounts continue, and the Scheduler remains running with `RestartCount=0`. Individual account Session expiry is therefore an operational account-health condition rather than a CHG-0018 code defect once the fail-closed bounded behavior is preserved.

Repository governance does not define a `VERIFIED` status. Because the next formal state is merge-bound `MERGED` and PR #26 is explicitly required to remain Draft/Open/Unmerged, final production verification does not fabricate a new state or advance the Change past `VERIFYING`.

## Upstream capability audit

The design reuses pinned upstream account management, password login refresh, Cookie browser renewal, publish execution, publish page diagnostics, and browser concurrency primitives.

## Pinned upstream evidence

Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.

## Existing local implementation search

Existing local wrapper and prior CHG-0017 evidence are governance and operations assets only. They are not a replacement implementation path.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

The design forbids parallel account stores, Profile stores, browser brokers, queues, senders, Token systems, and publishers. The exact-item/no-retry extension changes only optional parameters and filters in existing methods, so duplicate-development risk remains low.

## Why upstream cannot satisfy the requirement

The pinned upstream behavior needs minimal safety and lifecycle patches to meet the owner's credential and publish readiness requirements.

## Approved exception ADR

Not applicable.

## Component owner

Pinned upstream remains the runtime owner; XIANYU owns the governance patch artifact.

## Retirement plan for overlapping local code

No overlapping local production code is introduced. Rollback is removal of the optional parameters from the existing methods or restoration of the prior scheduler image; no data migration is required.

## Post-merge archive closeout

PR #31 merged at `64c37d20a00f77d7e860705123244692d134dd48`; the verified design is preserved under `changes/archive` without further runtime modification.
