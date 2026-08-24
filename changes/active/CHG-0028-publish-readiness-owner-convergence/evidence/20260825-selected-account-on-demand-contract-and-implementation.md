# CHG-0028 selected-account on-demand contract and implementation evidence - 2026-08-25

Status: VERIFYING

Change ID: CHG-0028-publish-readiness-owner-convergence

## Owner decision

```text
CHG0028_OWNER_CONTRACT_DECISION=APPROVED__SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY
GLOBAL_PERSISTED_PUBLISH_READINESS=DEPRECATED
LINEAGE_AWARE_READINESS_WRITER=NOT_AUTHORIZED
BROWSER_SCOPE=EXCLUDED
PRODUCTION_FREEZE=true
```

The approved continuation chooses the non-persisted option identified by T1-T3. Publisher capability is current fact only when a user selects an account or an explicit caller requests that account's capability. Global account overview and periodic polling must not call the Publisher capability producer and must not describe missing persisted readiness as a system fault, permanent pending, Session invalid, or fabricated `READY`.

## Execution contract

```text
User outcome: expose Publisher capability truth only for the selected account or an explicit on-demand request, using the existing Backend native capability owner.
Confirmed blocker: the previous Accounts-level persisted readiness contract expected an unwritten session_maintenance.consumers.publish record and misrepresented unprobed accounts as a stuck readiness problem.
Smallest success test: deterministic tests prove unprobed Publisher status is ON_DEMAND/NOT_CHECKED, selected-account capability calls PublishAccountCapabilityService.detect exactly once when explicitly requested, and no persisted Publisher readiness writer or polling producer exists.
```

## Development precheck

```text
TASK_TYPE=REPAIR
FAILURE_REASON=ACCOUNTS_READINESS_CONSUMER_EXPECTS_UNWRITTEN_PUBLISH_RECORD
RESPONSIBLE_LAYER=XIANYU_BACKEND_EXISTING_PUBLISH_CAPABILITY_AND_ACCOUNT_STATUS_OWNERS
CURRENT_UPSTREAM_CAPABILITY=PARTIAL__SELECTED_ACCOUNT_CAPABILITY_ROUTE_AND_SERVICE_EXIST_IN_FRESH_UPSTREAM
CURRENT_LOCAL_CAPABILITY=PATCH_ARTIFACT_GOVERNANCE_ONLY__NO_BACKEND_ROUTE_SOURCE_IN_THIS_REPOSITORY
CURRENT_RUNTIME_CAPABILITY=PRODUCER_SERVICE_PLUS_CONSUMER_PRESENT__NO_READINESS_WRITER
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=backend-web/app/api/routes/product_publish_capability.py route adoption plus cookies.py Accounts consumer contract presentation
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=the route is absent from the deployed patch layer and the current Accounts consumer still expects an unwritten persisted record
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false
NEW_IMPLEMENTATION_ALLOWED=false
REUSE_DECISION=PATCH_UPSTREAM
```

## Upstream and local evidence

```text
EXECUTION_WORKTREE=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
EXECUTION_BRANCH=feat/CHG-0028-publish-readiness-owner-convergence
START_BASE_SHA=02fd7ba8a64ebe56d4366635a478b581a3ae1012
PINNED_UPSTREAM_SHA=bda1a859df63fa5f24e51398fa80a23490bb6dfc
FRESH_UPSTREAM_MAIN_SHA=29dc831d4498f3174f0502c989a352ef59815553
UPSTREAM_SELECTED_ACCOUNT_CAPABILITY_COMMIT=5984b483b5bfd6c852ef00c22291b1bf163022ee
```

Fresh upstream commit `5984b483b5bfd6c852ef00c22291b1bf163022ee` adds `backend-web/app/api/routes/product_publish_capability.py`, exports it from `backend-web/app/api/routes/_exports.py`, and routes selected-account checks through `PublishAccountCapabilityService.detect`. The local XIANYU repository carries upstream runtime deltas as vendor patch artifacts, so the source implementation must be delivered as a new scoped patch layer plus deterministic repository tests.

## RED test evidence

```text
COMMAND=python -m pytest changes/active/CHG-0028-publish-readiness-owner-convergence/tests/test_acceptance.py tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py -q
RESULT=FAIL_EXPECTED
SUMMARY=5 failed, 7 passed
FAILURE_REASON=missing vendor/patches/xianyu-auto-reply/chg0028-selected-account-on-demand-capability.patch
RED_SCOPE=deterministic_patch_artifact_contract
REAL_MTOP_CALLS=0
REAL_BROWSER_ACTIONS=0
REAL_BUSINESS_ACTIONS=0
```

The RED failures are the newly added deterministic patch-artifact tests:

- `test_chg0028_patch_is_parseable_and_scoped_to_existing_backend_owner`
- `test_selected_account_route_uses_existing_capability_service_once`
- `test_account_list_contract_is_on_demand_not_persisted_ready`
- `test_patch_does_not_create_global_readiness_writer_or_browser_gate`
- `test_patch_contains_upstream_native_mock_tests`

## Implementation evidence

```text
PATCH_FILE=vendor/patches/xianyu-auto-reply/chg0028-selected-account-on-demand-capability.patch
PATCH_SHA256=CED451293701C53475E23F9B87DF205AB97AFDD0B3696D35A4D9C8675BC4E490
PATCH_BUILDER=D:/xianyu-worktrees/_chg0028_patch_builder_runtime
RUNTIME_PREIMAGE=read-only extracted xianyu-chg0027-backend-web:session-transient-classification-20260824-r1 source files
CHANGED_UPSTREAM_RUNTIME_FILES=4
```

Changed upstream/runtime files in the patch:

- `backend-web/app/api/routes/_exports.py`
- `backend-web/app/api/routes/cookies.py`
- `backend-web/app/api/routes/product_publish_capability.py`
- `tests/test_chg0028_selected_account_on_demand_capability.py`

Implementation summary:

- registers the selected-account route `/product-publish/accounts/{account_id}/capability`;
- uses the existing `detect_publish_account_capability` helper, which loads `PublishAccountCapabilityService.detect` and uses the current account Cookie;
- returns explicit selected-account success as `state=READY`, `mode=ON_DEMAND`, `checked=true`;
- maps explicit selected-account transient failure to `state=RETRY_LATER`, `retryable=true`, not Session invalid;
- maps explicit account-invalid failure to `state=ACCOUNT_INVALID`, `retryable=false`;
- changes the account-list/global Publisher presentation for unchecked capability to `state=NOT_CHECKED`, `mode=ON_DEMAND`, `checked=false`;
- replaces stale persisted `publish_state == READY` account-list presentation with on-demand/not-checked because global persisted Publisher readiness is deprecated and has no lineage validation.

The explicit selected-account route uses the existing `detect_publish_account_capability` helper. Current upstream evidence at `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1:common/services/xianyu_publish_service.py` shows that helper loads `backend-web/app/services/publish_account_capability_service.py` and calls `PublishAccountCapabilityService.detect`; CHG-0028 does not add a parallel wrapper or second capability service.

No `session_maintenance.consumers.publish` writer, readiness table, scheduler/background probe, Browser gate, COMPANY owner, second Publisher owner, or account-list MTop/preget producer is added.

## Verification evidence

```text
COMMAND=python -m pytest tests/test_chg0028_selected_account_on_demand_capability.py -q
WORKDIR=D:/xianyu-worktrees/_chg0028_patch_builder_runtime
RESULT=PASS
SUMMARY=11 passed in 0.14s

COMMAND=git apply --check --whitespace=error-all --unidiff-zero D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825/vendor/patches/xianyu-auto-reply/chg0028-selected-account-on-demand-capability.patch
WORKDIR=D:/xianyu-worktrees/_chg0028_patch_builder_runtime_check
RESULT=PASS

COMMAND=git apply --numstat --unidiff-zero D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825/vendor/patches/xianyu-auto-reply/chg0028-selected-account-on-demand-capability.patch
WORKDIR=D:/xianyu-worktrees/_chg0028_patch_builder_runtime_check
RESULT=PASS
NUMSTAT=2 0 backend-web/app/api/routes/_exports.py; 15 10 backend-web/app/api/routes/cookies.py; 79 0 backend-web/app/api/routes/product_publish_capability.py; 259 0 tests/test_chg0028_selected_account_on_demand_capability.py

COMMAND=git apply --unidiff-zero D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825/vendor/patches/xianyu-auto-reply/chg0028-selected-account-on-demand-capability.patch && python -m pytest tests/test_chg0028_selected_account_on_demand_capability.py -q
WORKDIR=D:/xianyu-worktrees/_chg0028_patch_builder_runtime_check2
RESULT=PASS
SUMMARY=11 passed in 0.12s

COMMAND=python -m pytest changes/active/CHG-0028-publish-readiness-owner-convergence/tests/test_acceptance.py tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py -q
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PASS
SUMMARY=12 passed in 0.15s

COMMAND=python -m pytest changes/archive/CHG-0026-qr-dual-mode-and-chat-connectivity-recovery/tests/test_acceptance.py -q
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PASS
SUMMARY=6 passed in 0.08s

COMMAND=python -m pytest changes/archive/CHG-0027-session-transient-classification-qr-cooldown-lineage/tests/test_acceptance.py -q
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PASS
SUMMARY=5 passed in 0.09s

COMMAND=python -m pytest tests/unit/test_generate_state.py tests/unit/test_project_context.py tests/unit/test_validate_change.py -q
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PRE_EXISTING_BLOCKED
SUMMARY=22 passed, 5 failed
BLOCKER=CHG-0020 archived change missing design.md and tasks.md; unrelated branch mismatch was corrected by renaming the isolated execution branch.

COMMAND=python scripts/validate_change.py
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PRE_EXISTING_BLOCKED
ERROR=missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md

COMMAND=git diff --check
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PASS

COMMAND=ruff check .
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PASS
SUMMARY=All checks passed

COMMAND=python scripts/security_scan.py
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PASS
SUMMARY=security scan passed

COMMAND=python scripts/verify_repository.py
WORKDIR=D:/xianyu-worktrees/CHG-0028-selected-account-on-demand-20260825
RESULT=PRE_EXISTING_BLOCKED
ERROR=missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md
```

## Safety counters

```text
REAL_MESSAGES_SENT=0
REAL_PRODUCTS_PUBLISHED=0
REAL_PRODUCTS_MODIFIED=0
NEW_ITEM_SYNC_INVOCATION_COUNT=0
QR_LOGIN_INVOCATION_COUNT=0
MANUAL_RECONNECT_INVOCATION_COUNT=0
PRODUCTION_ACCOUNT_MUTATION_COUNT=0
PRODUCTION_CONTAINER_RESTART_OR_REPLACEMENT_COUNT=0
PRODUCTION_RUNTIME_CONFIGURATION_MUTATION_COUNT=0
COMPANY_SOURCE_MUTATION_COUNT=0
BROWSER_INVOCATION_COUNT=0
GLOBAL_PERSISTED_PUBLISH_READINESS_WRITER_CREATED=0
```

## GitHub persistence and initial CI evidence - 2026-08-24

```text
LOCAL_START_SHA=02fd7ba8a64ebe56d4366635a478b581a3ae1012
IMPLEMENTATION_COMMIT_SHA=95c4675c5dae785fab801affa85cd1975892cd7e
REMOTE_BRANCH=feat/CHG-0028-publish-readiness-owner-convergence
REMOTE_BRANCH_SHA=95c4675c5dae785fab801affa85cd1975892cd7e
GITHUB_TRANSPORT_USED=HTTPS push to explicit repository URL; command returned MCP internal error, then GitHub API recovery verified the commit and branch SHA.
SSH_KEY_CREATED=NO
SHARED_ORIGIN_URL_CHANGED=NO
PR_NUMBER=41
PR_URL=https://github.com/yuanweizhang94-crypto/XIANYU/pull/41
PR_HEAD_SHA=95c4675c5dae785fab801affa85cd1975892cd7e
PR_BASE=main
PR_BASE_SHA=dc83ef23603c1725d3babcd8f89f54db0592f075
PATCH_SHA256=CED451293701C53475E23F9B87DF205AB97AFDD0B3696D35A4D9C8675BC4E490
```

Remote verification:

```text
CHECK=GitHub commit API
RESULT=PASS
REMOTE_COMMIT=95c4675c5dae785fab801affa85cd1975892cd7e
PARENT=02fd7ba8a64ebe56d4366635a478b581a3ae1012

CHECK=GitHub compare 02fd7ba8..feat/CHG-0028-publish-readiness-owner-convergence
RESULT=PASS
AHEAD_BY=1
BEHIND_BY=0
FILES=10
```

Current implementation commit scoped files:

```text
changes/active/CHG-0028-publish-readiness-owner-convergence/acceptance.md
changes/active/CHG-0028-publish-readiness-owner-convergence/design.md
changes/active/CHG-0028-publish-readiness-owner-convergence/evidence/20260825-selected-account-on-demand-contract-and-implementation.md
changes/active/CHG-0028-publish-readiness-owner-convergence/proposal.md
changes/active/CHG-0028-publish-readiness-owner-convergence/tasks.md
changes/active/CHG-0028-publish-readiness-owner-convergence/tests/test_acceptance.py
generated/PROJECT_STATE.json
tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py
vendor/patches/xianyu-auto-reply/README.md
vendor/patches/xianyu-auto-reply/chg0028-selected-account-on-demand-capability.patch
```

Main-based PR #41 currently lists 17 files because the feature branch includes earlier CHG-0028 audit/approval history and CHG-0027 archive files that are ancestors of `02fd7ba8a64ebe56d4366635a478b581a3ae1012` but not yet on main. The current implementation commit remains the exact 10-file scoped diff above.

Initial PR CI for head `95c4675c5dae785fab801affa85cd1975892cd7e`:

```text
security / security = success
quality / quality = failure
  PASS: Ruff check
  PASS: Mypy check
  FAIL: Repository and change validation
  FAILURE_CLASSIFICATION=PRE_EXISTING_CHG0020_ARCHIVE_DEBT
  ERROR=missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md

tests / tests = failure
  FAIL: Run pytest
  SUMMARY=11 failed, 592 passed, 1 warning
  FAILURE_CLASSIFICATION=UNRELATED_PRE_EXISTING_GOVERNANCE_DEBT
  FAILURES=CHG-0020 missing archive design/tasks; CHG-0022 active evidence file path assumptions; README/AGENTS governance drift assertion.
```

CHG-0028-specific CI/log classification:

```text
CHG0028_SPECIFIC_CI=PASS_BY_LOG_CLASSIFICATION
CHG0028_BEHAVIOR_FAILURES_IN_CI=0
GLOBAL_CI_STATUS=FAIL_UNRELATED_PRE_EXISTING_GOVERNANCE_DEBT
CHG0020_DEBT_ABSORBED=NO
BROWSER_ACTIONS=0
PRODUCTION_MUTATIONS=0
REAL_BUSINESS_ACTIONS=0
```

Closure-commit local verification after recording PR/CI evidence:

```text
python -m pytest changes/active/CHG-0028-publish-readiness-owner-convergence/tests/test_acceptance.py tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py -q = 12 passed in 0.09s
python -m pytest changes/archive/CHG-0026-qr-dual-mode-and-chat-connectivity-recovery/tests/test_acceptance.py -q = 6 passed in 0.03s
python -m pytest changes/archive/CHG-0027-session-transient-classification-qr-cooldown-lineage/tests/test_acceptance.py -q = 5 passed in 0.02s
python -m ruff check . = All checks passed
python scripts/security_scan.py = security scan passed
git diff --check = PASS
python scripts/validate_change.py = PRE_EXISTING_BLOCKED: CHG-0020 archived change missing design.md and tasks.md
python scripts/verify_repository.py = PRE_EXISTING_BLOCKED: CHG-0020 archived change missing design.md and tasks.md
```

No CI failure references the selected-account on-demand capability patch, CHG-0028 acceptance tests, Browser exclusion, production freeze, real business actions, or persisted readiness writer creation. The unrelated debt is recorded and not fixed in this Change.
