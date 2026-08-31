# CHG-0037 Acceptance

Change ID: CHG-0037-opencv-headless-runtime-dependency
Status: ARCHIVED

## Required source gates

- `CURRENT_BACKEND_DEPENDENCY_AUTHORITY=backend-web/pyproject.toml consumed by backend-web/Dockerfile`.
- Vendor patch changes only `backend-web/pyproject.toml`.
- Exact dependency after patch: `opencv-python-headless==5.0.0.93`.
- No `opencv-python` GUI package is introduced.
- `BUSINESS_SOURCE_LOGIC_CHANGED=false`.
- CHG-0036 forbidden session pattern remains absent.
- Canonical capability-cookie flow remains unchanged.
- Targeted tests, change validation, secret scan and `git diff --check` pass.

## Required candidate gates

Candidate is built only after source PR merge and records the merged/final XIANYU main source SHA.

- `CANDIDATE_CV2_IMPORT_PASS=true`.
- `CANDIDATE_CV2_VERSION=5.0.0`.
- `CANDIDATE_OPENCV_DISTRIBUTION_VERSION=5.0.0.93`.
- `CANDIDATE_PUBLISHER_IMPORT_PASS=true`.
- `CANDIDATE_SESSION_FORBIDDEN_PATTERN_COUNT=0`.
- `CANDIDATE_CANONICAL_COOKIE_FLOW=true`.

## Required production gates

Backend-only replacement must preserve Frontend, WebSocket, Scheduler, MySQL, Redis, volumes, network, port bindings, restart policy, Cookie, Session and Profile state.

- `BACKEND_HEALTHY=true` and HTTP health 200.
- `RUNTIME_CV2_IMPORT_PASS=true`.
- `RUNTIME_CV2_VERSION=5.0.0`.
- `RUNTIME_OPENCV_DISTRIBUTION_VERSION=5.0.0.93`.
- `PRODUCTION_SESSION_FORBIDDEN_PATTERN_COUNT=0`.
- `PRODUCTION_CANONICAL_COOKIE_FLOW=true`.
- account read-only smoke passes.
- chat read-only route is reachable without reconnect/login/account mutation; pre-existing disconnected IM state may be reported as such.

## Material 94 hard-blocked dry-run

Use Material 94 and account `2804730247` only after current read-only readiness still shows enabled/online/login-ready and no human verification/cooldown blocker.

The real platform transport must be stubbed/intercepted/hard-blocked before any item create request.

Required:

- `RUNTIME_TRANSPORT_GUARD_INSTALLED=true`.
- `PLATFORM_WRITE_GUARD_ACTIVE=true`.
- `MATERIAL_94_CV2_RUNTIME_PREFLIGHT_PASS=true`.
- `CV2_ERROR_REPRODUCED=false`.
- `SESSION_NAMEERROR_REPRODUCED=false`.
- `PUBLISH_FLOW_REACHES_PLATFORM_BOUNDARY=true`.
- `REAL_PLATFORM_REQUEST_BLOCKED=true`.
- `NO_FALSE_PUBLISH_SUCCESS=true`.
- `REAL_PUBLISH_HTTP_REQUEST_COUNT=0`.
- `REAL_ITEM_CREATE_COUNT=0`.

## Safety invariants

- `REAL_XIANYU_PUBLISH_EXECUTED=false`.
- `MATERIALS_PUBLISHED_THIS_RUN=0`.
- `ITEMS_CREATED_THIS_RUN=0`.
- `AUTO_REPLY_CHANGED=false`.
- `MESSAGE_SENT=false`.
- `ORDER_CHANGED=false`.
- `ACCOUNT_STATE_CHANGED=false`.
- no QR login, face verification or verification bypass.
- no MySQL/Redis/Cookie/Session/Profile loss.

## Upstream capability audit

Pinned/current upstream already own the dependency declaration and Docker installation path.

## Pinned upstream evidence

Pinned SHA `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`; dependency in `backend-web/pyproject.toml`; install consumer in `backend-web/Dockerfile`.

## Existing local implementation search

The current production Backend lacks cv2; historical formal runtime proves `opencv-python-headless==5.0.0.93` produces `cv2==5.0.0`.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Dependency-only pin; no duplicate Publisher/session/build owner.

## Why upstream cannot satisfy the requirement

XIANYU needs an exact local release pin and drift guard so the dependency cannot disappear again during local Runtime lineage replay.

## Approved exception ADR

Not applicable.

## Component owner

Existing upstream Backend dependency/build path.

## Retirement plan for overlapping local code

Retire this pin when equivalent upstream exact pinning is proven in clean build and production.

## Final verified closure evidence

The sanitized final Runtime/category evidence is preserved at `evidence/20260831-final-runtime-category-and-archive-closure.md`.

Verified closure facts include:

- PR #55 merged and both CHG-0037 source commits are ancestors of `dc3c2d3956e5be09ebaaf61d62aea539b5d9d254`.
- candidate and production Backend import `cv2==5.0.0` from `opencv-python-headless==5.0.0.93`.
- Publisher import passes, the CHG-0036 forbidden session pattern count is zero, and canonical capability-cookie flow remains intact.
- Backend-only activation preserved the non-Backend services and MySQL/Redis/Cookie/Session/Profile state.
- Material 94 category compatibility was proven from an existing platform donor and a fresh XIANYU native recommendation.
- the formal `xianyu_material_category_apply` adapter persisted Material 94's complete platform category without caller-supplied category IDs.
- the final hard-blocked Runtime preflight used the persisted Material category, not in-memory category injection, and reached the platform item-create boundary with zero real publish requests/items and no false SUCCESS.
- no real Material 94 canary was executed by CHG-0037.

`RUNTIME_ACCEPTANCE_COMPLETE=true`.
`MATERIAL_94_PERSISTED_CATEGORY_PREFLIGHT_PASS=true`.
`BUSINESS_SOURCE_LOGIC_CHANGED=false`.
