# CHG-0032 Archived Active-Change Baseline Repair

Date: 2026-08-30

## Execution contract

User outcome: repair the archived CHG-0032 governance test so later legitimate active Changes do not fail CI.

Confirmed blocker: `test_generated_project_state_has_no_active_change_after_archive` encoded the one-time post-archive snapshot `active_change=None` as a permanent repository invariant.

Smallest success test: preserve the rule that archived CHG-0032 cannot become active again while allowing either no active Change or a later legitimate active Change.

## Original intent evidence

CHG-0032 is recorded as `Status: ARCHIVED` in its proposal, design, tasks, and acceptance documents. Task T11 explicitly describes archiving CHG-0032 and regenerating project state to `active_change/null` and `next_task/null` as the closure state for that Change at that moment.

Repository lifecycle governance does not define `active_change=None` as a permanent global invariant. `scripts/repo_utils.py` discovers the current directory under `changes/active/`, allows at most one active Change, and recognizes `DRAFT`, `APPROVED`, `IMPLEMENTING`, and `VERIFYING` as active lifecycle statuses. `contracts/schemas/project-state.schema.json` explicitly allows `active_change` to be either `null` or a valid Change object.

Therefore the archived CHG-0032 test must protect CHG-0032's archived lifecycle identity, not prohibit all future active Changes.

`STALE_ASSERTION_PROVEN=true`

`CHG0032_TEST_ORIGINAL_INTENT=ARCHIVED_CHG0032_MUST_NOT_REMAIN_OR_RETURN_AS_ACTIVE_CHANGE`

## Repair semantics

Old assertion semantics:

`PROJECT_STATE.active_change must always be None after CHG-0032 archive`

New assertion semantics:

`PROJECT_STATE.active_change may be None or a later legitimate Change, but it must never identify/path to archived CHG-0032. When there is no active Change, generated task state remains zero/null as before.`

The repair does not delete, skip, xfail, comment out, or trivialize the lifecycle check.

## Required scenarios

1. CHG-0032 archived + `active_change=None` -> accepted.
2. CHG-0032 archived + `active_change=CHG-0036` -> accepted.
3. CHG-0032 archived + `active_change=CHG-0032` -> rejected.

## Scope

Changed governance test only plus this evidence record.

No Publisher, Session, Cookie, Chat runtime, Account, Material, Backend, Frontend, CHG-0036 regression logic, Runtime, platform write, message, order, auto-reply, or account-state behavior is modified.
