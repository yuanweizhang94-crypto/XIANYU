# CHG-0036 Acceptance

Change ID: CHG-0036-publisher-session-runtime-drift-regression
Status: ARCHIVED

Acceptance requires all of the following:

- `CANONICAL_SOURCE_ALREADY_CORRECT=true`.
- `BUSINESS_SOURCE_LOGIC_CHANGED=false`.
- pinned-upstream regression suite passes all eight required cases with real Publisher transport replaced by stubs.
- `FORBIDDEN_PATTERN_COUNT=0` for canonical source and clean replayed Backend source.
- clean replay preserves `capability.get("cookies_str") or cookies_str` and `account.cookie = cookies_str`.
- targeted source/regression gates, syntax, diff check and secret scan pass; unrelated baseline debt is classified rather than repaired.
- GitHub PR security/quality/tests pass, PR merges normally, and the regression guard is an ancestor of final main.
- clean Backend candidate is built from final main replay, not from the current production container or dirty worktree.
- Backend-only activation preserves MySQL, Redis, Cookie, Session, Profile, environment, mounts, network, ports and restart policy.
- production source has zero forbidden pattern and canonical capability-cookie flow after activation.
- Backend health, account-status smoke and read-only Chat smoke pass.
- Material 94 hard-blocked runtime preflight reaches Publisher transport boundary without the prior NameError and without a real platform request.
- Materials 94-103 read-only preflight completes without changing material content.
- three-account mock/dry-run proves no cross-account cookie/session leakage.
- blocked transport cannot persist real SUCCESS or generate an item id.
- `REAL_PUBLISH_HTTP_REQUEST_COUNT=0` and `REAL_ITEM_CREATE_COUNT=0` for this Change.
- no real Material 94-103 publish, auto-reply change, message send, order mutation or account-state change occurs.

## Upstream capability audit

Canonical capability is already implemented by pinned upstream; acceptance is regression/convergence only.

## Pinned upstream evidence

Pinned SHA `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.

## Existing local implementation search

Current XIANYU source governance and the upstream-native Publisher owner are reused.

## Reuse decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate implementation risk

A second Publisher, Session owner, Cookie owner or publish transport would invalidate acceptance.

## Why upstream cannot satisfy the requirement

Local Runtime-only drift prevention and production image convergence require local regression/operational controls.

## Approved exception ADR

Not applicable.

## Component owner

Existing XIANYU Backend Publisher path.

## Retirement plan for overlapping local code

No overlapping production implementation is introduced.

## Final closure results — 2026-08-30

- `ROOT_CAUSE_PROVEN=true`.
- `SOURCE_REGRESSION_CLOSURE_PASS=true`.
- `GITHUB_SOURCE_CLOSURE_PASS=true`; PR #52 merged and `cef03d9478dbfb205ae64052e069cca0991a5583` is an ancestor of `2df208780e556ace2230f0c6ce7d4e7252a33a25`.
- `RUNTIME_CLOSURE_PASS=true`.
- `BUSINESS_SOURCE_LOGIC_CHANGED=false`.
- `PRODUCTION_BACKEND_IMAGE=xianyu-chg0018-backend-web:chg0036-clean-replay-2df2087-20260830-r1`.
- `PRODUCTION_FORBIDDEN_PATTERN_COUNT=0`.
- `PRODUCTION_CANONICAL_COOKIE_FLOW=PASS`.
- `BACKEND_HEALTHY=true`.
- `ACCOUNT_STATUS_SMOKE_PASS=true`.
- `CHAT_READ_ONLY_SMOKE_RESULT=PASS_WITH_PRE_EXISTING_ACCOUNT_CONNECTION_STATE`; the route remained reachable with Backend HTTP 200 and no Backend 5xx/crash/import error, while the sampled IM sessions were already naturally disconnected and were not reconnected for this Change.
- `CHAT_RUNTIME_REGRESSION=false` because no replacement-induced connection-state regression evidence was observed.
- `MATERIAL_94_RUNTIME_PREFLIGHT_PASS=true`.
- `ALL_MATERIAL_94_103_PREFLIGHT_PASS=true`.
- `PUBLISH_FLOW_REACHES_PLATFORM_BOUNDARY=true` under the hard-blocked in-process transport stub.
- `SESSION_NAMEERROR_REPRODUCED=false`.
- `CROSS_ACCOUNT_SESSION_LEAK=false`.
- `NO_FALSE_PUBLISH_SUCCESS=true`; the blocked dry-run persisted zero publish logs and generated no item id.
- `REAL_PUBLISH_HTTP_REQUEST_COUNT=0`.
- `REAL_ITEM_CREATE_COUNT=0`.
- `REAL_XIANYU_PUBLISH_EXECUTED=false`.
- `PUBLISHER_READY_FOR_FUTURE_CANARY=true`; a future real single-item canary requires a separate explicit authorization and is not part of this Change.
