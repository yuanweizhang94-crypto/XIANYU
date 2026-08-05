# CHG-0018 Account Profile Publish Safety

Status: VERIFYING

Change ID: CHG-0018-account-profile-publish-safety

## Execution contract

User outcome: prevent account credential mis-save and false account disablement, then make publish readiness reuse the account's persistent upstream browser Profile without production side effects.

Confirmed blocker: CHG-0017 is suspended because the owner approved priority repair for raw password exposure, shared credential editing, bad/no credential disablement, missing publish Profile, publish preflight gaps, and browser mutual-exclusion gaps.

Smallest success test: P0 prevents raw password return and false disablement; P1-P4 prove publish preflight and formal publish use one locked account Profile lifecycle without real account operation.

## Scope

- P0: secure account credential responses and editing, and prevent no/bad credentials from disabling accounts.
- P1: make publish reuse authoritative account persistent Profile.
- P2: initialize or repair Profile only when missing or explicitly requested.
- P3: share read-only publish preflight diagnostics with formal publish.
- P4: use the existing canonical browser locking/slot combination exactly once per task.
- Runtime expansion: complete CANARY-A01 UI/Profile/preflight validation and harden the pinned upstream native auto-polish chain for one scoped canary item without product creation, product publish, or test messages.

## Upstream capability audit

Pinned upstream was inspected for existing account management, password login refresh, Cookie browser renewal, publish execution, publish diagnostics, and browser concurrency primitives.

## Pinned upstream evidence

Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.

Evidence paths include upstream account routes and schemas, `common/services/cookie_renew_browser_service.py`, `common/services/captcha/concurrency.py`, `backend-web/app/services/xianyu_publisher.py`, `common/services/publish_execution_service.py`, and CHG-0017 publish diagnostics tests.

## Existing local implementation search

Local governance, wrapper, and prior CHG-0017 evidence were searched. No local replacement publisher, Token system, WebSocket, sender, queue, or browser broker is approved for this Change.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Risk is controlled by patching the pinned upstream paths already used by CHG-0017. The Change must not create a second Profile manager, sender, publisher, login system, browser broker, queue, or database table.

## Why upstream cannot satisfy the requirement

Pinned upstream currently returns raw saved login password through account APIs, uses the same edit surface for normal account data and credentials, disables accounts for no/bad password refresh outcomes, and does not prove publish uses the same persistent account Profile and preflight lifecycle.

## Approved exception ADR

Not applicable because this is a pinned upstream patch, not a local replacement capability.

## Component owner

Pinned upstream account, publish, and browser lifecycle paths remain the owner. XIANYU governance owns the patch artifact and acceptance evidence.

## Retirement plan for overlapping local code

No overlapping local production code is added. The patch can be retired when upstream natively provides equivalent credential safety and publish Profile readiness behavior.

## Allowed files

Allowed changes are limited to CHG-0018 governance files, governance-generated state, targeted tests, the independent CHG-0018 vendor patch artifact, the pinned upstream files required by P0-P4, and the pinned upstream native scheduler files required to safely execute the authorized CANARY-A01 auto-polish canary.

## Forbidden work

No database tables, services, queues, Browser Broker, sender, Token system, login system, Docker/Compose changes, real account operation, real publish, message sending, CHG-0017 T17, PR #26 state change, archive, or merge.

The runtime expansion must reuse upstream native scheduler paths and must not create a second polish service, task queue, table, browser polish implementation, sender, or account runtime.

## Rollback boundary

Implementation commits must preserve three auditable boundaries: P0 safety, P1-P4 Profile readiness, and tests/vendor patch/evidence.

## Runtime closeout summary

- Target alias: `CANARY-A01`.
- Frontend CHG-0018 image deployed without restarting WebSocket, backend, MySQL, or Redis.
- Credential UI/API safety remained in effect during the canary: no raw password response path is accepted, and the target account has no automatic-login username or password configured.
- Persistent Profile creation and read-only publish preflight completed without product creation, product publish, upload, or message sending.
- Auto-polish used the pinned upstream native scheduler path, with `day_switch`, `fetch_items`, and `polish` as the only enabled scheduler tasks.
- One scoped canary item was polished through `PolishTaskService.execute(account_ids=..., max_items_per_account=1)`, then the single scheduler handled only remaining CANARY-A01 eligible items.
- Other accounts kept `auto_polish=false`; follow-up owner approval is required before enabling auto-polish for any other account.
