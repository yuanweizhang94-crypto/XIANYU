# XIANYU Single-Account Auto Reply Runtime Recovery — 2026-09-20

Status: VERIFYING_POST_RECOVERY_INBOUND

## Scope

This record covers a target-only production Auto Reply recovery. Customer messages, buyer identifiers, credentials, Cookies, Tokens, Authorization values, and private chat contents are not persisted.

```text
TARGET_ACCOUNT=221431***9860
TARGET_NICKNAME=丸子
OTHER_ACCOUNTS_CHANGED=false
GLOBAL_WEBSOCKET_CHANGED=false
AUTO_REPLY_CONFIG_REBUILT=false
CODE_CHANGE=false
```

## Pre-recovery state

Backend/runtime readback:

```text
ACCOUNT_ENABLED=true
ACCOUNT_ONLINE=true
NATIVE_WS_CONNECTED=true
TOKEN_READY=true
PLATFORM_VERIFICATION_REQUIRED=false
HUMAN_QR_REQUIRED=false
REGISTRATION_ACK_2026-09-20_11_12=true
MESSAGE_LOOP_READY=true
HEARTBEAT_CONTINUOUS=true
```

The target had successful native text+image Auto Reply activity at 09:56 and 10:40. After the 10:40 event, no later buyer-body inbound for the target was present in retained Native WebSocket logs before recovery, while other accounts continued to receive and auto-reply to real buyer messages.

A cross-account routing scan used all item IDs configured for the target. From 10:40 onward, none of those item IDs appeared as buyer-body messages under another account. Therefore no wrong-account routing evidence was found.

## Configuration readback

Production database read-only query:

```text
DEFAULT_REPLY_RULE_COUNT=49
DEFAULT_REPLY_ENABLED_COUNT=49
TEXT_READY_COUNT=49
IMAGE_READY_COUNT=49
REPEATABLE_REPLY_COUNT=48
KEYWORD_RULE_COUNT=0
ACCOUNT_STATUS=active
MESSAGE_EXPIRE_TIME_SECONDS=3600
```

The rule/image/text configuration is not the first divergence.

## A/B comparison

A currently healthy account continued to record real inbound -> MessageHandler -> item default rule -> text_image -> send_status=success during the period when the target had no later buyer-body records.

The comparison is used only to distinguish global failure from target-only runtime state; the healthy account's messages are not counted as target acceptance.

## First divergence

```text
FIRST_DIVERGENCE=platform-reported target buyer activity -> target Native WebSocket buyer-body inbound
ACCOUNT_ROUTING_MISMATCH_PROVEN=false
MESSAGE_HANDLER_FAILURE_PROVEN=false
RULE_FAILURE_PROVEN=false
IMAGE_CONFIG_FAILURE_PROVEN=false
TEXT_CONFIG_FAILURE_PROVEN=false
SEND_FAILURE_PROVEN=false
```

This is classified as a target-account Native WebSocket inbound/subscription runtime-state drift. It is not classified as a CHG-0038 global regression because the target had a confirmed registration acknowledgement, continuous heartbeats, and no evidence that other accounts lost inbound delivery.

## Minimal recovery

Only the target Native WebSocket instance was restarted through the existing single-account owner with Token cache preserved:

```text
INVALIDATE_TOKEN_CACHE=false
GLOBAL_RESTART=false
OTHER_ACCOUNT_RESTART=false
```

Post-recovery readback:

```text
TARGET_RESTART_AT=2026-09-20T16:46:19+08:00
REGISTRATION_ACK_AT=2026-09-20T16:46:20+08:00
CONNECTED_AT=2026-09-20T16:46:21+08:00
MESSAGE_LOOP_READY_AT=2026-09-20T16:46:21+08:00
TOKEN_STATE=success_from_cache
TOKEN_READY=true
CONNECTION_FAILURES=0
NETWORK_FAILURES=0
PLATFORM_VERIFICATION_REQUIRED=false
HUMAN_QR_REQUIRED=false
```

ChatNew was connected for the target only to attempt read-only remote-history retrieval. That history endpoint returned an empty conversation list and is not used as causal proof or as the Auto Reply repair.

## Remaining acceptance

No new post-recovery real buyer-body inbound had arrived for the target at the time this record was written.

```text
TARGET_POST_RECOVERY_REAL_INBOUND_COUNT=0
TARGET_POST_RECOVERY_MESSAGE_HANDLER_COUNT=0
TARGET_POST_RECOVERY_AUTO_REPLY_SUCCESS_COUNT=0
REAL_E2E_STABILITY=PENDING_3_REAL_TARGET_INBOUNDS
```

Do not count manual seller replies or successful messages from other accounts toward this gate.
