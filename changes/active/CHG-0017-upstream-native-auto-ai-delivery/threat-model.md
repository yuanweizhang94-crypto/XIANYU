Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
# Threat Model

## Primary Risks

- A second local sender or worker could send duplicate replies.
- AI configuration could be incomplete or accidentally enabled outside the approved test scope.
- Keyword/default rules could trigger on real customer messages.
- Token or Cookie material could be printed or committed.
- Scheduler/order/shipping/rating automation could create business side effects.
- Platform verification could require owner action or create risk-control state.

## Controls

- Use only upstream-native runtime paths.
- Keep CHG-0010 frozen, deprecated, and stopped.
- Require whitelist-only accounts for live tests.
- Capture only counts, states, aliases, and redacted hashes.
- Stop on platform verification, unknown sender, unknown account identity, or any non-whitelist message.
- Do not start scheduler or Docker websocket unless the active task explicitly requires the approved upstream candidate service.
- Enforce a hard cap of 8 automatic test replies.

## Secret Handling

Do not print, commit, or place in PR text:

- Cookie
- Token
- API key
- Device ID
- UNB
- Full account ID
- Full chat/session/item ID
- Customer message text
- Verification URL
- Database or Redis credential

## Closeout Requirement

CHG-0017 cannot close as a delivery success unless all test executors are stopped, the quiet period passes, and the final evidence shows zero non-whitelist sends and no business side effects.
