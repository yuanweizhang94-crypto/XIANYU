Change ID: CHG-0012-validate-upstream-native-multi-account-fixed-template-reply
Status: ARCHIVED
# Design

## Validation architecture

CHG-0012 validates pinned upstream native fixed-template automatic reply in a controlled way. `D:/xianyu-upstream-pilot` remains the business app and execution engine. `D:/xianyu` remains the control layer for planning, safety gates, status verification, redacted evidence, and repository validation.

This APPROVED change creates no local runtime path and no business code. It authorizes one controlled live validation phase using pinned upstream native UI/API/service paths, without creating a parallel implementation.

## Static evidence model

The validation plan uses four evidence groups:

1. Pinned source evidence: exact SHA and upstream files for accounts, keywords, default replies, message filters, WebSocket, auto reply, and logs.
2. Local overlap evidence: current local wrapper and CHG-0010 worker disposition.
3. Runtime status evidence: Docker service status, ports, wrapper listener status, local worker status, and process scan.
4. Live validation evidence: only for approved run `CHG12-20260730-0237-FE2R`, using masked identifiers and redacted evidence.

## Upstream UI/API/service/data model evidence

Pinned upstream evidence to audit before execution:

| Scope | UI/API evidence | Service/data evidence |
|---|---|---|
| Multi-account account records | `frontend/src/pages/accounts/Accounts.tsx`, `backend-web/app/api/routes/cookies.py` | `common/models/xy_account.py` |
| Login and account state | account login/status UI and APIs, `websocket/app/api/routes/password_login.py` | `websocket/app/services/xianyu/connection_manager.py` |
| WebSocket connection | online chat UI/status APIs | `backend-web/app/services/chat_new/im_session_manager.py`, `websocket/app/services/xianyu/message_handler.py` |
| Text keyword reply | `frontend/src/pages/keywords/Keywords.tsx`, `frontend/src/api/keywords.ts`, `backend-web/app/api/routes/keywords.py` | `common/models/xy_keyword_rule.py`, `backend-web/app/services/keyword_service.py`, `websocket/app/services/xianyu/auto_reply_service.py` |
| Image keyword configuration | Keywords UI/API upload fields | `XYKeywordRule.image_url`, upstream image keyword handler paths |
| Default reply and reply once | account/item default reply APIs, `frontend/src/api/items.ts` | `common/models/default_reply.py`, `common/utils/default_reply_api.py`, upstream default reply service |
| Product-specific reply | item-bound keyword/default reply APIs | `XYKeywordRule.item_id`, `DefaultReply.item_id`, catalog joins |
| Variable replacement | keyword/default reply UI/API | formatting branches in `websocket/app/services/xianyu/auto_reply_service.py` |
| Message filtering | `backend-web/app/api/routes/message_filters.py` | upstream filter service paths |
| Pause and resume | account pause controls | `XYAccount.pause_duration`, pause checks in upstream services |
| Reply delay | account delay controls | `XYAccount.reply_delay_seconds`, upstream delay load path |
| Duplicate protection | logs and default-reply records | default reply record and duplicate-message log fields |
| Autoreply logs | `frontend/src/pages/autoReplyLogs/AutoReplyLogs.tsx`, `backend-web/app/api/routes/auto_reply_logs.py` | `common/models/auto_reply_message_log.py`, upstream log services |
| Controlled trigger send | `frontend/src/pages/chat-new/ChatNew.tsx`, `frontend/src/api/chatNew.ts` | `backend-web/app/api/routes/chat_new.py`, `backend-web/app/services/chat_new/im_client.py` |

## Execution-state gate

Before any later live validation starts, the operator must confirm all of the following in read-only/status-only mode:

- Main repository is on the authorized branch and active Change status is executable.
- Pinned upstream SHA is still `bda1a859df63fa5f24e51398fa80a23490bb6dfc`, or any SHA change has explicit owner approval and updated audit evidence.
- Docker services required for MySQL, Redis, backend, and frontend are healthy.
- Wrapper-owned listener is stopped unless the approved test matrix explicitly starts it.
- CHG-0010 local autoreply worker is stopped.
- Upstream native WebSocket and upstream native autoreply startup method are explicitly approved for the test matrix.
- No unknown automatic-reply sender process is present.
- No sensitive values are printed in command output.

If any state is unknown, validation must fail closed.

## Approved live validation safety gate

The project owner approved one controlled validation matrix for run `CHG12-20260730-0237-FE2R`. Before real validation starts, the operator must confirm the matrix still matches runtime state:

1. Test account A masked identifier.
2. Test account B masked identifier.
3. Controlled counterpart identity.
4. Test time window.
5. Test keywords.
6. Expected reply for each test case.
7. Expected send count for each test case.
8. Total approved text-message send cap.
9. Native autoreply start command.
10. Native autoreply stop command.
11. Native WebSocket start command.
12. Native WebSocket stop command.
13. Rollback method.
14. Masked log/evidence location.
15. Risk stop conditions.
16. Sole-executor confirmation.
17. Image-send approval, when applicable.

The owner approval record must be complete before any live platform validation starts:

- Controlled counterpart identity must identify the controlled test counterpart; generic "controlled counterpart" wording is insufficient.
- Test time window must include an explicit start and end time or an approved time period.
- Both test accounts must use masked identifiers only.
- The matrix must not record real Cookie, Token, phone number, complete account name, complete session ID, or other secrets.
- Image messages are not approved by default and require separate approval.
- Missing any required field blocks validation from starting.
- Any change to approved content requires reapproval; old approval must not be reused.

Approved account and item scope:

- `ACCOUNT-A` and `ACCOUNT-B` are dedicated controlled test accounts and each other's controlled counterpart.
- Both accounts must be connected and active through upstream native account/chat APIs.
- `TEST-ITEM-1` is an existing item owned by `ACCOUNT-B`; no full item title or full item id may be recorded.
- Only one target account may have autoreply enabled for a scenario. The opposite account is paused/disabled and may only send the trigger text.

Approved trigger send path:

- Frontend page component: `frontend/src/pages/chat-new/ChatNew.tsx`, `sendMessageText`.
- Frontend API client: `frontend/src/api/chatNew.ts`, `sendTextMessage(accountId, cid, toUserId, text)`.
- Backend route: `POST /api/v1/chat-new/send-message/{account_id}`.
- Request schema: `SendMessageRequest` with `cid`, `toUserId`, and `text`.
- Backend service: `backend-web/app/services/chat_new/im_client.py`, `IMClient.send_text_message`.
- Text-only constraint: use only the text route; do not call `sendImageMessage` or any image upload route.
- Send granularity: exactly one request per approved trigger message; no batch send or broadcast.
- Authorization: use current upstream logged-in session through the existing app/API; do not read or print Cookie or Token.
- Non-business constraint: do not invoke order, item mutation, refund, shipping, rating, publish, blacklist, recall, image, AI, or admin mutation paths.

Approved run parameters:

| Field | Value |
|---|---|
| Run ID | `CHG12-20260730-0237-FE2R` |
| ACCOUNT-A keyword | `AKEY-CHG12-20260730-0237-FE2R` |
| ACCOUNT-B keyword | `BKEY-CHG12-20260730-0237-FE2R` |
| default-A unmatched input | `AUNMATCHED-CHG12-20260730-0237-FE2R` |
| default-B unmatched input | `BUNMATCHED-CHG12-20260730-0237-FE2R` |
| product keyword | `PRODUCT-CHG12-20260730-0237-FE2R` |
| variable keyword | `VARIABLE-CHG12-20260730-0237-FE2R` |
| filter keyword | `FILTER-CHG12-20260730-0237-FE2R` |
| resume keyword | `RESUME-CHG12-20260730-0237-FE2R` |
| dedup keyword | `DEDUP-CHG12-20260730-0237-FE2R` |
| ACCOUNT-A keyword reply | `账号A固定回复测试成功-CHG12-20260730-0237-FE2R` |
| ACCOUNT-B keyword reply | `账号B固定回复测试成功-CHG12-20260730-0237-FE2R` |
| ACCOUNT-A default reply | `账号A默认回复测试成功-CHG12-20260730-0237-FE2R` |
| ACCOUNT-B default reply | `账号B默认回复测试成功-CHG12-20260730-0237-FE2R` |
| product-specific reply | `商品专属回复测试成功-CHG12-20260730-0237-FE2R` |
| variable replacement reply | `变量替换测试成功-CHG12-20260730-0237-FE2R-{send_message}` |
| pause/resume reply | `暂停恢复测试成功-CHG12-20260730-0237-FE2R` |
| delay/dedup reply | `延迟去重测试成功-CHG12-20260730-0237-FE2R` |

Rules for any later live validation:

- Use only dedicated test accounts.
- Use only a controlled test counterpart.
- Do not use real customers.
- Test one scenario at a time.
- Limit message count.
- Do not loop sends.
- Do not batch trigger.
- Do not perform item, order, refund, shipping, or rating operations.
- Stop on CAPTCHA, slider, face verification, device verification, risk-control prompt, unknown result, or uncertain permission.
- Never run two automatic-reply send executors at the same time.

## Text-message send cap

The first live validation may send at most 12 total text messages across both test accounts and all test cases.

- The cap is not 12 per account.
- The cap is not 12 per test scenario.
- The cap is 12 total text messages across both test accounts and the entire approved matrix.
- Inbound messages do not count toward the cap.
- Only outbound messages actively sent by the test system count toward the cap.
- Retries, duplicates, and abnormal sends count toward the cap.
- When the cap is reached, validation stops immediately and must not continue.
- Image sends are excluded from the 12 text-message approval and require separate project-owner approval.
- If the operator is unable to determine whether a message was sent, count it as sent and stop.

## Test matrix outline

The later approved matrix should include these scenario groups:

1. Account existence and login-state independence for account A and account B.
2. WebSocket-state independence for account A and account B.
3. Account A text keyword reply.
4. Account B text keyword reply with a different keyword.
5. Cross-account non-trigger checks for A keyword against B and B keyword against A.
6. Default reply check.
7. `reply_once` check.
8. Product-specific keyword or default reply check.
9. Variable replacement using only upstream-supported variables.
10. Message-filter skip check.
11. Pause automatic reply check.
12. Resume automatic reply check.
13. Reply delay observation.
14. Duplicate message protection observation.
15. Upstream native autoreply log review.
16. Manual intervention pause observation.
17. Risk/verification stop drill.
18. Sole-executor and local-worker-stopped confirmation.

Recommended maximum planned live sends for the first approved matrix: 12 total text messages across both test accounts. Image sends are excluded unless separately approved.

Two-account validation requirements:

- Use two dedicated test accounts.
- Record only masked identifiers.
- Confirm independent login state for account A and account B.
- Confirm independent WebSocket state for account A and account B.
- Confirm independent keyword/rule configuration for account A and account B.
- Use the approved controlled counterpart identity only.
- Confirm cross-account keyword isolation before any broader validation.

## Sole executor guarantee

The formal sender for this validation is upstream native automatic reply only. The guarantee method is:

- Check `python -m xianyu_system autoreply status` reports `running=False`.
- Check `python -m xianyu_system upstream listener status` before and after the test matrix.
- Check Docker service names and process names for unknown autoreply/websocket/scheduler senders.
- Confirm the approved native upstream sender is the only sender before each scenario.
- Stop immediately if any local worker, wrapper-owned sender, or unknown sender appears.
- Two automatic-reply send executors must never run at the same time.
- Unknown executor state must fail closed.

## Risk stop conditions

Any later live validation must fail closed immediately on:

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
- Sensitive information exposure.
- Unable to determine whether a message was sent.
- Unable to determine whether the stop command took effect.
- Unable to confirm native autoreply is stopped.
- Unable to confirm native WebSocket is stopped.
- Unable to confirm the local CHG-0010 worker remains stopped.
- Message count reaches or may have exceeded the approved cap.

Unknown state = stop, not retry.

Operators must not use repeated starts, repeated stops, relogin, automatic retries, or continued sends to determine state.

## Stop and rollback plan

Normal stop sequence for any later approved live validation:

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

Project-owner approval must define the observable stop criteria before validation starts. The criteria must cover at least:

Native autoreply stopped:

- Approved process/service/container status shows stopped or disabled.
- No active autoreply worker is present.
- No approved rule execution can begin.

Native WebSocket stopped:

- Approved connection/process status shows disconnected or stopped.
- No reconnect loop is active.
- No scheduler or restart policy will reconnect it.

No further message can send:

- No active sender executor.
- No queued approved test message remains.
- Approved quiet period completes with no new outbound message.
- No automatic restart or reconnect occurs.

CHG-0010 worker stopped:

- Repository status command reports `running=False`.
- No matching worker process exists.

Stop failure handling:

If a stop command fails, returns an unknown result, times out, or cannot be independently verified:

- Enter `STOP_STATE_UNKNOWN`.
- Do not issue another test message.
- Do not start another executor.
- Do not retry platform actions automatically.
- Preserve masked diagnostics.
- Escalate to the project owner.
- Treat the validation as failed.

Before validation starts and before each scenario, the operator must check for reactivation risk from:

- Docker restart policy.
- Compose restart policy.
- Scheduler.
- Supervisor.
- Windows scheduled task.
- Background launcher.
- Autoreconnect loop.
- Service dependency.

If any mechanism can reactivate a sender or WebSocket, validation must not start or must terminate immediately. This Change must not create a new supervisor, monitor, or second control system.

Rollback plan:

- Stop upstream native autoreply.
- Stop upstream native WebSocket.
- Confirm local CHG-0010 worker remains stopped.
- Disable or remove only rules created for this validation.
- Restore the approved pre-test configuration state.
- Preserve masked evidence.
- Generate a masked failure report.
- Do not delete production data.
- Do not clean unknown data.
- Do not modify upstream source code.
- Do not enable a local substitute executor.
- Do not automatically continue testing.

## Upstream capability audit

Pinned upstream was audited at `D:/xianyu-upstream-pilot` for the native fixed-template autoreply surfaces listed above. The audit confirms capability presence for planning and configuration, not live multi-account success.

## Pinned upstream evidence

- Upstream path: `D:/xianyu-upstream-pilot`
- Expected SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Actual SHA at DRAFT creation: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Branch state: detached HEAD.
- Tracked upstream source modified by this change: no.

## Existing local implementation search

Local search found CHG-0009 wrapper diagnostics and CHG-0010 local autoreply worker code. `docs/LOCAL_COMPONENT_DISPOSITION.md` freezes/deprecates local autoreply overlap and keeps wrapper commands operations-only.

## Reuse decision

Decision: CONFIGURE_UPSTREAM

## Duplicate implementation risk

The main risk is accidentally restoring CHG-0010 or adding a second local matcher, sender, scheduler, account database, UI, API adapter, Cookie vault, WebSocket parser, default reply executor, product reply executor, image executor, AIReplyEngine, production audit implementation, or dedup implementation. This design forbids those paths and requires upstream native validation first.

## Why upstream cannot satisfy the requirement

Not applicable. Current evidence points to upstream native capability presence. Configuration and validation are the required next step.

## Approved exception ADR

Not applicable. No local build exception is requested.

## Component owner

Upstream owns business execution. `D:/xianyu` owns validation governance and operational safety gates.

## Retirement plan for overlapping local code

CHG-0010 local worker remains frozen/deprecated. CHG-0015 will evaluate retirement after upstream native fixed-template and AI reply validation.

## Closeout design finding

CHG-0012 is closed as archived documentation and evidence only. It does not authorize production automatic reply.

The blocked root cause is:

`PLATFORM_MANUAL_VERIFICATION_CAPABILITY_GAP`

Closeout evidence summary:

1. `MESSAGE_SERVICE_RESTART_DID_NOT_RECOVER`: the system restart path did not produce stable connected account state for live validation.
2. `WEBSOCKET_RUNNING_ACCOUNTS_DISCONNECTED`: websocket container startup and health were possible, but account connection state stayed blocked before real reply validation.
3. `TOKEN PATH DIAGNOSTIC`: online chat and automatic reply use separate token caches and the failure was in token acquisition, not a local CHG-0010 sender path.
4. `NATIVE TOKEN STAGE REPORT`: both target accounts could create upstream tasks but token refresh encountered platform verification before websocket connection could be validated.
5. `ONLINE CHAT AND TOKEN VERIFICATION REPORT`: ACCOUNT-A online-chat Token API returned `FAIL_SYS_USER_VALIDATE`; login remained valid and relogin was not evidenced.
6. `MANUAL VERIFICATION CAPABILITY AUDIT`: pinned upstream, latest upstream, and local history contain automated slider paths but no pure manual local handoff suitable for the approved safety constraints.

Configuration correction record:

- WebSocket control URL mismatch was confirmed.
- The local pilot `.pilot` compose configuration was corrected.
- The original pilot configuration backup is outside the repository.
- `.pilot` files remain untracked and are not part of this closeout.
- No secret values are recorded in repository evidence.

Rollback and stop state:

- Upstream websocket remains stopped.
- Formal test rules do not exist.
- CHG-0010 local worker remains stopped.
- No further CHG-0012 live validation may run until an independent manual verification handoff Change is completed.

Design conclusion:

The upstream native fixed-template reply design remains the intended executor path. The missing piece is not a second sender, matcher, token client, or websocket. The missing piece is an owner-controlled, local-only manual platform verification handoff that can safely return to upstream native token refresh after official verification succeeds.
