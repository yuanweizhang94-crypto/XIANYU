# CHG-0017 Laptop Source Sync Status

Change ID: `CHG-0017-upstream-native-auto-ai-delivery`

Status: `IMPLEMENTING`

PR: `#26` / Draft / Open / Unmerged

## Summary

The production laptop's verified CHG-0017 candidate source has been reconciled
into the governance repository as a regenerated upstream vendor patch, masked
evidence, and updated acceptance documentation.

This status page does not authorize archive, merge, Ready transition, live
platform actions, product publish, account operations, or message sends.

## Source Sync

- Local repository branch before sync: `feat/CHG-0017-upstream-native-auto-ai-delivery`
- Remote PR head before sync: `2c1058fd5c0a9f1a572b578faf913df16e2cbd2b`
- Main base before sync: `3da7f6d5f03f692e4f34f2139ecb5d997a2a8195`
- Candidate upstream worktree: `D:/xianyu-upstream-delivery-chg0017`
- Pinned upstream base: `4c5e1ac5f532c7313365d70409ae115305de8a55`
- Patch artifact:
  `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0017-reply-identity-allowlist.patch`
- Patch SHA256:
  `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`
- Patch target files: `12`
- Patch clean apply: passed
- Applied-source diff check: passed
- Staged blob equivalence: passed, `12/12`

## Included Fix Families

- Reply identity allowlist and fail-closed sender gate.
- Catalog-miss account-level fallback with item-scoped side effects disabled.
- Redacted item-list diagnostics.
- Gemini response parser, retry, and quality gate.
- Account-level custom prompt JSON validation.
- Native account UI AI settings validation.
- Product publish login handoff, submit readiness, masked diagnostics, and
  failure classification.

## Included Evidence

Only masked Markdown reports are eligible for Git from the laptop evidence
review. Raw screenshots, browser JSON summaries, logs, Cookie, Token, API keys,
full account IDs, full item IDs, chat IDs, customer messages, and platform
verification URLs remain excluded.

Submitted masked report:

- `changes/active/CHG-0017-upstream-native-auto-ai-delivery/evidence/CHG17-LAPTOP-SOURCE-SYNC-20260805T035232Z-masked-report.md`

Original evidence backup was preserved outside the repository:

- `D:/xianyu-handoff/LAPTOP-SOURCE-SYNC-20260805-113904/evidence-original-backup`

## Offline Verification

Targeted upstream candidate tests:

```text
python -m pytest tests/test_chg0017_publish_login_submit.py tests/test_chg0017_reply_allowlist.py tests/test_chg0017_ai_prompt_validation.py tests/test_chg0017_gemini_response_parser.py -q
```

Result: `58 passed`

## Runtime Boundary

During this source sync:

- Production containers were inspected only.
- Docker compose up/down/restart/build was not used.
- No production container was stopped, restarted, rebuilt, or recreated.
- No account task was started, stopped, or restarted.
- No platform verification was attempted.
- No product publish was attempted.
- No Gemini provider request was made.
- Messages sent: `0`

## Current Governance State

- Completed tasks: `16 / 17`
- Next task: `T17 Archive and deliver.`
- T17: unchecked
- Archive: not authorized
- Merge: not authorized
- PR #26 Ready transition: not authorized

## Verdict

`LAPTOP_SOURCE_SYNC_READY_FOR_DRAFT_PR`
