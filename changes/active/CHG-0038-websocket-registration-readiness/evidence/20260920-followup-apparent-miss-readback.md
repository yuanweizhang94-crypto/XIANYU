# CHG-0038 Follow-up Production Incident Readback — 2026-09-20

Change ID: CHG-0038-websocket-registration-readiness
Status: VERIFIED_FOLLOWUP

## Scope

A user-reported apparent Auto Reply miss was investigated from platform-message identity through Native WebSocket, MessageHandler, AutoReplyService, image/text send, send-result writeback, and subsequent organic inbound stability.

Customer-sensitive fields are intentionally omitted. Account identifiers are masked in this repository evidence.

## Authoritative mapping

The reported event did not belong to the previously investigated account. Native message authority mapped it to:

```text
ACCOUNT=221793***3500
CONVERSATION_ID=671160***177
ITEM_ID=1085396433551
SOURCE_MESSAGE_ID_PRESENT=true
SOURCE_MESSAGE_TIME=2026-09-20T15:29:38+08:00
NATIVE_BODY_RECEIVED_AT=2026-09-20T15:29:58+08:00
```

The approximately 20-second difference between the message-embedded timestamp and local receive-log time was also present on unrelated normal messages. It is therefore not evidence of a target-account receive-loop stall by itself; no network-latency or clock-skew cause is asserted from this delta alone.

## Native pipeline evidence

```text
REGISTRATION_ACK_PREVIOUSLY_CONFIRMED=true
CONNECTED_AT_EVENT=true
TOKEN_IN_USE_AT_EVENT=true
HEARTBEAT_CONTINUOUS=true
SOCKET_CLOSE_IN_WINDOW=false
SOCKET_ERROR_IN_WINDOW=false
RECONNECT_IN_WINDOW=false
TASK_LOOP_EXCEPTION_IN_WINDOW=false

NATIVE_WS_BODY_RECEIVED=true
MESSAGE_HANDLER_ENTERED=true
ACCOUNT_ROUTE_MATCHED=true
MESSAGE_FILTER_SKIP=false
AUTO_REPLY_SERVICE_ENTERED=true
MATCHED_RULE_TYPE=default_item
REPLY_MODE=text_image
IMAGE_SEND_WRITE=true
TEXT_SEND_WRITE=true
```

The text send path starts with `send_status=unknown` and asynchronously changes status only after its registered mid Future resolves or the 10-second wait expires. For this event, the persisted activity has `created_at` and `updated_at` in the same second and final `send_status=success`, excluding the 10-second timeout-success path.

Immediately after the two outbound writes, Native WS also received two large response frames followed by two same-conversation PNM push events, matching the normal successful text+image reply pattern seen on other production replies.

Image send itself does not register a send Future in the current implementation, so the image conclusion uses outbound-write success plus the paired same-conversation platform push pattern; no code change is made solely to strengthen observability.

## Manual reply exclusion

No Native WS `manual outbound` event for this conversation was found in the retained runtime logs. Any user-identified later manual reply is excluded from Auto Reply acceptance and is not used as E2E evidence.

## Recurrence classification

```text
SAME_AS_PREVIOUS_NATIVE_INBOUND_TO_HANDLER_GAP=false
FALSE_READY_RECEIVE_LOOP_AT_EVENT=false
CHG0038_RECURRING_FAILURE_PROVEN=false
CODE_CHANGE_REQUIRED=false
PRODUCTION_SWITCH_REQUIRED=false
```

This event is not evidence that `connected=true/token_ready=true` masked a dead receive loop. Native heartbeat traffic continued, the target body entered MessageHandler, AutoReplyService ran, and the reply send path completed.

## Post-incident organic stability

Three consecutive later real buyer inbound messages were observed in production. All three:

```text
NATIVE_WS_INBOUND=true
MESSAGE_HANDLER=true
AUTO_REPLY=true
REPLY_MODE=text_image
IMAGE_REPLY=success
TEXT_REPLY=success
SEND_STATUS=success
MANUAL_REPLY_USED_AS_EVIDENCE=false
```

A later organic inbound on the same masked target account also completed `text_image / success`.

## Readback boundary

The separate ChatNew durable-history API returned an empty conversation/message result for the target conversation during this investigation, so it was not used as proof of platform-visible content. The follow-up conclusion is based on the Native production pipeline, asynchronous send-result writeback, same-conversation platform push pattern, and later organic stability.

## Final follow-up conclusion

```text
FOLLOWUP_INCIDENT_RESULT=PASS
NATIVE_WS_RECURRING_ROOT_CAUSE=NOT_PROVEN
CHG0038_RUNTIME_REMAINS_VALID=true
AUTO_REPLY_RULES_CHANGED=false
GLOBAL_RESTART=false
ACCOUNT_RESTART=false
```
