# Change Transition Runbook

Use this runbook when one approved change has been merged and the repository needs to prepare the next change. The transition must be atomic so future agents can discover exactly one source of truth.

## Preconditions

- The previous change PR has been merged.
- The working tree is clean.
- No new business implementation has started for the next change.

## Atomic transition steps

1. Create or switch to the preparation branch for the next change.
2. Move the previous change directory from `changes/active/` to `changes/archive/`.
3. Update the moved change status to `ARCHIVED` in all change files:
   - `proposal.md`
   - `design.md`
   - `tasks.md`
   - `acceptance.md`
4. Create the new unique active change directory under `changes/active/`.
5. Set the new change status to `DRAFT`, or to `APPROVED` only after explicit project-owner approval.
6. Run `python scripts/generate_state.py`.
7. Run `python scripts/verify_repository.py`.
8. Commit the archive move, new active change directory, and regenerated project state in the same preparation commit.

## Invariants

- `changes/active/` contains at most one directory in the final tree.
- `ARCHIVED` changes exist only in `changes/archive/`.
- A `DRAFT` active change may be read and reviewed, but not implemented.
- Business code may be changed only when the active change status is `APPROVED`, `IMPLEMENTING`, or `VERIFYING`.
- The active change `acceptance.md` is the primary scope boundary for allowed and forbidden work.

## Generic example

```text
changes/
  active/
    new-approved-change/
      proposal.md
      design.md
      tasks.md
      acceptance.md
  archive/
    previous-merged-change/
      proposal.md
      design.md
      tasks.md
      acceptance.md
```

In the same commit, the previous change files all declare `Status: ARCHIVED`, the new active change files declare `Status: DRAFT` or `Status: APPROVED`, and `generated/PROJECT_STATE.json` has been regenerated.
