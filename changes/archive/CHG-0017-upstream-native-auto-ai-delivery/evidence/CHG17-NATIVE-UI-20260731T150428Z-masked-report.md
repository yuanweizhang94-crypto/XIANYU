Run ID: CHG17-NATIVE-UI-20260731T150428Z

# CHG-0017 Native UI Delivery Evidence

## Scope

This run aligned the upstream-native management UI with the already-running
CHG-0017 candidate runtime. It did not create a new Change, branch, PR,
frontend, backend, IM client, Token client, WebSocket runtime, sender, AI
provider, or automatic reply worker.

No Cookie, Token, API key, Device ID, UNB, full account ID, full chat/session
ID, customer message content, platform URL, or raw traceback is recorded here.

## Topology

- frontend_url: `http://127.0.0.1:19000`
- frontend_container_before: old Pilot frontend on `xianyu_pilot_network`
- frontend_container_after: CHG-0017 candidate frontend on `xianyu_chg0017_network`
- frontend_api_base: same-origin `/api`, proxied by nginx to `backend-web:8089`
- frontend_ws_base: same-origin `ws://127.0.0.1:19000/api/v1/chat-new/ws/<account>`
- candidate_backend: `http://127.0.0.1:28089`, container `xianyu_chg0017_backend_web`
- candidate_websocket: internal `http://xianyu_chg0017_websocket:8090`
- candidate_mysql: `127.0.0.1:23306`, container `xianyu_chg0017_mysql`
- candidate_redis: `127.0.0.1:26379`, container `xianyu_chg0017_redis`
- frontend_database_same: true
- frontend_redis_same: true
- frontend_candidate_same: true

## Root Cause

The owner-facing URL `http://127.0.0.1:19000` was served by the old Pilot
frontend. That frontend used the upstream nginx same-origin proxy, but because
it was attached to `xianyu_pilot_network`, `backend-web:8089` resolved to the
Pilot backend rather than the CHG-0017 candidate backend.

This made the UI display Pilot state while the production automatic reply path
was running in the candidate containers.

## Configuration Correction

- Stopped only the conflicting old Pilot frontend that owned port `19000`.
- Started the existing upstream-built candidate frontend image on
  `127.0.0.1:19000`.
- Attached the candidate frontend to `xianyu_chg0017_network`.
- Kept the candidate backend, MySQL, Redis, and WebSocket as the single runtime
  used by CHG-0017.
- Set candidate containers to Docker `unless-stopped` restart policy.
- Added a local-only healthcheck override for the frontend because the image
  healthcheck used `localhost` and hit IPv6 `::1`; `127.0.0.1/health` succeeds.
- The local runtime compose file is under `.local/` and is gitignored.

## Upstream Native Meanings

- Account record enabled/disabled: account `status` in `xy_accounts`; changing
  it through `/api/v1/cookies/{account_id}/status` starts or stops the upstream
  WebSocket account task through `websocket_client`.
- Account online status: backend account listing resolves realtime connected
  account IDs from the upstream WebSocket service.
- Online-chat connect: `/api/v1/chat-new/connect/{account_id}` creates an
  independent upstream native IM session in backend `chat_new` session manager.
- Online-chat WebSocket: browser push channel is same-origin
  `/api/v1/chat-new/ws/{account_id}` through the candidate frontend proxy.
- AI switch and AI settings: upstream native `/api/v1/ai-reply-settings`
  routes and the account management AI settings modal.
- Message logs: upstream native `/message-logs` page backed by
  `xy_auto_reply_message_logs`.
- Keyword rules: upstream native `/keywords` page backed by `xy_keyword_rules`.

## UI Validation

- frontend_status: healthy
- backend_service_status_in_ui: online
- message_service_status_in_ui: online
- scheduler_status_in_ui: offline; not part of the CHG-0017 production auto
  reply chain validated by this Change
- account_record_enabled: true for ACCOUNT-A
- account_online_status: online for ACCOUNT-A
- websocket_connection_stats: one native connected account task
- online_chat_connection: connected for ACCOUNT-A
- online_chat_sessions: available after selecting ACCOUNT-A
- im_connect_error: resolved
- ai_switch_control: verified
- ai_enabled: true for ACCOUNT-A
- ai_settings_modal: verified
- provider_type: `gemini`
- base_url: `https://generativelanguage.googleapis.com`
- model_name: `gemini-3.6-flash`
- model_name_has_models_prefix: false
- api_key_control: present, value redacted
- prompt_control: present, value redacted
- keyword_control: verified
- reply_log_control: verified
- account_task_control: verified by upstream route/source; not clicked during
  this UI correction because ACCOUNT-A is already production running
- duplicate_executor_count: 0

## Safety Counts

- active keyword rules for ACCOUNT-A: 0
- enabled default replies for ACCOUNT-A: 0
- enabled message filters: not enabled in this UI correction
- processing autoreply rows for ACCOUNT-A: 0
- 60 second post-UI observation: no delta in autoreply total, successful send
  count, AI message total, AI assistant message count, or processing rows
- successful non-whitelist sends observed by this run: 0
- proactive customer sends by this run: 0
- sender implementation added: no
- runtime source modified: no
- upstream business code modified: no
- PR merged: no

## PR State

- pr_number: 26
- pr_state: Draft / Open / Unmerged
- pr_exact_head_before_this_evidence: `fa23eee4dbdb99c7a60e1d4aad957c1475357c1f`
- pull_request CI at that head: quality success, tests success, security success

## Verdict

`UI_NATIVE_DELIVERY_READY`
