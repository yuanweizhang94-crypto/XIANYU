# CHG-0022 Design

Status: ARCHIVED

Change ID: CHG-0022-websocket-token-network-classification

## Design

Preserve the current single WebSocket reconnect loop and its existing network backoff. Modify only the existing exception classification so DNS and other transport failures remain network failures before or after a successful socket connection.

Required behavior:

1. `gaierror`, DNS resolution messages, `ConnectionResetError`, network timeout and existing connection-closed transport errors classify as network failures even when `was_connected=false`.
2. Pre-connect network failures do not run short-disconnect accounting that is meaningful only after a successful connection.
3. Network failures continue through the existing `calculate_network_retry_delay()` / long cooldown path.
4. `attempt_duration < 15` is not authentication evidence and must not delete cached Token.
5. Existing explicit Token/Session response handling in the current Token/Session owner remains unchanged.
6. No second classifier/state machine is introduced outside the existing reconnect branch.

## Upstream capability audit

Latest upstream has the same reconnect branch and defect.

## Pinned upstream evidence

Base `9cbb3725b7e91daec33cb824a3ff4bd84acdcb12`; source `websocket/app/services/xianyu/xianyu_async.py`.

## Existing local implementation search

No tracked equivalent repair exists in recovery branch/archives/vendor tests. Production runtime reproduces the same defect.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No new owner/helper subsystem/cache/scheduler. Existing connection manager and Token/Session owners remain authoritative.

## Why upstream cannot satisfy the requirement

The latest upstream branch still contains the defect.

## Approved exception ADR

Not applicable.

## Component owner

Existing `XianyuAsync` reconnect loop.

## Retirement plan for overlapping local code

Retire the patch when a verified upstream equivalent is available.
