# CHG-0018 Exact Item / No-Retry Canary Patch

Status: VERIFYING
Evidence date: 2026-08-07
Task: CHG0018-EXACT-ITEM-NO-RETRY-CANARY-PATCH

## Superseded production state

This file records the historical exact-item/no-retry deployment stage. Current production closeout supersedes the intermediate Patch/image values below with Vendor Patch SHA256 `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD` and Scheduler image `xianyu-chg0018-scheduler:56d62e2-94c8682`. Final four-item production verification and global enablement are recorded in `20260807-final-production-enable-closeout.md`.

## Execution contract

User outcome: allow the existing `PolishTaskService` to scope an internal controlled run to one account and one exact platform item while ensuring strict item-list validation can stop after the first MTop request.

Confirmed blocker: the existing scheduler supported only account scope and a per-account item limit, while the two audited accounts had multiple eligible items. `ItemInfoManager.get_item_list_info` also performed recursive Token-expiry retry inside the same method.

Smallest success test: default-off `platform_item_ids`, default-compatible `retry_on_token_expiry=True`, SQL-level exact-item filtering, one-request item-list strict mode, unchanged default production calls, and no real polish or publish.

## Reuse decision

Decision: `PATCH_UPSTREAM`.

The implementation modifies only the pinned upstream `PolishTaskService`, `ItemInfoManager`, and the existing CHG-0018 safety test file. It adds no service, HTTP API, frontend control, scheduler task, database model, database field, Token system, Cookie recovery system, Profile manager, queue, or second execution owner.

Duplicate-development risk: low. The existing scheduler and MTop methods remain the sole owners.

Rollback: restore the prior scheduler container/image or remove the optional parameters from the existing methods. No migration or data rollback is required.

## Implementation

- `PolishTaskService.execute` accepts `platform_item_ids: set[str] | None = None` and `retry_on_token_expiry: bool = True`.
- `platform_item_ids=None` preserves the existing item query and normal scheduler calls.
- Exact item scope is applied in the existing `XYCatalogItem` SQL `SELECT` together with account ownership and unpolished-state filters, before the existing item limit.
- Empty, missing, cross-account, and already-polished targets select no item and report `target_item_not_eligible`; no fallback item is selected.
- Controlled logs record masked account scope, requested platform item scope, selected local/platform item identifiers, retry mode, actual request count, API code/message, and result status without Cookie, Token, password, Authorization, or full response data.
- `ItemInfoManager.get_item_list_info` accepts `retry_on_token_expiry: bool = True` at the end of its existing signature.
- Default mode retains recursive Token-expiry/exception retry and response-Cookie handling.
- Strict mode returns the first auth, Token, risk, or unknown failure without recursion and does not accept or persist response Cookies for that call.
- The existing polish MTop method has no recursive retry path. It records `actual_platform_request_count` and remains one request per selected item.
- Duplicate polish responses remain `duplicate_unverified` and do not write `is_polished=true`.

## Validation

- Python syntax compilation: passed for `polish_task.py` and `item_info_manager.py`.
- CHG-0018 targeted tests: 30 passed.
- Exact-item/no-retry safety file: 18 passed.
- CHG-0017 regression tests: 58 passed.
- Combined targeted and regression tests: 88 passed.
- `python scripts/validate_change.py`: passed.
- `python scripts/verify_repository.py`: 595 passed; repository verification passed. The Windows test temporary directory was shortened to avoid an unrelated long-path copy failure in suspended CHG-0017 evidence.
- Vendor Patch parse check: passed.
- Vendor Patch staged-base clean apply check: passed.
- Vendor Patch/current upstream diff byte equivalence: passed for 26 targets.

## Patch artifact

- Path: `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`
- Previous SHA256: `ED5C9F429E70BC5147A3FEB346E3B30A11141602D05B4C56CD65DD997058686E`
- New SHA256: `03F79D07F1177786CF9F9A8B835E71D106BBC4099627A7D39CCA0A3D2F317CCF`
- Fixed upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`

## Production deployment

- Previous scheduler image: `xianyu-chg0018-scheduler:56d62e2-ed5c9f4`.
- New scheduler image: `xianyu-chg0018-scheduler:56d62e2-03f79d0`.
- New image ID: `sha256:20b1dfdfdd638cc6fb5ea79e9d066c6376eb926ad3bcb3d0a13a9b0a253e555a`.
- Only `xianyu_chg0017_scheduler` was replaced.
- Previous scheduler was stopped and retained as `xianyu_chg0017_scheduler_rollback_20260807_121307`.
- Backend, frontend, MySQL, Redis, and WebSocket container IDs remained unchanged.
- New scheduler is running on the existing network and port mapping.
- Production image inspection confirmed exact-item scope and no-retry mode.
- Production polish request path inspection confirmed no recursive retry.
- Before deployment: `polish=false`, `day_switch=true`.
- After deployment: `polish=false`, `day_switch=true`.

## Safety result

- Real polish requests: 0.
- Real publish attempts: 0.
- Cookie refreshes: 0.
- Login actions: 0.
- Messages sent: 0.
- Database schema changes: 0.
- Database business writes: 0.
- Redis writes by this task: 0.
- GitHub writes: 0.
- PR #26 changes: 0.
- Global polish remains disabled.
- The next permitted action is mobile selection of one real currently listed item, followed by a separate explicit authorization for a controlled polish attempt.
