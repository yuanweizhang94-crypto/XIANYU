# CHG-0017 Laptop Source Sync Masked Report

Run ID: `CHG17-LAPTOP-SOURCE-SYNC-20260805T035232Z`

Purpose: preserve the source, tests, masked evidence, and IMPLEMENTING status
from the production laptop where CHG-0017 runtime validation already passed,
then synchronize the result into existing Draft PR #26.

## Scope

- Repository: `D:/xianyu`
- Candidate upstream worktree: `D:/xianyu-upstream-delivery-chg0017`
- Pinned upstream base: `4c5e1ac5f532c7313365d70409ae115305de8a55`
- Branch: `feat/CHG-0017-upstream-native-auto-ai-delivery`
- PR: `#26`
- PR state before sync: Draft / Open / Unmerged
- Remote PR head before sync: `2c1058fd5c0a9f1a572b578faf913df16e2cbd2b`
- Base main before sync: `3da7f6d5f03f692e4f34f2139ecb5d997a2a8195`

## Runtime Protection

- Production containers inspected only: yes
- Docker compose up/down/restart/build used: no
- Container stop/restart/recreate used: no
- Account start/stop/restart used: no
- Scheduler started: no
- CHG-0010 worker started: no
- Platform verification attempted: no
- Messages sent: `0`
- Product publish attempted: no
- AI provider call attempted during sync: no

Observed protected runtime containers before source sync:

- `xianyu_chg0017_backend_web`: running / healthy
- `xianyu_chg0017_frontend`: running / healthy
- `xianyu_chg0017_websocket`: running / healthy
- `xianyu_chg0017_mysql`: running / healthy
- `xianyu_chg0017_redis`: running / healthy

## Source Artifact

- Patch artifact:
  `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0017-reply-identity-allowlist.patch`
- Patch SHA256:
  `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`
- Patch target count: `12`
- Clean apply check: passed
- Applied-source diff check: passed
- Staged blob equivalence: passed, `12/12`
- Sensitive-shaped test fixtures replaced with synthetic values: yes

Patch target files:

- `backend-web/app/services/ai_reply_service.py`
- `backend-web/app/services/xianyu_publisher.py`
- `common/services/ai_provider_service.py`
- `common/services/publish_execution_service.py`
- `common/utils/item_info_manager.py`
- `frontend/src/pages/accounts/Accounts.tsx`
- `tests/test_chg0017_ai_prompt_validation.py`
- `tests/test_chg0017_gemini_response_parser.py`
- `tests/test_chg0017_publish_login_submit.py`
- `tests/test_chg0017_reply_allowlist.py`
- `websocket/app/services/xianyu/ai_reply_engine.py`
- `websocket/app/services/xianyu/auto_reply_service.py`

## Targeted Offline Tests

Command:

```text
python -m pytest tests/test_chg0017_publish_login_submit.py tests/test_chg0017_reply_allowlist.py tests/test_chg0017_ai_prompt_validation.py tests/test_chg0017_gemini_response_parser.py -q
```

Result: `58 passed`

## Evidence Handling

Original laptop evidence was backed up outside the repository before review:

- Backup directory:
  `D:/xianyu-handoff/LAPTOP-SOURCE-SYNC-20260805-113904/evidence-original-backup`
- Backup hash manifest:
  `D:/xianyu-handoff/LAPTOP-SOURCE-SYNC-20260805-113904/evidence-original-backup-sha256.txt`

Repository evidence submitted by this sync is limited to masked Markdown
reports. Raw screenshots, raw browser summaries, logs, Cookie, Token, API keys,
full account IDs, full item IDs, chat IDs, and customer messages are not
submitted.

## Governance State

- Change status after sync: `IMPLEMENTING`
- Completed tasks after sync: `16 / 17`
- Next task after sync: `T17 Archive and deliver.`
- T17 archived: no
- PR #26 kept Draft: yes
- PR #26 merged: no
- Ready transition: no

## Verdict

`LAPTOP_SOURCE_SYNC_READY_FOR_DRAFT_PR`
