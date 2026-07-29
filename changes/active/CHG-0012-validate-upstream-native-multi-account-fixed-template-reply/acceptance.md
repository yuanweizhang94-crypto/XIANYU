Change ID: CHG-0012-validate-upstream-native-multi-account-fixed-template-reply
Status: APPROVED
# Acceptance

## APPROVED acceptance criteria

- The scope validates and configures upstream native multi-account fixed-template automatic reply.
- The reuse decision is `CONFIGURE_UPSTREAM`.
- The pinned upstream SHA is recorded.
- Upstream UI/API/service/data model evidence is listed.
- Existing local overlap is searched and tied to `docs/LOCAL_COMPONENT_DISPOSITION.md`.
- Duplicate local implementation risk is documented.
- Component ownership is explicit.
- CHG-0010 local autoreply worker remains `FREEZE_AND_DEPRECATE`.
- A live validation safety gate is documented.
- A sole-executor guarantee is documented.
- Stop and rollback plans are documented.
- No business code is modified.
- No generated file is manually edited.
- Owner approval for run `CHG12-20260730-0237-FE2R` is recorded.
- The approved validation uses only upstream native configuration and online-chat text trigger APIs.
- No account login, scan login, item/order/refund/shipping/rating operation, AI reply, image reply, local sender, or upstream source change is authorized.

## Future executable acceptance criteria

For the approved executable validation, acceptance requires:

1. Two dedicated test accounts independently exist through upstream native UI.
2. Account A and account B login states are independent.
3. Account A and account B WebSocket states are independent.
4. Account A and account B have independent rule configuration and different text keywords.
5. Account A keyword does not trigger account B reply.
6. Account B keyword does not trigger account A reply.
7. Default reply is correct.
8. `reply_once` is correct.
9. Product-specific keyword or default reply is correct.
10. Variable replacement uses only variables confirmed in pinned upstream.
11. Message filtering works.
12. Pause automatic reply works.
13. Resume automatic reply works.
14. Reply delay works.
15. Duplicate message protection works.
16. Upstream native autoreply logs are complete for redacted evidence.
17. Manual intervention pause behavior matches expectation.
18. Risk-control or verification state stops validation.
19. Only upstream native sender runs.
20. Local CHG-0010 worker remains stopped throughout.

## Required owner-approved live matrix

Real validation may start only for the approved matrix below after this approval PR is merged and local `main` is synced:

- Test account A masked identifier: `ACCOUNT-A`.
- Test account B masked identifier: `ACCOUNT-B`.
- Controlled counterpart identity: `ACCOUNT-A` and `ACCOUNT-B` are each other's controlled test counterpart.
- Test time window: starts after approval PR merge and local `main` sync; maximum duration 4 hours from that synced-main start time.
- Test keywords: listed in the approved run matrix below.
- Expected reply for each test case: listed in the approved run matrix below.
- Expected send count for each test case: listed in the approved run matrix below.
- Total approved text-message send cap: 12 total outbound text autoreplies across both accounts and all cases.
- Native autoreply start command: `Set-Location D:\xianyu-upstream-pilot; docker compose -f .\.pilot\docker-compose.pilot.yml up -d websocket`.
- Native autoreply stop command: `Set-Location D:\xianyu-upstream-pilot; docker compose -f .\.pilot\docker-compose.pilot.yml stop websocket`.
- Native WebSocket start command: `Set-Location D:\xianyu-upstream-pilot; docker compose -f .\.pilot\docker-compose.pilot.yml up -d websocket`.
- Native WebSocket stop command: `Set-Location D:\xianyu-upstream-pilot; docker compose -f .\.pilot\docker-compose.pilot.yml stop websocket`.
- Rollback method: pause/disable both accounts, stop `websocket`, verify 18090 stopped, verify no sender/reconnect risk, delete only run-id temporary rules, restore pre-test config, preserve masked evidence.
- Masked log/evidence location: `changes/active/CHG-0012-validate-upstream-native-multi-account-fixed-template-reply/evidence/CHG12-20260730-0237-FE2R-masked-report.md` when the completion phase records results.
- Risk stop conditions: the full list in this acceptance file.
- Sole-executor confirmation: upstream native automatic reply only; CHG-0010 local worker must remain stopped; wrapper listener must remain stopped.
- Image-send approval, when applicable: denied.

The matrix is complete only when:

- Controlled counterpart identity identifies the controlled test counterpart, not a generic counterpart label.
- Test time window records an explicit start and end time or an approved time period.
- Both test accounts use masked identifiers.
- No real Cookie, Token, phone number, complete account name, complete session ID, or other secret is recorded.
- Missing any required field blocks validation from starting.
- Changed approval content is reapproved before use.

## Approved run matrix

- Run ID: `CHG12-20260730-0237-FE2R`.
- `TEST-ITEM-1` is an existing item owned by `ACCOUNT-B`.
- Use the upstream online-chat text path only: `frontend/src/pages/chat-new/ChatNew.tsx` -> `frontend/src/api/chatNew.ts` -> `POST /api/v1/chat-new/send-message/{account_id}` -> `backend-web/app/services/chat_new/im_client.py::IMClient.send_text_message`.
- `SendMessageRequest` fields are `cid`, `toUserId`, and `text`.
- Text trigger sends must use the current logged-in upstream session and must not print Cookie, Token, full account id, full item id, full session id, nickname, phone number, or real customer message body.

| # | Target autoreply account | Trigger sender | Trigger text | Expected reply | Expected outbound autoreply count | Stop condition |
|---|---|---|---|---|---:|---|
| 1 | ACCOUNT-A | ACCOUNT-B | `AKEY-CHG12-20260730-0237-FE2R` | `账号A固定回复测试成功-CHG12-20260730-0237-FE2R` | 1 | wrong account, wrong session, wrong text, or duplicate reply |
| 2 | ACCOUNT-A | ACCOUNT-B | `BKEY-CHG12-20260730-0237-FE2R` | no reply | 0 | any outbound autoreply |
| 3 | ACCOUNT-A | ACCOUNT-B | `AUNMATCHED-CHG12-20260730-0237-FE2R` | `账号A默认回复测试成功-CHG12-20260730-0237-FE2R` | 1 | wrong default reply or duplicate reply |
| 4 | ACCOUNT-A | ACCOUNT-B | approved repeat of A default/reply_once input | first approved reply only; repeat must not create a second reply | <= 1 | reply_once repeats unexpectedly |
| 5 | ACCOUNT-B | ACCOUNT-A | `BKEY-CHG12-20260730-0237-FE2R` | `账号B固定回复测试成功-CHG12-20260730-0237-FE2R` | 1 | wrong account, wrong session, wrong text, or duplicate reply |
| 6 | ACCOUNT-B | ACCOUNT-A | `AKEY-CHG12-20260730-0237-FE2R` | no reply | 0 | any outbound autoreply |
| 7 | ACCOUNT-B | ACCOUNT-A | `BUNMATCHED-CHG12-20260730-0237-FE2R` | `账号B默认回复测试成功-CHG12-20260730-0237-FE2R` | 1 | wrong default reply or duplicate reply |
| 8 | ACCOUNT-B | ACCOUNT-A | `PRODUCT-CHG12-20260730-0237-FE2R` in the `TEST-ITEM-1` conversation | `商品专属回复测试成功-CHG12-20260730-0237-FE2R` | 1 | wrong item, wrong account, wrong text, or duplicate reply |
| 9 | ACCOUNT-B | ACCOUNT-A | `VARIABLE-CHG12-20260730-0237-FE2R` | `变量替换测试成功-CHG12-20260730-0237-FE2R-VARIABLE-CHG12-20260730-0237-FE2R` using upstream `{send_message}` formatting | 1 | raw placeholder remains or text mismatch |
| 10 | ACCOUNT-B | ACCOUNT-A | `FILTER-CHG12-20260730-0237-FE2R` | no reply | 0 | any outbound autoreply |
| 11 | ACCOUNT-B | ACCOUNT-A | `RESUME-CHG12-20260730-0237-FE2R` | pause phase: no reply; resumed phase: `暂停恢复测试成功-CHG12-20260730-0237-FE2R` | 1 | reply during pause or no reply after resume |
| 12 | ACCOUNT-B | ACCOUNT-A | `DEDUP-CHG12-20260730-0237-FE2R` sent twice in approved order | `延迟去重测试成功-CHG12-20260730-0237-FE2R` once after approved 2-5 second delay | 1 | early reply, duplicate reply, or more than one reply |

## Text-message send cap

Recommended maximum first matrix send count: 12 total text messages across both test accounts and all test cases. This is not 12 per account and not 12 per test scenario.

- Inbound messages do not count toward the cap.
- Only outbound messages actively sent by the test system count toward the cap.
- Retries, duplicate sends, and abnormal sends count toward the cap.
- When the cap is reached, validation stops immediately and must not continue.
- Image keyword reply is static audit only unless the project owner separately approves a real image send smoke test.
- Image sends are excluded from the 12 text-message approval and require separate approval.
- If the operator is unable to determine whether a message was sent, count it as sent and stop.

## Risk stop conditions

Stop immediately and fail closed on:

- CAPTCHA.
- Slider verification.
- Face verification.
- Device verification.
- Risk-control warning.
- Unknown login state.
- Unknown account state.
- Unknown WebSocket state.
- Unknown sender identity.
- Unknown recipient identity.
- More than one possible send executor.
- Unexpected reply content.
- Unexpected target account or item.
- Reply loop.
- Batch trigger.
- Duplicate or repeated send.
- Any item, order, refund, shipping, or rating operation prompt.
- Sensitive information exposure.
- Unable to determine whether a message was sent.
- Unable to determine whether the stop command took effect.
- Unable to confirm native autoreply is stopped.
- Unable to confirm native WebSocket is stopped.
- Unable to confirm the local CHG-0010 worker remains stopped.
- Message count reaches or may have exceeded the approved cap.

Unknown state = stop, not retry.

Operators must not use repeated starts, repeated stops, relogin, automatic retries, or continued sends to determine state.

## Stop and rollback acceptance

Any future executable validation must document and follow this ordered stop sequence:

1. Block initiation of any new test case.
2. Record the current approved and observed send count using masked evidence.
3. Issue the approved native autoreply stop command.
4. Verify native autoreply is stopped using an approved observable criterion.
5. Issue the approved native WebSocket stop command.
6. Verify native WebSocket is stopped using an approved observable criterion.
7. Verify no scheduler, restart policy, supervisor, or container policy can reactivate a sender.
8. Verify CHG-0010 local worker remains stopped.
9. Verify no second or unknown send executor exists.
10. Disable or remove only the approved test rules.
11. Observe the approved quiet period and confirm no further outbound message occurs.
12. Preserve masked evidence.
13. Generate the masked validation report.

The owner-approved stop criteria must include:

- Native autoreply stopped: approved process/service/container status shows stopped or disabled, no active autoreply worker is present, and no approved rule execution can begin.
- Native WebSocket stopped: approved connection/process status shows disconnected or stopped, no reconnect loop is active, and no scheduler or restart policy will reconnect it.
- No further message can send: no active sender executor, no queued approved test message remains, approved quiet period completes with no new outbound message, and no automatic restart or reconnect occurs.
- CHG-0010 worker stopped: repository status command reports `running=False` and no matching worker process exists.

If a stop command fails, returns an unknown result, times out, or cannot be independently verified, validation enters `STOP_STATE_UNKNOWN`, issues no additional test message, starts no other executor, does not retry platform actions automatically, preserves masked diagnostics, escalates to the project owner, and treats the validation as failed.

Before validation starts and before each scenario, reactivation risk must be checked for Docker restart policy, Compose restart policy, scheduler, supervisor, Windows scheduled task, background launcher, autoreconnect loop, and service dependency. If any mechanism can reactivate a sender or WebSocket, validation must not start or must terminate immediately.

Rollback may only stop upstream native autoreply, stop upstream native WebSocket, confirm local CHG-0010 worker remains stopped, disable or remove approved test rules, restore approved pre-test configuration, preserve masked evidence, and generate a masked failure report. Rollback must not delete production data, clean unknown data, modify upstream source code, enable a local substitute executor, or automatically continue testing.

## Verification commands

DRAFT creation verification:

- `python scripts/generate_state.py`
- `python scripts/validate_change.py`
- `python scripts/project_context.py`
- `python scripts/verify_repository.py`

## Upstream capability audit

Pinned upstream evidence covers account, login, WebSocket, keyword, image keyword configuration, default reply, `reply_once`, product-specific reply, variable replacement, message filtering, pause/resume, reply delay, duplicate protection, and autoreply logs.

## Pinned upstream evidence

- Path: `D:/xianyu-upstream-pilot`
- SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Branch state: detached HEAD.
- Upstream tracked source modified by this Change: no.

## Existing local implementation search

Local search found CHG-0009 wrapper diagnostics and CHG-0010 local autoreply worker overlap. The local worker is not the formal executor and must not be expanded.

## Reuse decision

Decision: CONFIGURE_UPSTREAM

## Duplicate implementation risk

High if the main repository adds a second sender, local matcher, production YAML rules, local worker extension, local account database, second UI, second API, Cookie vault, WebSocket parser, default reply executor, product reply executor, image executor, AIReplyEngine, delay/pause scheduler, second audit implementation, or second dedup implementation.

## Why upstream cannot satisfy the requirement

Not applicable. This Change assumes upstream native capabilities should be configured and validated first.

## Approved exception ADR

Not applicable. No local build exception is requested.

## Component owner

- Upstream: business app, account login/session, WebSocket, keyword/default/product-specific reply, native sender, logs.
- `D:/xianyu`: safety gate, redacted validation evidence, sole-executor checks, stop and rollback plan, repository governance.

## Retirement plan for overlapping local code

CHG-0010 local worker remains frozen/deprecated. CHG-0015 remains the retirement evaluation phase after upstream native validation.
