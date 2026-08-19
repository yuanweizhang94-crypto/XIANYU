# 2026-08-19 Chain dynamic delivery secret log redaction

## Scope

This is a minimal upstream-first security patch for the existing XIANYU native text sender. It does not change Session, Cookie lifecycle, Token/CAPTCHA, Publisher, Auto Reply, Scheduler, order ownership, or message transport semantics.

## Why it is required

The existing upstream-native `XianyuAsync.send_msg` path is the correct sender for per-order dynamic Chain delivery content, and the current internal send endpoint can wait for the native platform send result. However, the sender previously logged the first 50 characters of every successful text message. A Chain CDK/recharge payload is an order-delivery secret and must not be persisted in ordinary logs.

## Minimal change

Patch artifact:

`vendor/patches/xianyu-auto-reply/bda1a85-chain-delivery-secret-log-redaction.patch`

Only the successful text-send log line changes:

- before: logs the first 50 characters of `content`;
- after: logs only `content_length`.

The text sent to the official XIANYU WebSocket is unchanged. Send-result waiting and rejection detection remain unchanged.

## Runtime evidence

Current production WebSocket container was patched in place and self-restarted through its existing `/internal/system/self-restart` route. Readback after restart confirmed the running file contains only:

`发送消息成功: content_length={len(content)}`

for this success log path.

No real CDK was used for validation and no buyer message was sent for this patch test.

## Security rule

`DELIVERY_SECRET_PERSISTENCE=LOCAL_PROTECTED_ONLY`

Dynamic delivery content may exist transiently in process memory and in the protected local procurement state required for crash recovery. It must not be written to GitHub, normal logs, docs, console output, persistent-job ordinary logs, or public MCP audit output.

## Remaining proof boundary

A real already-paid Chain order bound to a real XIANYU paid order was not available during this validation. Therefore real `XIANYU_SEND_PASS`, `SEND_SUCCESS_READBACK_PASS`, and shipment-confirm-after-send remain `NOT_PROVEN` until the next legitimate paid order reaches the delivery-ready state. No new procurement was created solely for testing.
