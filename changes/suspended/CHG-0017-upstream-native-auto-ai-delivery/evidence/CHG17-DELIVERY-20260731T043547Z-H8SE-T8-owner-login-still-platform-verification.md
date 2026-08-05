Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
# T8 Owner Login Follow-Up Masked Report

## Scope

- Run ID: `CHG17-DELIVERY-20260731T043547Z-H8SE`
- Task: T8 Validate upstream native Token and account connection.
- Trigger: project owner replied `OWNER_LOGIN_COMPLETED`.
- Upstream candidate SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`

## Token Configuration

- Token mode at preflight: `web`
- Remote Token URL: configured
- Remote Token secret: configured
- Remote Token connectivity test: success
- Remote host recorded: masked only
- Token value printed: no
- Secret value printed: no
- Full URL printed: no

## Preflight

- `ACCOUNT-A` alias: resolved
- `OWNER_TEST_ACCOUNT_B` alias: resolved
- Alias values are distinct: yes
- Active keyword rules: `0`
- Enabled default replies: `0`
- Enabled message filters: `0`
- AI enabled metadata count: `0`
- Autoreply logs before: `0`
- AI chat messages before: `0`
- Candidate websocket before start: stopped
- Old Pilot websocket: stopped
- CHG-0010 worker: stopped
- Manual-listener: stopped

## Attempt

- Upstream native endpoint used: `/internal/accounts/{ACCOUNT-A}/start`
- Account start requests after owner login: `1`
- Account start accepted: yes
- `OWNER_TEST_ACCOUNT_B` touched: no
- Send-message endpoint called: no
- Account task observed: running
- Final connection state: disconnected
- Token obtained: no
- WebSocket connected: false
- Platform verification signal: present

## Cleanup

- `ACCOUNT-A` stop requests: `1`
- `ACCOUNT-A` stop accepted: yes
- Candidate websocket stopped: yes
- Quiet period: 120 seconds
- Reactivation observed: no
- Risk processing rows after quiet period: `0`

## Zero-Send Audit

- Autoreply logs after attempt: `0`
- Successful autoreply sends after attempt: `0`
- AI chat messages after attempt: `0`
- AI assistant messages after attempt: `0`
- Messages sent by this attempt: `0`
- Secrets printed: no
- Full account identifiers printed: no
- Cookie, Token, Device ID, API key, verification URL printed: no

## Verdict

`PLATFORM_VERIFICATION_STILL_REQUIRED`

T8 remains unchecked. CHG-0017 remains `IMPLEMENTING`. No retry was performed.
