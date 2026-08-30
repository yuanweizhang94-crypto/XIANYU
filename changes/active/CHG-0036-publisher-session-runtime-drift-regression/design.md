# CHG-0036 Design

Change ID: CHG-0036-publisher-session-runtime-drift-regression
Status: IMPLEMENTING

## Design

This Change does not alter canonical Publisher business logic. It adds a regression artifact against pinned upstream and a XIANYU-side verifier so CI can detect reintroduction of the production-only bad pattern.

The regression artifact exercises `PublishExecutorService.batch_publish` with all external publish transport stubbed. It verifies:

1. refreshed capability `cookies_str` is assigned to the matching account and passed to Publisher;
2. the batch function does not reference the undefined local `session`;
3. no duplicate SQLAlchemy refresh occurs after capability detection;
4. missing refreshed cookies fall back to the existing valid cookie under current canonical semantics;
5. capability/auth failure fails closed before Publisher transport;
6. success path reaches the stubbed Publisher boundary without a real request;
7. three accounts preserve cookie isolation;
8. Material 94-shaped input reaches the pre-platform stub and cannot create an item.

Runtime convergence then rebuilds Backend from the final merged XIANYU truth plus the pinned upstream/vendor replay chain. Candidate and production images are inspected for the forbidden line before/after activation.

## Platform write guard

`PLATFORM_WRITE_GUARD_ACTIVE=true`

All regression and dry-run transports are replaced with in-process stubs. No real `publish_single_item` / `publish_personal_single_item` transport may execute in tests. Any runtime dry-run must use a hard blocker and must not persist SUCCESS or an item id.

## Clean replay

Replay authority is pinned upstream plus current XIANYU vendor patch artifacts. The replayed `backend-web/app/services/publish_execution_service.py` must contain the canonical capability-cookie assignment and zero instances of `await session.refresh(account)`.

## Runtime activation

Only Backend may be replaced. Preserve existing environment, mounts, network, ports, restart policy, MySQL, Redis, Cookie, Session and Profile. Record rollback identity before activation and health/read-only smoke after activation.

## Upstream capability audit

Canonical capability exists and is correct; no source functional repair is required.

## Pinned upstream evidence

Pinned SHA: `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.

## Existing local implementation search

Current XIANYU main contains governance/vendor artifacts and no proved canonical business-source defect for this incident.

## Reuse decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate implementation risk

A second Session/Cookie/Publisher owner would duplicate the upstream path and is forbidden.

## Why upstream cannot satisfy the requirement

Repository drift guards and local production image convergence are operational concerns outside upstream's ability to guarantee.

## Approved exception ADR

Not applicable.

## Component owner

Existing XIANYU upstream-native Backend Publisher path.

## Retirement plan for overlapping local code

No overlapping production code is introduced.
