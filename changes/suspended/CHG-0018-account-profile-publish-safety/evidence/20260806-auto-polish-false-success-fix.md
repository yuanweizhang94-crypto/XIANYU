# CHG-0018 Auto-Polish False-Success Fix

Status: VERIFYING

## Superseded production state

This file preserves the historical false-success repair stage. Its intermediate Patch SHA and no-production-operation statements are historical, not current production status. Current Vendor Patch SHA256 is `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`; final explicit four-item API success and global polish enablement are recorded in `20260807-final-production-enable-closeout.md`.

## Execution contract

User outcome: stop duplicate or expired-session auto-polish responses from becoming local success and remove frontend wording that implies platform confirmation.

Confirmed blocker: the pinned upstream scheduler converts duplicate responses into success, writes `is_polished=true`, and records success without a platform-state readback.

Smallest success test: only the explicit API success response may set `is_polished=true`; duplicate, session-expired, token-empty, and unknown responses remain non-success with structured result metadata, and the frontend states that local completion is not platform readback confirmation.

## Reuse decision

Decision: PATCH_UPSTREAM.

The existing pinned upstream scheduler, existing `xy_scheduled_polish_log` fields, existing item list, and existing polish log detail UI remain the execution and display owners. No service, task, table, migration, queue, browser path, login path, or platform-state verifier is added.

## Historical state boundary

- Current catalog rows reported by the read-only audit: 44.
- Historical `is_polished=true` rows: 42.
- Historical `is_polished=false/null` rows: 2.
- All 42 historical true rows have incompletely traceable provenance.
- At least part of the 42 rows was produced after `POLISH_DUPLICATE` responses were converted to success.
- The 42 rows cannot be batch-classified as platform-confirmed success.
- This change does not update or reset any historical row and does not trigger polish retry.

## Implementation result

- Only exact `SUCCESS::调用成功` produces `success_confirmed_by_api`, increments success, and writes `is_polished=true`.
- Duplicate codes and messages produce `duplicate_unverified`; they do not write `is_polished=true` or increment success.
- Missing `_m_h5_tk` produces `TOKEN_EMPTY` with `skipped`.
- Session-expired responses produce `session_expired`; the account enters the existing in-memory cooldown, remaining items are skipped, and this path does not trigger password login or Cookie refresh.
- Missing or unknown response payloads produce `UNKNOWN_RESPONSE` and fail closed.
- Existing `xy_scheduled_polish_log.error_message` stores structured JSON containing `api_code`, `api_message`, `result_status`, and `attempted_at`; account and item remain in their existing columns.
- The item list uses `本地记录已完成` and `待擦亮`, with an explicit warning that local state is not platform readback confirmation.
- The polish log detail page displays `接口返回成功`, `重复状态待确认`, `登录已失效`, `失败`, and `任务跳过` from the structured result.

## Actual source paths

The final source was located in `D:/xianyu-upstream-delivery-chg0017` rather than the XIANYU governance repository root:

- `scheduler/app/services/scheduler/polish_task.py`
- `tests/test_chg0018_auto_polish_safety.py`
- `frontend/src/pages/items/Items.tsx`
- `frontend/src/pages/polishLogs/PolishBatchDetail.tsx`

The governance artifact and evidence are stored in `D:/xianyu`:

- `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`
- `vendor/patches/xianyu-auto-reply/README.md`
- `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260806-auto-polish-false-success-fix.md`

## Final validation result

- Fixed upstream baseline: `4c5e1ac5f532c7313365d70409ae115305de8a55`.
- Auto-polish safety tests: 10 passed, 0 failed.
- Combined CHG-0018 targeted tests: 22 passed, 0 failed.
- CHG-0017 regression tests: 58 passed, 0 failed.
- Combined targeted and regression tests: 80 passed, 0 failed.
- Frontend TypeScript/Vite production build: passed with `npm --prefix frontend run build`.
- Full XIANYU repository tests: 594 passed, 1 failed out of 595.
- The only full-repository failure is classified as `EXPECTED_STATE_GATE_FAILURE`.
- Prior state-gate failure: CHG-0018 was truthfully `IMPLEMENTING` while `test_chg0018_is_active_verifying_change` required `VERIFYING`; this was an expected state gate, not a business-code regression.
- Business regression detected: no.
- Vendor patch parse check: passed.
- Vendor patch clean apply check: passed against the fixed-SHA CHG-0017 staged base.
- Vendor patch source equivalence: passed for all 22 patch targets after the patch format's documented LF and end-of-line whitespace normalization.
- Duplicate fix included in patch: yes (`duplicate_unverified`; no success conversion or `is_polished=true`).
- Session fix included in patch: yes (`session_expired`; no success write).
- Unknown-response fail-closed behavior included in patch: yes (`UNKNOWN_RESPONSE`).
- Remaining-item skipped logging included in patch: yes (`for skipped_item in items[item_index + 1:]`, `result_status="skipped"`).
- Frontend semantic fix included in patch: yes (`本地记录已完成`, `重复状态待确认`, `登录已失效`, and the no-platform-readback warning).
- Final vendor patch SHA256: `ED5C9F429E70BC5147A3FEB346E3B30A11141602D05B4C56CD65DD997058686E`.

## VERIFYING entry

- Status transition: `IMPLEMENTING` -> `VERIFYING`.
- Entry basis: final vendor patch SHA256 `ED5C9F429E70BC5147A3FEB346E3B30A11141602D05B4C56CD65DD997058686E`.
- Patch parse check: passed.
- Patch clean apply check: passed.
- Patch/source equivalence check: passed.
- CHG-0018 targeted tests: 22/22 passed.
- CHG-0017 regression tests: 58/58 passed.
- Frontend production build: passed.
- Full repository validation before transition: 594 tests passed; the sole failure was the expected `IMPLEMENTING`/`VERIFYING` state gate.
- Original state-gate test after transition: 1/1 passed.
- Full repository validation after transition: 595/595 passed.
- Business regression detected: no.
- Database writes: 0.
- Redis writes: 0.
- Real platform actions: 0.
- Production container changes: 0.
- This transition does not claim that Xianyu platform state was read back or independently confirmed.

## Runtime boundary

- Database writes: 0.
- Redis writes: 0.
- Real platform actions: 0.
- Production container changes: 0.
- Historical `is_polished=true` rows changed: 0.
- No real polish, publish, login, Cookie refresh, account operation, production container restart/rebuild, PR #26 update, commit, or push was performed for this fix.
