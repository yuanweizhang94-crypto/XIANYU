# CHG-0018 Final Production Enable and Closeout Evidence

Status: VERIFYING
Evidence date: 2026-08-07
Task: CHG0018-FINAL-PRODUCTION-ENABLE-AND-CLOSEOUT

## Reuse decision

Decision: `PATCH_UPSTREAM`.

The existing upstream-native per-item MTop polish path, `PolishTaskService`, `ItemInfoManager`, scheduled-task management route, Scheduler configuration cache, and account/item models remain the only runtime owners. No new API, service, worker, queue, database table, database field, Token system, Cookie system, Profile manager, or second Scheduler was created.

## Final fixed production artifact

- Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.
- Vendor Patch: `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`.
- Vendor Patch SHA256: `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`.
- Production Scheduler image: `xianyu-chg0018-scheduler:56d62e2-94c8682`.
- Production Scheduler image ID: `sha256:fbd83f76745a7d2a56ebc28ad8addfcc47aa35720dbfa5cae021e35d30c2ec4c`.

Earlier Patch SHA values and Scheduler image tags in dated evidence are historical intermediate artifacts and are superseded by the values above for current production state.

## Final controlled end-to-end polish verification

Owner-recovered account session was confirmed before the final controlled run.

Controlled account: `2219319284219`.

The existing `PolishTaskService.execute` path selected only the four owner-authorized platform item IDs. Each item used exactly one polish request, no auth recovery was needed, and all four returned explicit platform API success:

- `1070297095320`: `API_CODE=SUCCESS`, `API_MESSAGE=调用成功`, `is_polished=false -> true`.
- `1073348972265`: `API_CODE=SUCCESS`, `API_MESSAGE=调用成功`, `is_polished=false -> true`.
- `1070510695919`: `API_CODE=SUCCESS`, `API_MESSAGE=调用成功`, `is_polished=false -> true`.
- `1073905692512`: `API_CODE=SUCCESS`, `API_MESSAGE=调用成功`, `is_polished=false -> true`.

Final controlled-run totals:

- `TOTAL_ELIGIBLE_ITEMS=4`
- `TOTAL_PLATFORM_POLISH_REQUESTS=4`
- `TOTAL_AUTH_RECOVERY_ATTEMPTS=0`
- `SUCCESS_ITEM_COUNT=4`
- `DUPLICATE_ITEM_COUNT=0`
- `AUTH_FAILURE_ITEM_COUNT=0`
- `UNKNOWN_FAILURE_ITEM_COUNT=0`
- `SKIPPED_AFTER_FAILURE_COUNT=0`
- `OTHER_ACCOUNT_PLATFORM_REQUESTS=0`
- `OUT_OF_SCOPE_ITEM_REQUESTS=0`
- `ACCOUNT_ALL_ITEMS_PROCESSED=true`
- `END_TO_END_ACCOUNT_POLISH_VERIFIED=true`
- `SAFE_TO_REENABLE_GLOBAL_POLISH=true`

Duplicate responses remain `duplicate_unverified` and do not become explicit success. Session/Token failures remain fail-closed. `platform_item_ids` provides exact controlled scope, and `retry_on_token_expiry` preserves default-compatible behavior. An explicit Session/Token expiry may perform at most one existing auth recovery and one final polish retry; there is no third polish request or unbounded recovery loop.

## Global production enablement

The existing scheduled-task administrator path was used to change only `polish.enabled` from `false` to `true`. The existing 60-second interval was not changed. `day_switch.enabled` remained `true`.

The production Scheduler's existing `/internal/tasks/reload` path reloaded the persisted configuration and reported:

- Scheduler running: true.
- `polish.enabled=true`, interval 60 seconds.
- `day_switch.enabled=true`, interval 60 seconds.
- No second production Scheduler.

One natural Scheduler polish cycle was observed without a manual polish trigger. The cycle completed normally. Healthy accounts continued to produce explicit `SUCCESS`; accounts with expired sessions performed one bounded recovery attempt and then stopped that account while later accounts continued; already-completed accounts had no eligible items. No crash loop, unbounded retry, second Scheduler, or other-service restart was observed. Production Scheduler `RestartCount=0` after the cycle.

Account Session expiry is therefore a runtime account-health condition and is not, by itself, a CHG-0018 code-acceptance failure.

## Final technical conclusions

1. Polish continues to reuse the pinned upstream per-item MTop path.
2. Duplicate remains `duplicate_unverified` and is not rewritten as explicit success.
3. Session/Token failures fail closed.
4. Controlled execution supports exact `platform_item_ids` scope.
5. Controlled/default-compatible execution supports `retry_on_token_expiry`.
6. Polish authentication recovery is bounded to at most one recovery plus one final retry.
7. Infinite authentication recovery is not allowed.
8. Global production polish is re-enabled through the existing scheduled-task management path.
9. Individual account Session expiry is runtime account health, not a CHG-0018 code defect.
10. Reuse decision remains `PATCH_UPSTREAM`.

## Governance state boundary

The repository-defined status sequence contains `DRAFT`, `APPROVED`, `IMPLEMENTING`, `VERIFYING`, `MERGED`, and `ARCHIVED`; it does not define `VERIFIED`. The next formal status after `VERIFYING` is tied to merge. PR #26 is explicitly required to remain Draft/Open/Unmerged in this task, so this closeout evidence does not invent a new status and does not set CHG-0018 to `MERGED`.

T11/T12 real-batch-publish runtime recovery tasks are not proven complete by the final polish evidence and are not falsely marked complete. This task records the completed polish production verification and production enablement while preserving truthful governance state.

## Safety boundary

- Product publishes by this closeout task: 0.
- Messages sent by this closeout task: 0.
- Database schema changes: 0.
- Manual database writes: 0.
- Manual Redis writes: 0.
- New APIs/services/workers/tables: 0.
- Backend/Frontend/MySQL/Redis/WebSocket restarts: 0.
- PR #26 state changes: 0.
