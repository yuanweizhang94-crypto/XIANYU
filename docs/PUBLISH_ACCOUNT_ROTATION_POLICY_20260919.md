# XIANYU multi-account publish rotation policy — 2026-09-19

Permanent flags:

PUBLISH_ACCOUNT_ROTATION_REQUIRED=true
PUBLISH_ACCOUNT_BALANCING_REQUIRED=true
STRICT_SELECTED_ACCOUNT_AFTER_ASSIGNMENT=true
UNKNOWN_NEVER_MIGRATE=true

## 1. Scope

For ordinary multi-account publishing, when the user has not explicitly assigned a product to a specific account, account assignment must be balanced across the current publish-ready pool.

This is not a fixed round-robin that restarts from the first account every batch. Imbalance carries across batches.

## 2. Eligible account pool

Before assigning each new product, use the formal Publisher capability/state. Exclude HUMAN_QR_REQUIRED, LOGIN_REQUIRED, Publisher-confirmed PLATFORM_VERIFICATION_REQUIRED, account-invalid/publish-forbidden accounts, unresolved UNKNOWN operations, conflicting active real publish executors, and any account that is not PUBLISH_READY.

A temporarily ineligible account receives no new automatic assignment. When it later becomes PUBLISH_READY again, it re-enters with its existing carried success count.

## 3. Balance authority

Count only authoritative successful real publishes:

FINAL_STATUS=SUCCESS and at least one of platform_item_id, item_url, or AUTHORITATIVE_SYNC_CONFIRMED=true.

Do not increment rotation counts for FAILED, UNKNOWN, preflight, Material creation, category selection, or failed/no-create retries.

If one intended product first fails or becomes UNKNOWN and later safely reaches one authoritative SUCCESS, count that intended successful product once.

## 4. Assignment algorithm

1. Read current PUBLISH_READY pool.
2. Read each eligible account's carried authoritative-success count.
3. Find MIN_SUCCESS_COUNT.
4. Candidate pool = eligible accounts at MIN_SUCCESS_COUNT.
5. Choose the next account from that candidate pool using stable rotation order.
6. Assign exactly one product.
7. After authoritative SUCCESS, increment only that account's carried count.
8. Recompute when Runtime capability changes before the next unassigned product.

Therefore, if one account published more items in the previous round, the next round first assigns to lower-count accounts until they catch up.

Example: A=2, B=2, C=2, D=2, E=1, F=1. The next assignments start E, F. Only after E and F reach 2 does ordinary tied rotation resume.

For 10 products across six equally ready accounts, a balanced distribution is normally 2/2/2/2/1/1. The two accounts left at 1 become first priority in the next batch.

## 5. Stable tie order

When multiple eligible accounts have the same carried count, use deterministic continuation from the previous completed assignment order. Do not restart every batch from the same hard-coded first account and do not randomize.

Lower-count accounts always take priority over tie-order continuation.

## 6. Safety boundary

Rotation applies only before formal assignment.

Once MATERIAL_ID + TARGET_ACCOUNT_ID + task_id + idempotency_key exists, the target account remains strict. A publish failure must not automatically migrate the same product to another account merely to improve balancing.

For timeout, 502, connection reset, or response loss: stop writes, perform read-only authoritative recovery, and resolve SUCCESS / FAILED / UNKNOWN. If UNKNOWN remains unresolved, do not migrate or republish.

A controlled retry on the same account is allowed only under existing XIANYU no-side-effect proof and retry rules.

## 7. Explicit user assignment

An explicit user instruction assigning a product to a named account overrides balancing for that item only. If it succeeds, that account's carried success count still increases, so later automatic assignments favor lower-count eligible accounts until balance is restored.

## 8. Current carry baseline

The latest authoritative completed multi-account batch at policy adoption is ASTRA-R2-20260919:

1992416548      = 2
2804730247      = 2
2214313339860   = 2
2196106636      = 2
2221422775489   = 1
2221384086829   = 1

If these six accounts remain PUBLISH_READY at the next ordinary batch start, first balancing priority is:

2221422775489
2221384086829

Only after those two catch up should the four accounts already at 2 receive additional automatically assigned products.

This baseline advances only from authoritative publish results, never from planned assignments or assumed success.
