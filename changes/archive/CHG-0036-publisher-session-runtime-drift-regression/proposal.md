# CHG-0036 Publisher Session Runtime Drift Regression

Change ID: CHG-0036-publisher-session-runtime-drift-regression
Status: ARCHIVED
Created: 2026-08-30
Owner task: publisher_session_runtime_drift_final_closure

## User Outcome

User outcome: preserve the already-correct canonical Publisher cookie/session flow in GitHub, remove the proven production-only `await session.refresh(account)` drift by rebuilding Backend from canonical source, and complete Material 94-103 zero-publish preflight.

Confirmed blocker: production Backend contains unsourced runtime drift in `backend-web/app/services/publish_execution_service.py`; canonical pinned upstream uses capability `cookies_str -> account.cookie` and is already correct.

Smallest success test: regression tests prove refreshed capability cookies reach only the matching Publisher, the forbidden runtime pattern is absent after clean replay and production activation, Material 94 reaches a blocked transport boundary with zero real platform requests, and Materials 94-103 pass read-only preflight.

## Scope

Allowed:

- isolated clean XIANYU worktree based on current remote main;
- regression/drift-guard tests and sanitized governance/evidence only;
- upstream pinned-source test artifact generation without changing canonical business logic;
- clean replay verification;
- targeted tests, repository verify, diff check, secret scan;
- Git branch/PR/CI/merge closure;
- Backend-only clean build and activation through the existing safe lifecycle path;
- read-only account/chat/material preflight and hard-blocked publish dry-run with zero platform writes.

Forbidden:

- modifying the historical dirty `D:/xianyu` checkout;
- changing canonical Publisher business logic merely to create a fix commit;
- mechanically replacing the bad runtime line with `await self.session.refresh(account)`;
- real publish for Materials 94-103;
- auto-reply configuration, message send, order mutation, account-state changes;
- frontend, WebSocket, Scheduler, MySQL, Redis or Profile replacement;
- compose down, prune, volume deletion, credential/secret exposure, force push, direct push to main.

## Root Cause Baseline

`ROOT_CAUSE_PROVEN=true`

`ROOT_CAUSE=PRODUCTION_RUNTIME_ONLY_DRIFT`

`BUG_INTRODUCING_COMMIT=NOT_PROVEN`

`CANONICAL_SOURCE_ALREADY_CORRECT=true`

`FORBIDDEN_PATTERN=await session.refresh(account)`

`SOURCE_FUNCTIONAL_FIX_REQUIRED=false`

## Upstream capability audit

Pinned upstream `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1` already implements the correct flow in `backend-web/app/services/publish_execution_service.py`: capability detection returns refreshed `cookies_str`, then `account.cookie = cookies_str`, then Publisher receives that cookie. Current upstream has also removed the proven runtime-only bad pattern.

## Pinned upstream evidence

Pinned baseline: `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.

Relevant source owner: `backend-web/app/services/publish_execution_service.py`.

Expected canonical sequence: `detect_publish_account_capability -> capability.get("cookies_str") or cookies_str -> account.cookie = cookies_str -> publish_personal_single_item / publish_single_item`.

## Existing local implementation search

XIANYU current main already records the upstream-native Publisher ownership and vendor-patch governance. No canonical source commit contains `await session.refresh(account)` in the proven failure location. The defect exists only in the active production Runtime.

## Reuse decision

Decision: WRAP_FOR_OPERATIONS

No second Publisher, Session owner, Cookie owner, service, route, table, worker, scheduler or transport is added. Source work is limited to regression/drift guards and evidence around the existing upstream-native path.

## Duplicate implementation risk

Low while this Change remains regression/evidence/runtime-convergence only. High if a parallel Publisher/session refresh path is introduced; that is forbidden.

## Why upstream cannot satisfy the requirement

Upstream already supplies the correct behavior, but upstream alone cannot prevent a future local Runtime-only hot patch from reintroducing the forbidden line or prove that the production image was rebuilt from canonical source. Repository regression guards and runtime convergence evidence are therefore required.

## Approved exception ADR

Not applicable. `BUILD_LOCAL_EXCEPTION` is not authorized.

## Component owner

Publisher/capability/session-cookie flow remains owned by the existing upstream-native XIANYU Backend. COMPANY remains deployment/transport infrastructure only.

## Retirement plan for overlapping local code

No overlapping production code is added. Regression/evidence artifacts remain as drift guards; any temporary replay/build workspace is disposable.
