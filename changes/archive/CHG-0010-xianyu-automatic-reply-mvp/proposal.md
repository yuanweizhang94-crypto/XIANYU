Change ID: CHG-0010-xianyu-automatic-reply-mvp
Status: ARCHIVED
# Proposal

## Title

CHG-0010 Xianyu automatic reply MVP

## Owner approval

The project owner explicitly corrected the next-stage direction after CHG-0009: the target is automatic reply after new Xianyu inbound messages arrive, not an interactive operator workflow. The project owner authorized a dedicated-test automatic reply MVP that reuses the CHG-0009 Wrapper and does not require per-message selection, per-message reply entry, or per-message SEND confirmation.

## Goal

When a new inbound Xianyu message arrives for the dedicated test account, the system reads it through the existing localhost Wrapper, matches deterministic local rules, sends an automatic reply through the existing Wrapper send boundary, records idempotency/audit state, and avoids duplicate or historical replies.

## Non-goals

- AI large language model replies.
- Automatic bargaining, pricing commitments, refund promises, offline transaction guidance, marketing blasts, or batch messaging.
- Product publishing, delisting, order operations, delivery, refunds, ratings, crawler, promotion, updater, or unrelated scheduler jobs.
- Public web service, cloud deployment, Web UI, or multi-account complex scheduling.
- Reimplementing Xianyu login, WebSocket, message protocols, signing, send protocol, HTTP client, message model, audit, or idempotency.

## Dependencies

CHG-0009 is merged and archived. CHG-0010 reuses `UpstreamWrapper`, `CHAT_NEW_API`, listener control, `NormalizedInboundMessage`, result mapping, localhost restriction, credential redaction, audit, and idempotency boundaries.
