# CHG17-MULTI-ACCOUNT-20260731T160511Z Masked Report

## Scope

- Change: CHG-0017-upstream-native-auto-ai-delivery
- Stage: CHG0017_MULTI_ACCOUNT_RUNNING
- PR: #26 remains Draft, Open, and Unmerged
- Runtime URL: http://127.0.0.1:19000
- Secrets recorded: no
- Full account identifiers recorded: no
- Cookie, Token, Device ID, UNB, chat/session/customer text recorded: no

## Root Cause

- account_b_login_record=present
- account_b_enabled=true
- account_b_task=not_started before this run
- account_b_websocket=not_started before this run
- account_b_cookie=present_valid
- account_b_root_cause=ACCOUNT-B was logged in and enabled, but no upstream native automatic-reply account task had been started for it. The previous candidate runtime had `AUTO_START_WEBSOCKET=false`, and the CHG-0017 reply gate was configured with ACCOUNT-A/OWNER_TEST_ACCOUNT_B validation-only receiver and sender values.

## Upstream Native Capability

- upstream account start API: present
- upstream account stop API: present
- upstream account status API: present
- upstream connection stats API: present
- CookieManager `start_all_tasks`: present
- CookieManager loads enabled accounts from DB: present
- per-account WebSocket task registry: present
- per-account connection state: present
- per-account AI config: present
- per-account keyword rules/default replies: present
- second local multi-account manager added: no
- second sender/Token/WebSocket/AI worker added: no

## Minimal Fix

- fixed confirmed CHG-0017 patch defect: allowlist values now support `*`
- preserved fail-closed missing-config behavior: yes
- preserved explicit allowlist behavior: yes
- preserved empty sender rejection: yes
- preserved unknown sender rejection: yes
- preserved system sender rejection: yes
- preserved own-message rejection: yes
- changed upstream sender: no
- changed upstream Token flow: no
- changed upstream WebSocket architecture: no
- changed reply priority: no
- local candidate compose set `AUTO_START_WEBSOCKET=true`: yes
- local candidate compose set receiver/sender gate to wildcard values: yes

## Tests

- upstream targeted allowlist tests: 20 passed
- container wildcard function check: passed
- patch numstat parse: passed
- patch clean apply check in external temporary worktree: passed
- `git diff --check` for patched upstream files: passed
- `python scripts/validate_change.py`: passed before evidence update

## Runtime Validation

- services share same candidate runtime: true
- frontend: healthy
- backend: healthy
- MySQL: healthy
- Redis: healthy
- WebSocket: healthy
- ACCOUNT-A record: enabled
- ACCOUNT-A task: running
- ACCOUNT-A websocket: connected
- ACCOUNT-A online status: online
- ACCOUNT-A AI: enabled, Gemini configured
- ACCOUNT-B record: enabled
- ACCOUNT-B task: running
- ACCOUNT-B websocket: connected
- ACCOUNT-B online status: online
- ACCOUNT-B AI: not configured / not enabled
- all started accounts online: true
- executor_per_account: 1
- duplicate_executor_count: 0
- connection stats: 2 total instances, 2 connected
- stop ACCOUNT-A: ACCOUNT-B stayed connected
- start ACCOUNT-A: ACCOUNT-A recovered connected
- stop ACCOUNT-B: ACCOUNT-A stayed connected
- start ACCOUNT-B: ACCOUNT-B recovered connected
- service restart recovery: both enabled accounts recovered connected
- frontend account page: both rows showed enabled and online
- online chat page: both accounts were visible and online

## Safety Counts

- active keyword rules ACCOUNT-A: 0
- active keyword rules ACCOUNT-B: 0
- enabled default replies ACCOUNT-A: 0
- enabled default replies ACCOUNT-B: 0
- ACCOUNT-A auto-reply log total after run: 25
- ACCOUNT-A successful send total after run: 12
- ACCOUNT-A processing rows after run: 0
- ACCOUNT-A AI message total after run: 26
- ACCOUNT-A assistant message total after run: 11
- ACCOUNT-B auto-reply log total after run: 7
- ACCOUNT-B successful send total after run: 0
- ACCOUNT-B processing rows after run: 0
- ACCOUNT-B allowlist skip rows after run: 2
- proactive customer sends by Codex: 0
- manual test messages sent by Codex: 0

ACCOUNT-A remained production-running during this multi-account run and processed new inbound messages through the already-approved production chain. Those records are runtime inbound processing, not proactive sends initiated by Codex. ACCOUNT-B remains AI-disabled / not configured and produced zero successful sends.

## Owner Operating Notes

1. Add or log in an account from Account Management.
2. A logged-in account can still show offline until its account task is started.
3. Enable the account record if it is disabled.
4. Start that account task from the existing account start control or batch start.
5. Confirm online state from the account row or WebSocket account status.
6. Configure AI per account from More -> AI settings.
7. Keep AI disabled if the account should stay online without automatic AI replies.
8. Stop an account task to take only that account offline.
9. Use that account's logs and reply counts from the native pages.
10. Use online chat by selecting the intended account; do not treat another account's sessions as shared.
11. Docker restart now restores enabled accounts through upstream `start_all_tasks`.
12. Avoid duplicate import/start by keeping one account record per platform account and using the existing per-account task status.

## Verdict

MULTI_ACCOUNT_NATIVE_READY
