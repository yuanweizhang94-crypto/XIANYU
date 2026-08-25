# CHG-0030 Phase 4b skipped-lock follow-up evidence

Date: 2026-08-25

Production canary state: NOT AUTHORIZED. No Item Sync invocation was performed.

## Defect

Commander finding confirmed: the r1 CHG-0030 route could classify an `ItemService.fetch_all_items_from_account` Redis-lock result as successful because the owner returned:

```text
success=true, skipped=true, items=[], total_count=0, saved_count=0
```

The r1 durable readback then reconciled zero response IDs and zero counts and could set:

```text
sync_status=SUCCESS
durable_readback.checked=true
duplicate_count=0
```

This is not terminal Fresh Item Sync success. It means the owner did not run because the account lock was occupied.

## RED evidence

Runtime replay source:

```text
D:/xianyu-worktrees/_chg0030_r1_followup_builder_tmp
```

Base:

```text
8c2723e552bb9f797c73b6c497858bc314549877
```

Applied first locked patch:

```text
vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-controlled-canary.patch
SHA256=595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201
```

RED command:

```text
python -m pytest tests/test_chg0030_fresh_item_sync_controlled_canary.py::test_skipped_lock_result_is_terminal_unknown_not_success -q
```

RED result:

```text
FAILED tests/test_chg0030_fresh_item_sync_controlled_canary.py::test_skipped_lock_result_is_terminal_unknown_not_success
assert True is False
```

## Follow-up patch

Patch file:

```text
vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-skipped-lock-success-guard.patch
```

SHA256:

```text
1FC5597EEC8FB0060EBA6551D4F98407649EB0FA0675BDC4CA5574D0362B9DC6
```

Changed runtime files:

```text
backend-web/app/api/routes/cookies.py
backend-web/app/api/routes/items.py
tests/test_chg0030_fresh_item_sync_controlled_canary.py
```

Behavior:

- `skipped=true` sets terminal `UNKNOWN`, not `SUCCESS`;
- `success` is set false for the terminal UNKNOWN response so adapters that strip extension fields do not see success;
- `durable_readback.checked=false`;
- `durable_readback.reconciled=false`;
- `durable_readback.failure_reason=OWNER_LOCK_OCCUPIED_SKIPPED`;
- `retry_allowed=false` remains unchanged;
- terminal log `CHG0030_ITEM_SYNC_TERMINAL_READBACK` includes `skipped`, `failure_reason`, and `full_active_list_confirmed`;
- Fresh Item Sync `SUCCESS` additionally requires `full_active_list_confirmed=true`;
- incomplete/capped service results fail closed as `FULL_ACTIVE_LIST_NOT_CONFIRMED`;
- selected-account preflight facts/logs expose sanitized `platform_verification_evidence_type`.

No second owner, queue/status ledger, DB truth model, scheduler, worker, Browser/UI/CDP path, auth recovery, retry, account mutation, message path, publish/edit/offline/delete path, or second Item Sync invocation was added.

## GREEN runtime replay evidence

Builder validation:

```text
python -m py_compile common/schemas/item.py backend-web/app/api/routes/items.py backend-web/app/api/routes/cookies.py
python -m pytest tests/test_chg0030_fresh_item_sync_controlled_canary.py -q
```

Result:

```text
6 passed
```

Adjacent CHG-0028 regression:

```text
python -m pytest tests/test_chg0028_selected_account_on_demand_capability.py -q
```

Result:

```text
11 passed
```

Clean two-patch replay source:

```text
D:/xianyu-worktrees/_chg0030_two_patch_replay_20260825111651
```

Replay commands:

```text
git apply --check --whitespace=error-all --unidiff-zero chg0030-fresh-item-sync-controlled-canary.patch
git apply --whitespace=error-all --unidiff-zero chg0030-fresh-item-sync-controlled-canary.patch
git apply --check --whitespace=error-all --unidiff-zero chg0030-fresh-item-sync-skipped-lock-success-guard.patch
git apply --whitespace=error-all --unidiff-zero chg0030-fresh-item-sync-skipped-lock-success-guard.patch
python -m py_compile common/schemas/item.py backend-web/app/api/routes/items.py backend-web/app/api/routes/cookies.py
python -m pytest tests/test_chg0030_fresh_item_sync_controlled_canary.py tests/test_chg0028_selected_account_on_demand_capability.py -q
git diff --check
```

Result:

```text
17 passed
git diff --check PASS
```

## Deployment state

Backend r1 remains deployed at the time of this evidence. Backend r2 is not deployed yet. Production Item Sync canary remains NO-GO until r2 is deployed, read-only preflight is repeated, and commander later sends explicit GO.

## Repository-side focused verification

Locked r1 artifact hash recheck:

```text
595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201
```

Follow-up artifact hash:

```text
1FC5597EEC8FB0060EBA6551D4F98407649EB0FA0675BDC4CA5574D0362B9DC6
```

CHG-0030 active acceptance, CHG-0030 artifact tests, and CHG-0028 artifact tests:

```text
D:/xianyu/.venv/Scripts/python.exe -m pytest changes/active/CHG-0030-fresh-item-sync-controlled-canary/tests/test_acceptance.py tests/unit/test_chg0030_fresh_item_sync_canary_patch_artifact.py tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py -q
22 passed
```

Owner/session/capability archive regressions:

```text
D:/xianyu/.venv/Scripts/python.exe -m pytest changes/archive/CHG-0024-item-sync-no-auth-recovery-safety/tests/test_acceptance.py -q
8 passed

D:/xianyu/.venv/Scripts/python.exe -m pytest changes/archive/CHG-0026-qr-dual-mode-and-chat-connectivity-recovery/tests/test_acceptance.py -q
6 passed

D:/xianyu/.venv/Scripts/python.exe -m pytest changes/archive/CHG-0027-session-transient-classification-qr-cooldown-lineage/tests/test_acceptance.py -q
5 passed
```

Archive acceptance notes:

```text
CHG-0018 archive acceptance: 8 passed, 1 failed on generated active_change expected None while CHG-0030 is intentionally active.
CHG-0028 archive acceptance: 7 passed, 1 failed on generated active_change expected None while CHG-0030 is intentionally active.
CHG-0029 archive acceptance: 6 passed, 2 failed on active change directory/state expected none while CHG-0030 is intentionally active.
```

Auto-reply, online-chat, publish, duplicate, security, ruff, and diff checks:

```text
D:/xianyu/.venv/Scripts/python.exe -m pytest changes/archive/CHG-0023-websocket-auto-reply-readiness-contract-restoration/tests/test_acceptance.py -q
5 passed

D:/xianyu/.venv/Scripts/python.exe -m pytest tests/unit/test_autoreply.py tests/unit/test_reply_domain.py tests/unit/test_reply_evaluator.py tests/unit/test_reply_mapper.py tests/unit/test_reply_renderer.py tests/unit/test_reply_service.py tests/unit/test_publish_domain.py tests/unit/test_publish_fingerprint.py tests/unit/test_publish_service.py tests/unit/test_publish_validation.py -q
183 passed

D:/xianyu/.venv/Scripts/python.exe -m pytest tests/unit/test_duplicate_capabilities.py -q
4 passed

D:/xianyu/.venv/Scripts/python.exe scripts/detect_duplicate_capabilities.py
duplicate capability validation passed

D:/xianyu/.venv/Scripts/python.exe scripts/security_scan.py
security scan passed

D:/xianyu/.venv/Scripts/python.exe -m pytest tests/contract/test_security_boundary.py tests/contract/test_account_security.py tests/contract/test_message_security.py tests/contract/test_publish_security.py tests/contract/test_reply_security.py tests/contract/test_schedule_security.py -q
27 passed

D:/xianyu/.venv/Scripts/python.exe -m ruff check .
All checks passed

git diff --check
PASS
```

Repository deterministic verification:

```text
D:/xianyu/.venv/Scripts/python.exe scripts/validate_change.py
ERROR: missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md

D:/xianyu/.venv/Scripts/python.exe scripts/verify_repository.py
ERROR: missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md
```

This matches the previously classified global CHG-0020 archive debt and is outside the CHG-0030 scoped patch. No CHG-0030 scoped test failed after the follow-up patch.

## GitHub PR #45 current-commit CI

Commit:

```text
fcaf869f2551341e9e0dcbf057d9af58e72e3e08
```

Remote branch equality:

```text
LOCAL=fcaf869f2551341e9e0dcbf057d9af58e72e3e08
REMOTE=fcaf869f2551341e9e0dcbf057d9af58e72e3e08
```

PR:

```text
PR #45
URL=https://github.com/yuanweizhang94-crypto/XIANYU/pull/45
HEAD=feat/CHG-0030-fresh-item-sync-controlled-canary
BASE=main
HEAD_SHA=fcaf869f2551341e9e0dcbf057d9af58e72e3e08
```

Check rollup:

```text
deterministic-security-scan=PASS
quality=FAIL_PRE_EXISTING_CHG0020_VALIDATION_DEBT
tests=FAIL_PRE_EXISTING_GLOBAL_DEBT
```

CI test summary:

```text
602 passed, 11 failed
```

Scoped CHG-0030 CI status:

```text
tests/unit/test_chg0030_fresh_item_sync_canary_patch_artifact.py: PASS
changes/active/CHG-0030-fresh-item-sync-controlled-canary/tests/test_acceptance.py: PASS
```

The 11 CI test failures match the pre-existing debt classes already independently classified for this PR:

- README active-change wording drift;
- CHG-0022 tests bound to an archived active-path assumption;
- AGENTS drift;
- CHG-0020 archived change validation debt.

`SCOPED_CI=PASS`

`GLOBAL_CI=FAIL_PRE_EXISTING_DEBT`

## Backend r2 deployment

Deployment authorization: Phase 4b. No Item Sync invocation was performed.

Pre-deploy selected account catalog baseline:

```text
MASKED_ACCOUNT=22*********60
LOCAL_XY_CATALOG_ITEMS_ROWS=20
DUPLICATE_GROUP_COUNT=0
DUPLICATE_ROW_COUNT=0
ACCOUNT_STATUS=active
```

Pre-deploy service state:

```text
Backend image=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r1 image_id=sha256:52af6761e3e6604b5e926977daf46432e53d2ec7bfd4818bb97660e7a1175586 RestartCount=0 health=/health HTTP_200
WebSocket image=xianyu-chg0023-websocket:readiness-contract-20260822-r1 image_id=sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256 RestartCount=0 health=HTTP_200
Scheduler image=xianyu-chg0027-scheduler:session-cooldown-lineage-20260824-r1 image_id=sha256:ab70f051e962a3138103de969e6976e13c923da86d9222eabf2b9223394331e8 RestartCount=0 health=HTTP_200
Frontend image=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2 image_id=sha256:71cfebe276e3d5ca84db01cd9ed1e6b70211dedf75cbe1b3da210b19e19da416 RestartCount=0 health=HTTP_200
```

R2 build:

```text
BUILD_BASE_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r1
BUILD_REPLAY_SOURCE=D:/xianyu-worktrees/_chg0030_two_patch_replay_20260825111651
PATCH_STACK=chg0030-fresh-item-sync-controlled-canary.patch + chg0030-fresh-item-sync-skipped-lock-success-guard.patch
R2_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2
R2_IMAGE_ID=sha256:f877b7273b2f4e23ff5f0dd5e599dbf860c1e83bc801fca8a26bea815cae4573
BUILDER_PY_COMPILE=PASS
BUILDER_MARKERS_PRESENT=OWNER_LOCK_OCCUPIED_SKIPPED,FULL_ACTIVE_LIST_NOT_CONFIRMED,CHG0030_ITEM_SYNC_TERMINAL_READBACK,platform_verification_evidence_type
```

Runtime r2 source hashes:

```text
/app/common/schemas/item.py sha256=d0ddda47586132cb0b9121ebe85d16d4d6050d42da2f34e572a90f5c56ed5fd4
/app/backend-web/app/api/routes/cookies.py sha256=af45aff224d64497ea7441db0baec3b6fbe1133b6f1faac79b253c0c9099e267
/app/backend-web/app/api/routes/items.py sha256=b7ba35f791c4dfea52f957629789bc3eb339fed1c2ad575fc7fa25ebaf55f6c7
```

Rollback:

```text
R1_ROLLBACK_CONTAINER=xianyu_chg0030_backend_web_pre_chg0030_r2_20260825_phase4b
R1_ROLLBACK_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r1
R1_ROLLBACK_IMAGE_ID=sha256:52af6761e3e6604b5e926977daf46432e53d2ec7bfd4818bb97660e7a1175586
CHG0029_ROLLBACK_CONTAINER=xianyu_chg0029_backend_web_pre_chg0030_20260825_phase4
CHG0029_ROLLBACK_IMAGE=xianyu-chg0029-backend-web:selected-account-on-demand-20260825-r2
CHG0029_ROLLBACK_IMAGE_ID=sha256:4663ca89ba9702bc4f53572593f47f7413cd82e77919ee43b619fba63dbfa7f1
```

Post-deploy service state:

```text
Backend image=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2 image_id=sha256:f877b7273b2f4e23ff5f0dd5e599dbf860c1e83bc801fca8a26bea815cae4573 RestartCount=0 health=/health HTTP_200
WebSocket image=xianyu-chg0023-websocket:readiness-contract-20260822-r1 image_id=sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256 RestartCount=0 health=HTTP_200
Scheduler image=xianyu-chg0027-scheduler:session-cooldown-lineage-20260824-r1 image_id=sha256:ab70f051e962a3138103de969e6976e13c923da86d9222eabf2b9223394331e8 RestartCount=0 health=HTTP_200
Frontend image=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2 image_id=sha256:71cfebe276e3d5ca84db01cd9ed1e6b70211dedf75cbe1b3da210b19e19da416 RestartCount=0 health=HTTP_200
```

## Backend r2 selected-account preflight

HTTP route:

```text
GET /api/v1/cookies/details/paginated?page=1&page_size=5&account_id=60
AUTH_SOURCE=existing COMPANY backend token file
AUTH_VERIFY=true
```

Sanitized selected-account facts:

```text
MASKED_ACCOUNT=22*********60
ROUTE_TOTAL=1
STATE=READY
ITEM_SYNC_ELIGIBLE=true
FAIL_CLOSED=false
FAILURE_REASONS=[]
DISABLED=false
CHECKING_STATE=REAL_BROWSER_LOGIN_READY
CHECKING_ACTIVE=false
PLATFORM_VERIFICATION_SOURCE=none
PLATFORM_VERIFICATION_EVIDENCE_TYPE=NONE
PLATFORM_VERIFICATION_REQUIRED=false
SESSION_COOKIE_LINEAGE=MATCH
TOKEN_READY=true
```

`source=none` is accepted here because the deployed classifier returned authoritative `evidence_type=NONE` with `required=false`; it is not inferred from the absence of a flag.

Post-deploy selected account catalog baseline:

```text
MASKED_ACCOUNT=22*********60
LOCAL_XY_CATALOG_ITEMS_ROWS=20
DUPLICATE_GROUP_COUNT=0
DUPLICATE_ROW_COUNT=0
```

COMPANY adapter check:

```text
ADAPTER_FILE=D:/TikTok_Auto/devspace_proxy/proxy.cjs
ADAPTER_SHA256=4013CF505BA036FFF11F0382761F14BE7711E8280DDD41097C285DC8D7FDE041
ROUTE=/api/v1/items/get-all-from-account?no_auth_recovery=true
OWNER=ItemService.fetch_all_items_from_account
DEFAULT_PAGE_SIZE=20
DEFAULT_MAX_PAGES=20
```

For the selected 20-row account, the current adapter defaults do not cap the canary incompletely: `page_size=20,max_pages=20` allows page 1 plus page 2 empty/short-list confirmation before reaching the cap. The r2 backend still fails closed if `full_active_list_confirmed` is false.

Post-deploy log/safety counters:

```text
CHG0030_ITEM_SYNC_PREFLIGHT_STATUS=1
CHG0030_ITEM_SYNC_OPERATION_ACCEPTED=0
CHG0030_ITEM_SYNC_TERMINAL_READBACK=0
GET_ALL_FROM_ACCOUNT=0
FETCH_ALL_ITEMS_FROM_ACCOUNT=0
PUBLISH_ITEM=0
SEND_MESSAGE=0
QR_LOGIN=0
RECONNECT=0
BATCH_OFFLINE=0
BATCH_DELETE=0
ACCOUNT_MUTATION=0
```

Operational gate state after r2:

```text
SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY=PASS
TRACE_IDENTITY_AVAILABLE=PASS_BACKEND_LOG_CONTRACT
SKIPPED_LOCK_SUCCESS_GUARD=PASS_DEPLOYED
FULL_ACTIVE_LIST_SUCCESS_GUARD=PASS_DEPLOYED
ITEM_SYNC_INVOCATION_COUNT=0
COMMANDER_GO_RECEIVED=false
```
