# CHG-0018 Threat Model

Status: VERIFYING

Change ID: CHG-0018-account-profile-publish-safety

## Threats

- Saved account passwords leak through API responses, frontend state, logs, tests, or evidence.
- Browser autofill or shared edit forms overwrite credentials without explicit owner action.
- Password refresh failures disable valid accounts.
- Caller-supplied account/Cookie pairs open the wrong Profile.
- Publish preflight opens one context and publish opens another, masking readiness failures.
- Locking is nested or duplicated, leaving browser resources behind.
- Profile repair performs real account, publish, or message operations.

## Mitigations

- No raw password response; credential editing is explicit and dirty-tracked.
- No account disablement on no/bad credentials.
- Profile services read authoritative account data.
- Shared preflight runs in the active context for formal publish attempts.
- Existing lock and browser slot primitives are used once per task.
- Production operations remain prohibited during development.

## Upstream capability audit

The threat model is limited to pinned upstream credential, Profile, publish, preflight, and browser lifecycle paths.

## Pinned upstream evidence

Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.

## Existing local implementation search

No local runtime replacement is allowed.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Parallel runtime components are forbidden.

## Why upstream cannot satisfy the requirement

Pinned upstream needs minimal safety and lifecycle patches.

## Approved exception ADR

Not applicable.

## Component owner

Pinned upstream runtime paths and XIANYU governance patch ownership.

## Retirement plan for overlapping local code

No overlapping local production code is introduced.
