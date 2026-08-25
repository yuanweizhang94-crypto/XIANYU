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
