# CHG-0018 Design

Status: IMPLEMENTING

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

## Upstream capability audit

The design reuses pinned upstream account management, password login refresh, Cookie browser renewal, publish execution, publish page diagnostics, and browser concurrency primitives.

## Pinned upstream evidence

Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.

## Existing local implementation search

Existing local wrapper and prior CHG-0017 evidence are governance and operations assets only. They are not a replacement implementation path.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

The design forbids parallel account stores, Profile stores, browser brokers, queues, senders, Token systems, and publishers.

## Why upstream cannot satisfy the requirement

The pinned upstream behavior needs minimal safety and lifecycle patches to meet the owner's credential and publish readiness requirements.

## Approved exception ADR

Not applicable.

## Component owner

Pinned upstream remains the runtime owner; XIANYU owns the governance patch artifact.

## Retirement plan for overlapping local code

No overlapping local production code is introduced.
