# Upstream Capability Matrix

Change: CHG-0011-upstream-first-product-direction-freeze
Pinned upstream path: `D:/xianyu-upstream-pilot`
Pinned upstream SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
Audit type: static source audit plus prior supervised Pilot evidence. No platform messages were sent for this change.

## Status labels

- `PINNED_AND_VERIFIED`: present in pinned upstream and previously verified in the local Pilot environment.
- `PINNED_PRESENT_NOT_LIVE_VERIFIED`: present in pinned upstream source but not live-verified for the full product scenario.
- `UPSTREAM_NEWER_ONLY`: not claimed for the pinned SHA; may require later upgrade assessment.
- `NOT_PRESENT`: not found in pinned upstream during this audit.

## Decision labels

`ADOPT_UPSTREAM`, `CONFIGURE_UPSTREAM`, `PATCH_UPSTREAM`, `WRAP_FOR_OPERATIONS`, `BUILD_LOCAL_EXCEPTION`, `RETIRE_LOCAL_OVERLAP`, `UNVERIFIED`, `OUT_OF_SCOPE`.

## Mandatory matrix maintenance and validation rule

This matrix is a baseline inventory, not a substitute for fresh upstream research.

Before development, repair, or validation of any row:

1. Read the original upstream feature description and intended user workflow first. Use README/docs, UI text, API descriptions, release notes, issues, and commits where available.
2. Re-check the pinned upstream SHA and record exact UI, route, service, model, worker, scheduler, test, configuration, and log evidence relevant to the task.
3. Confirm whether the deployed pinned SHA contains the described behavior. Newer upstream behavior must be marked separately and must not be represented as deployed.
4. Use the upstream-native workflow for the first implementation and validation plan.
5. Consult prior `D:/xianyu` implementations, archived Changes, ADRs, experiments, tests, and research only when upstream has no corresponding capability or does not address the observed problem.
6. Update this matrix when evidence, upstream SHA, ownership, reuse decision, validation status, or forbidden duplicate implementation changes.

Every active Change that references this matrix must also record upstream feature-description evidence, the pinned code path, the native workflow, expected status/log evidence, the reuse decision, and duplicate-development risk. A row marked present does not authorize a parallel local implementation. A row marked not present is invalid unless the searched documentation and source areas are recorded.

## Matrix

| Capability | Product requirement | Pinned upstream evidence | Upstream UI/API | Upstream execution service | Current live verification | Existing `D:/xianyu` overlap | Decision | Capability owner | Next validation | Forbidden duplicate implementation |
|---|---|---|---|---|---|---|---|---|---|---|
| Multi-account add | Add multiple Xianyu accounts | `common/models/xy_account.py`, `backend-web/app/api/routes/cookies.py`, `frontend/src/pages/accounts/Accounts.tsx` | Accounts page and account APIs | backend account services | PINNED_PRESENT_NOT_LIVE_VERIFIED | Local Account boundary is synthetic only | ADOPT_UPSTREAM | upstream | CHG-0012 add second dedicated test account through native UI | local account-login implementation |
| Multi-account login | Independent account login | `websocket/app/api/routes/password_login.py`, QR/password routes, account status fields | Login dialogs and account status APIs | upstream websocket/login services | Single dedicated account only; multi-account not verified | Wrapper account status only | ADOPT_UPSTREAM | upstream | CHG-0012 two-account login validation | local login/browser/Cookie flow |
| Account status | Per-account active/disabled/connected state | `XYAccount.status`, `frontend/src/pages/accounts/Accounts.tsx`, internal account status route | Accounts page, internal status route | `connection_manager`, `ImSessionManager` | PINNED_AND_VERIFIED for one account connected/stopped states | Wrapper status query | ADOPT_UPSTREAM | upstream | CHG-0012 account isolation status | local authoritative account status table |
| Cookie maintenance and renewal | Store and renew account session material | `XYAccount.cookie`, `cookie_refresh` routes/services, login renewal logs | Cookie/renewal APIs and admin logs | upstream cookie refresh services | PINNED_PRESENT_NOT_LIVE_VERIFIED | Wrapper never stores secrets | ADOPT_UPSTREAM | upstream | CHG-0012 login/renewal observation without secret output | local Cookie vault/Profile copying |
| Account enable/disable | Stop or pause account automation | `XYAccount.status`, disable reason, pause duration fields, Accounts page toggles | Accounts page status update APIs | upstream account services and websocket manager | PINNED_PRESENT_NOT_LIVE_VERIFIED | Local worker has allowlist and disabled config | ADOPT_UPSTREAM | upstream | CHG-0012 pause/enable validation | local second enable/disable authority |
| WebSocket connection | Connect to Xianyu IM | `websocket/app/services/xianyu/connection_manager.py`, `xianyu_async.py`, `backend-web/app/services/chat_new/im_session_manager.py` | Online chat route/status APIs | upstream websocket service | PINNED_AND_VERIFIED for one account connection | CHG-0009 listener wrapper | ADOPT_UPSTREAM | upstream | CHG-0012 native sender/listener ownership check | local protocol implementation |
| Message receiving | Receive and parse inbound messages | `push_message_parser.py`, `message_handler.py`, `chat_new` routes | Online chat page | upstream websocket service | PINNED_AND_VERIFIED for one account | CHG-0009 normalized inbound observation | ADOPT_UPSTREAM | upstream | CHG-0012 per-account receive validation | local parser/protocol clone |
| Online chat | Operator-visible conversations | `frontend/src/pages/chat-new/ChatNew.tsx`, `useChatNewWs.ts`, `chat_new.py` | Online chat UI and APIs | backend + websocket push | PINNED_AND_VERIFIED for displayed chats | Wrapper CLI diagnostics | ADOPT_UPSTREAM | upstream | CHG-0012 no local chat UI | local chat UI |
| Text keyword reply | Fixed-template text reply | `XYKeywordRule.reply_type`, `keyword_service.py`, `auto_reply_service.py` keyword branch | Keywords page and keyword APIs | upstream `auto_reply_service.py` | PINNED_PRESENT_NOT_LIVE_VERIFIED | CHG-0010 YAML rules/matcher | ADOPT_UPSTREAM | upstream | CHG-0012 native keyword reply validation | YAML keyword engine |
| Image keyword reply | Keyword sends image reply | `XYKeywordRule.image_url`, `_handle_image_keyword` | Keywords page image upload/API | upstream auto reply service | PINNED_PRESENT_NOT_LIVE_VERIFIED | none beyond local text-only worker | ADOPT_UPSTREAM | upstream | CHG-0012 image keyword smoke only if owner approves | local image keyword executor |
| Default reply | Account default reply | `DefaultReply`, `DefaultReplyService`, `get_default_reply` | Accounts default reply modal/API | upstream auto reply service | PINNED_PRESENT_NOT_LIVE_VERIFIED | CHG-0010 fallback setting | ADOPT_UPSTREAM | upstream | CHG-0012 default reply validation | local fallback executor |
| Reply once | Avoid repeated default reply | `DefaultReplyRecord`, `reply_once` checks and locks | Default reply modal/API | upstream auto reply service | PINNED_PRESENT_NOT_LIVE_VERIFIED | CHG-0010 idempotency/cooldown | ADOPT_UPSTREAM | upstream | CHG-0012 reply_once validation | local duplicate once table |
| Product-specific reply | Item-bound keyword/default reply | `XYKeywordRule.item_id`, `DefaultReply.item_id`, catalog joins | Keywords page item binding and default reply item APIs | upstream auto reply service | PINNED_PRESENT_NOT_LIVE_VERIFIED | local Reply boundary synthetic product facts | ADOPT_UPSTREAM | upstream | CHG-0012 product-specific native validation | local product-specific reply engine |
| Variable replacement | Reply variables in text | formatting branches in `auto_reply_service.py` around reply parsing and segments | Keyword/default reply UI | upstream auto reply service | PINNED_PRESENT_NOT_LIVE_VERIFIED | local renderer synthetic variables | ADOPT_UPSTREAM | upstream | CHG-0012 exact supported variables inventory | local variable renderer for production sends |
| Message filtering | Skip reply/notification filters | `message_filters.py`, `get_filter_keywords`, `should_skip_reply` | Message filter pages/APIs | upstream auto reply service | PINNED_PRESENT_NOT_LIVE_VERIFIED | local safety gates | ADOPT_UPSTREAM | upstream | CHG-0012 filter validation | local production skip-list engine |
| Duplicate message protection | Avoid duplicate handling | AI recent-message checks, default reply locks, duplicate decisions/log fields | Logs and service internals | upstream auto reply service | PINNED_PRESENT_NOT_LIVE_VERIFIED | CHG-0010 idempotency | ADOPT_UPSTREAM | upstream | CHG-0012 duplicate observation | parallel idempotency executor |
| Pause automatic reply | Manual pause/human intervention | `pause_duration`, `manual intervention pause` checks in AI/auto reply services | Accounts page pause controls | upstream services | PINNED_PRESENT_NOT_LIVE_VERIFIED | local disabled config only | ADOPT_UPSTREAM | upstream | CHG-0012 pause validation | local pause scheduler |
| Reply delay | Delay before sending reply | `XYAccount.reply_delay_seconds`, `_load_reply_delay` | Accounts page reply delay controls | upstream auto reply service | PINNED_PRESENT_NOT_LIVE_VERIFIED | CHG-0010 cooldown/rate limit | ADOPT_UPSTREAM | upstream | CHG-0012 delay validation | local delay executor |
| Auto reply logs | Auditable reply decisions | `XYAutoReplyMessageLog`, `auto_reply_logs.py`, `AutoReplyLogService` | Auto reply logs page/API | upstream log service | PINNED_PRESENT_NOT_LIVE_VERIFIED | CHG-0010 local audit | ADOPT_UPSTREAM | upstream | CHG-0012 log verification | separate production reply log authority |
| AI provider configuration | Per-account model/provider settings | `AIReplySettings`, `AIReplySettingsService`, Accounts AI modal | Accounts AI settings/API | upstream AI reply engine | PINNED_PRESENT_NOT_LIVE_VERIFIED | no local AI provider runtime | ADOPT_UPSTREAM | upstream | CHG-0013 native AI settings validation | local AI provider settings UI |
| OpenAI-compatible API | OpenAI-compatible model calls | `openai_compatible`, `AsyncOpenAI`, default DashScope compatible base URL | AI settings API/UI | upstream AI reply engine | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | ADOPT_UPSTREAM | upstream | CHG-0013 OpenAI-compatible endpoint validation | local OpenAI client engine |
| DashScope | DashScope compatible/app support | `dashscope_app`, DashScope default URLs | AI settings provider selection | upstream AI provider service | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | ADOPT_UPSTREAM | upstream | CHG-0013 provider validation | local DashScope adapter |
| Gemini | Gemini provider support | `gemini`, Gemini base URL builder | AI settings provider selection | upstream AI provider service | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | ADOPT_UPSTREAM | upstream | CHG-0013 provider validation | local Gemini adapter |
| Prompts | Per-account custom prompts | `custom_prompts`, `default_prompts`, AI settings modal | AI settings UI/API | upstream AI reply engine | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | ADOPT_UPSTREAM | upstream | CHG-0013 prompt isolation validation | local prompt engine |
| Conversation context | AI conversation history | `AIChatMessage`, `AIConversationService`, `get_context` | AI settings/logs | upstream AI reply engine | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | ADOPT_UPSTREAM | upstream | CHG-0013 context validation | local context DB |
| Intent recognition | Classify price/tech/default | `AIReplyEngine.detect_intent` | AI setting controls | upstream AI reply engine | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | ADOPT_UPSTREAM | upstream | CHG-0013 priority and intent validation | local intent classifier |
| Bargain control | Limit bargain rounds/discounts | `max_discount_percent`, `max_discount_amount`, `max_bargain_rounds`, bargain count | AI settings UI/API | upstream AI reply engine | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | ADOPT_UPSTREAM | upstream | CHG-0013 bargain validation | local bargain engine |
| Per-account AI settings | Isolate AI settings by account | settings stored in `XYAccount.metadata_json` and listed per owner/account | Accounts AI modal/API | upstream AI services | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | ADOPT_UPSTREAM | upstream | CHG-0013 account isolation validation | local second AI settings UI |
| Product info in AI context | Include item facts in prompt | AI reply engine product context assembly | AI engine/service internals | upstream AI reply engine | PINNED_PRESENT_NOT_LIVE_VERIFIED | local synthetic Reply/Publish facts only | ADOPT_UPSTREAM | upstream | CHG-0013 item context validation | local product-context prompt builder |
| Risk/verification failure handling | Stop on risk/verification | password login status `verification_required`, face verification routes, risk logs | Login/risk pages/APIs | upstream login/risk services | PINNED_AND_VERIFIED for face verification prompt handling in Pilot | local governance stop rules | WRAP_FOR_OPERATIONS | shared: upstream signal, local stop policy | CHG-0012 risk stop drill | bypass or auto-solve risk controls |
| Health checks | Service health and status | websocket health, backend health, wrapper health | health/status APIs | upstream plus wrapper checks | PINNED_AND_VERIFIED for P0/P1/P2 | Wrapper health commands | WRAP_FOR_OPERATIONS | `D:/xianyu` control layer | CHG-0012 operations checklist | duplicate business health source |
| Backup/restore | Operational recovery | upstream DB and volumes exist; no full validated process in pinned evidence | limited admin/data tools | not fully validated | PINNED_PRESENT_NOT_LIVE_VERIFIED | none | WRAP_FOR_OPERATIONS | `D:/xianyu` control layer | CHG-0014 backup/restore validation | hidden backup scripts without audit |
| Version upgrade | Pinned upgrade governance | git SHA pin plus Docker/Pilot files | no product UI | not an app feature | PINNED_AND_VERIFIED for pin evidence only | CHG-0008 pin governance | WRAP_FOR_OPERATIONS | `D:/xianyu` control layer | CHG-0014 upgrade runbook | floating upstream main |
| Log redaction | No secret output | upstream logs may include identifiers; local wrappers redact secrets | logs pages/services | mixed | PINNED_PRESENT_NOT_LIVE_VERIFIED | `security_scan.py`, wrapper redaction | WRAP_FOR_OPERATIONS | `D:/xianyu` control layer | CHG-0014 redaction audit | logging secret values |
| Runtime monitoring | State summary and alerts | upstream health/log endpoints plus wrapper status | health/status pages/APIs | services expose status/logs | PINNED_AND_VERIFIED for local Pilot service status | wrapper status commands | WRAP_FOR_OPERATIONS | `D:/xianyu` control layer | CHG-0014 monitoring validation | parallel business executor |

## Locked ownership summary

The formal automatic-reply sender must be the upstream native executor after CHG-0012/CHG-0013 validation. The CHG-0010 local worker is not the formal executor and must remain stopped unless a later approved diagnostic-only procedure explicitly starts it without upstream native sending.
