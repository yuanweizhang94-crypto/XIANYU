# CHG-0036 Source regression and clean replay evidence

Date: 2026-08-30

## Authority

`XIANYU_REMOTE_MAIN_SHA=5dd103e096cb921e979ae1a3923febe5c357fff8`

`COMPANY_REMOTE_MAIN_SHA=dfbb9e2b825f11be02a07217b3193f3cd6996fde`

`CURRENT_UPSTREAM_MAIN_SHA=d8c1a970304fdfb31fef549e07167d7ce82c0819`

`PINNED_UPSTREAM_SHA=742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`

## Root cause inherited

`ROOT_CAUSE_PROVEN=true`

`ROOT_CAUSE=PRODUCTION_RUNTIME_ONLY_DRIFT`

`BUG_INTRODUCING_COMMIT=NOT_PROVEN`

`CANONICAL_SOURCE_ALREADY_CORRECT=true`

`BUSINESS_SOURCE_LOGIC_CHANGED=false`

`FORBIDDEN_PATTERN=await session.refresh(account)`

## Pinned canonical source

`PINNED_PUBLISH_SERVICE_SHA256=50219b5069803498c350c8edf2eb765f997318a5ca92b6ed88e9ccf6ab3a3df7`

`PINNED_FORBIDDEN_PATTERN_COUNT=0`

`PINNED_CAPABILITY_COOKIE_FLOW=true`

The canonical batch flow remains `detect_publish_account_capability -> capability.get("cookies_str") or cookies_str -> account.cookie = cookies_str -> Publisher`. No functional business-source patch was made.

## Regression artifact

`PATCH=vendor/patches/xianyu-auto-reply/publisher-session-runtime-drift-regression-20260830.patch`

`PATCH_SHA256=750d60160cb4126669a74b1220e48b5bcc64f8d7be4562ca8a96e77ba7d1e52f`

`PATCH_CHANGED_FILES=tests/test_publish_session_runtime_drift_regression.py`

`UPSTREAM_REGRESSION_TESTS=8/8 PASS`

All Publisher transports in the regression suite are stubs/AsyncMock. The suite makes no real publish HTTP request and cannot create a platform item.

## Clean replay

A fresh managed worktree at pinned upstream `742fb58a...` accepted the regression artifact with `git apply --check --whitespace=error-all --unidiff-zero`, then applied it cleanly. The replayed regression suite passed 8/8.

`CLEAN_REPLAY_PASS=true`

`REPLAYED_PUBLISH_SERVICE_SHA256=50219b5069803498c350c8edf2eb765f997318a5ca92b6ed88e9ccf6ab3a3df7`

`FORBIDDEN_PATTERN_COUNT=0`

`CANONICAL_SOURCE_SESSION_FLOW_PASS=true`

`FORBIDDEN_RUNTIME_DRIFT_PATTERN_IN_SOURCE=false`

The regression artifact is test-only, so replay leaves the canonical Publish service blob unchanged. Current post-742 runtime/vendor layers inspected for this closure do not require a functional change to this source file.

## XIANYU source gates

Targeted XIANYU set: CHG-0036 guard, CHG-0028 selected-account capability artifact, publish service/validation/domain/fingerprint, publish persistence/security, and active-Change acceptance tests.

`TARGETED_TESTS_PASS=true`

`TARGETED_RESULT=132 passed`

`CHANGE_VALIDATION=PASS`

`SECRET_SCAN_PASS=true`

`DIFF_CHECK_PASS=true`

## Full verify classification

An untouched `5dd103e...` clean control worktree runs 630 tests and has 4 existing failures: CHG-0020 patch raw-byte SHA, CHG-0030 patch raw-byte SHA, online-chat patch raw-byte SHA, and Windows worktree Alembic path identity. These are present before CHG-0036.

The CHG-0036 worktree initially showed those same baseline failures plus the pre-existing archived CHG-0032 test that hardcodes `generated.PROJECT_STATE.active_change is None`; that assertion necessarily fails while any legitimate active Change exists. CHG-0036 did not modify those unrelated historical tests/artifacts.

`FULL_VERIFY_GLOBAL=FAIL_PRE_EXISTING_BASELINE_AND_ACTIVE_CHANGE_ASSUMPTION`

`CHG0036_TARGETED_SCOPE=PASS`

## Platform write counters

`PLATFORM_WRITE_GUARD_ACTIVE=true`

`REAL_PUBLISH_HTTP_REQUEST_COUNT=0`

`REAL_ITEM_CREATE_COUNT=0`

`REAL_XIANYU_PUBLISH_EXECUTED=false`
