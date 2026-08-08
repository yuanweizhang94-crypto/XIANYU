Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
# T8 Masked Runtime Report

## Scope

- Run ID: `CHG17-DELIVERY-20260731T043547Z-H8SE`
- Task: T8 Validate upstream native Token and account connection.
- Upstream candidate SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`
- Candidate worktree: `D:/xianyu-upstream-delivery-chg0017`
- Runtime type: isolated upstream candidate compose
- Candidate compose path: Git-ignored `.local/chg0017-candidate/docker-compose.yml`
- Candidate env path: Git-ignored `.local/chg0017-candidate/.env`

## Entry Gate

- `ACCOUNT-A` alias: resolved
- `OWNER_TEST_ACCOUNT_B` alias: resolved
- Alias values are distinct: yes
- Active keyword rules: `0`
- Enabled default replies: `0`
- Enabled message filters: `0`
- AI enabled metadata count: `0`
- `ACCOUNT-A` sending-risk flags enabled: `0`
- Old Pilot websocket: stopped
- Host manual-listener: stopped
- CHG-0010 worker: stopped
- Scheduler: stopped
- Candidate ports before start: closed

## Candidate Runtime

- Candidate MySQL: healthy
- Candidate Redis: healthy
- Candidate backend-web: healthy
- Candidate websocket: healthy
- Backend health database status: connected
- Websocket health database status: connected
- Empty service observation: quiet
- Empty service account instances: `0`
- Empty service connected accounts: `0`
- Empty service autoreply log delta: `0`
- Empty service AI message delta: `0`

## T8 Attempt

- Upstream native endpoint used: `/internal/accounts/{ACCOUNT-A}/start`
- Account start requests: `1`
- Account start accepted: yes
- `ACCOUNT-B` touched: no
- Send-message endpoint called: no
- Account task observed: running
- Final connection state: disconnected
- WebSocket connect signal observed: no
- Risk-control processing rows left open: `0`
- Risk log rows increased during observation: yes
- Sanitized log classification:
  - `FAIL_SYS_USER_VALIDATE`: present
  - punish / x5sec validation signal: present
  - token request signal: present
  - send-message signal: absent

## Cleanup

- `ACCOUNT-A` stop requests: `1`
- Candidate compose stopped: yes
- Candidate ports after stop: closed
- Old Pilot websocket after cleanup: stopped
- Host manual-listener after cleanup: stopped
- CHG-0010 after cleanup: stopped
- Quiet period: 120 seconds
- Reactivation observed during quiet period: no

## Zero-Send Audit

- Autoreply logs total after attempt: `0`
- Successful autoreply sends after attempt: `0`
- AI chat messages after attempt: `0`
- AI assistant messages after attempt: `0`
- Messages sent by CHG-0017 T8: `0`
- Secrets printed: no
- Full account identifiers printed: no
- Cookie, Token, Device ID, API key, verification URL printed: no

## Verdict

`PLATFORM_VERIFICATION_REQUIRED`

T8 remains unchecked. CHG-0017 remains `IMPLEMENTING`. The next safe action
requires project-owner approval for an owner-visible upstream-native platform
verification path or a different approved safe Token recovery path. No retry
was performed.
