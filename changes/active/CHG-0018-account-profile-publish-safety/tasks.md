# CHG-0018 Tasks

Status: VERIFYING

Change ID: CHG-0018-account-profile-publish-safety

- [x] T1 Implement P0 credential safety and false-disable prevention.
- [x] T2 Run P0 targeted tests and commit the P0 boundary.
- [x] T3 Implement P1 persistent Profile publish readiness.
- [x] T4 Implement P2 Profile initialization and repair boundaries.
- [x] T5 Implement P3 shared read-only publish preflight.
- [x] T6 Implement P4 canonical browser lock usage for publish readiness paths.
- [x] T7 Run P1-P4 targeted tests and commit the Profile readiness boundary.
- [x] T8 Generate CHG-0018 patch artifact, evidence, and full validation.

## Upstream capability audit

Pinned upstream account, password refresh, Cookie renewal, publisher, preflight diagnostics, and browser concurrency paths are the implementation sources.

## Pinned upstream evidence

Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.

## Existing local implementation search

Local wrapper and archived changes were checked for overlap; no local runtime replacement is allowed.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Tasks must not add a second sender, publisher, login system, Token system, browser broker, service, queue, or database table.

## Why upstream cannot satisfy the requirement

Pinned upstream lacks the required safety and Profile lifecycle guarantees without a minimal patch.

## Approved exception ADR

Not applicable.

## Component owner

Pinned upstream runtime paths and XIANYU governance patch ownership.

## Retirement plan for overlapping local code

No overlapping local production code is introduced.
