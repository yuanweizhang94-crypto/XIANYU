# CHG-0017 Final Delivery Report

Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
Run ID: CHG17-FINAL-DELIVERY-20260801T060801Z
PR: #26 Draft, Open, Unmerged
PR exact HEAD: 60c330c31edddc28eae6bb6e1e7748b64a96289a

This report is a delivery closeout report only. It does not archive the Change,
does not mark T17 complete, does not merge PR #26, and does not modify business
runtime code.

No Cookie, Token, API key, Device ID, UNB, full account ID, database primary
key, item ID, chat/session ID, customer message body, full AI reply body,
verification URL, or database credential is recorded here.

## Upstream Reuse

- Delivery decision: CONFIGURE_UPSTREAM with minimal PATCH_UPSTREAM safety fixes.
- Account tasks, IM Token acquisition, WebSocket connection, inbound parsing,
  reply decisioning, AI model invocation, message sending, and reply logs remain
  owned by the upstream candidate runtime.
- Backend account, rule, AI settings, online chat, and service status paths
  remain upstream-native management paths.
- Local repository ownership remains governance, redacted evidence, patch
  artifact, lifecycle checks, and rollback documentation.
- No second IM, Token, WebSocket, sender, AI worker, automatic reply worker,
  multi-account manager, or management UI was created.

## Added Fix Points

- Added fail-closed receiver/sender allowlist support for controlled and
  wildcard production operation.
- Added local catalog-miss fallback so item-scoped side effects are denied while
  account-level text and Gemini routes can continue after allowlist approval.
- Redacted item-sync diagnostics to avoid raw platform request or response data.
- Hardened Gemini response parsing and quality gates: merge final text parts,
  ignore thought parts, reject truncated output, reject leaked templates or
  malformed replies, and keep formal replies and Provider tests on the same
  parser.
- Validated account catalog alignment by applying Gemini configuration to the
  catalog-owning account through upstream `AIReplySettingsService.update_settings`.

## AI Chain

- Provider: gemini.
- Base URL: https://generativelanguage.googleapis.com.
- Model: gemini-3.6-flash.
- Model name prefix `models/`: absent.
- API key: present_redacted.
- Custom prompt format: valid JSON object.
- Product AI prompt format: plain text.
- Provider zero-send test: pass.
- Live reply strategy: ai.
- Live send status: success.
- Reply language: zh-CN.
- Reply completeness gate: pass.
- Markdown leak: 0.
- English/template leak: 0.
- JSON leak: 0.

## Product Context

- Catalog-owning account alias: ACCOUNT-CATALOG.
- WebSocket account alias: ACCOUNT-CATALOG.
- Product catalog row: present.
- Product title: present.
- Product price: present.
- Product description/detail: present.
- Product AI prompt: present.
- Runtime catalog lookup uses the current WebSocket account database primary key
  plus the inbound message item identifier.
- Runtime item information completeness: true.
- The final live AI reply used product context and did not fall back to unknown
  item, missing item information, zero price, or unavailable description.

## Account Mapping

Prior blocker `AFFECTED_ACCOUNT_ITEM_CATALOG_ABSENT` was reclassified as
`AFFECTED_ACCOUNT_IDENTITY_MISMATCH`.

- ACCOUNT-AI previously held Gemini settings.
- ACCOUNT-CATALOG held the visible product catalog row and the connected
  WebSocket task.
- Before alignment, AI settings and product catalog ownership were on different
  account aliases.
- After alignment, ACCOUNT-CATALOG is the effective production AI account.
- Product ownership was not copied or changed.
- Whole account metadata was not copied.
- Gemini settings were applied through the upstream-native service path.

## Test Results

- Targeted acceptance tests: pass.
- Change validation: pass.
- Repository verification: pass, 598 tests passed.
- PR #26 quality CI: success.
- PR #26 tests CI: success.
- PR #26 security CI: success.
- Provider product-context cases: 4 passed.
- Provider sender invocations: 0.
- Provider platform sends: 0.
- Controlled live owner-account test: pass.
- Duplicate sends: 0.
- Duplicate executor count: 0.
- Non-whitelist successful sends: 0.
- Proactive customer sends by Codex: 0.

## Current Online Boundary

- ACCOUNT-CATALOG account task: running.
- ACCOUNT-CATALOG WebSocket: connected.
- ACCOUNT-CATALOG AI: enabled.
- Active keyword rules: 0.
- Enabled default replies: 0.
- PR #26 remains Draft, Open, and Unmerged.
- T17 remains unchecked because archive and merge are not authorized.

Validated by CHG-0017:

- Upstream-native Gemini AI automatic reply for the aligned catalog account.
- Product-aware Simplified Chinese reply generation.
- Native WebSocket and sender chain for the controlled owner-account path.
- Multi-account native account task operation.
- Native management UI alignment with the candidate runtime.
- Stop, reconnect, duplicate protection, rollback drill, and zero non-whitelist
  send audit.

Not validated by CHG-0017:

- Image reply.
- Order, refund, shipping, rating, or listing mutation behavior.
- Proactive customer outreach.
- A second local reply executor.
- Merging PR #26 into main.
- Archiving this Change.

## Rollback

Shortest rollback path:

1. Disable AI for ACCOUNT-CATALOG from the upstream account AI settings UI or
   upstream-native settings service.
2. Stop the ACCOUNT-CATALOG account task from the upstream account management
   stop control.
3. If service-level rollback is needed, stop the candidate WebSocket service
   through the existing compose/lifecycle path.
4. Confirm account task stopped, WebSocket disconnected, active keyword rules
   remain `0`, enabled default replies remain `0`, and no new successful reply
   sends appear after the stop.
5. Keep PR #26 Draft/Open/Unmerged until the owner separately authorizes
   archive, Ready transition, merge, or another delivery action.

## Verdict

CHG0017_DELIVERY_REPORT_READY
