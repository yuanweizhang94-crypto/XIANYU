Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: SUSPENDED

suspended_from: IMPLEMENTING
suspended_at: 2026-08-05
suspended_reason: Project owner approved prioritizing account credential mis-save, false account disablement, missing account Profile, publish preflight, and browser mutual-exclusion fixes. CHG-0017 code, tests, evidence, and Draft PR remain preserved. T17 was not executed; the Change is incomplete, not archived, and not merged.
resume_condition: Project owner approval after CHG-0018 completion and verification.
# Threat Model

## Primary Risks

- A second local sender or worker could send duplicate replies.
- AI configuration could be incomplete or accidentally enabled outside the approved test scope.
- Keyword/default rules could trigger on real customer messages.
- Token or Cookie material could be printed or committed.
- Scheduler/order/shipping/rating automation could create business side effects.
- Platform verification could require owner action or create risk-control state.
- A local item catalog miss could be misclassified as platform ownership proof,
  either blocking account-level replies unnecessarily or enabling item-scoped
  side effects without local item configuration.

## Controls

- Use only upstream-native runtime paths.
- Keep CHG-0010 frozen, deprecated, and stopped.
- Require whitelist-only accounts for live tests.
- Capture only counts, states, aliases, and redacted hashes.
- Stop on platform verification, unknown sender, unknown account identity, or any non-whitelist message.
- Do not start scheduler or Docker websocket unless the active task explicitly requires the approved upstream candidate service.
- Enforce a hard cap of 8 automatic test replies.
- Treat local catalog misses as `item_catalog_missing`: allow only approved
  account-level text keyword and Gemini paths after the sender allowlist, and
  disable item-scoped keyword/default/image/card/delivery/order/rating/item
  mutation paths.
- Log item sync and catalog-missing diagnostics as counts and classifications
  only.

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
