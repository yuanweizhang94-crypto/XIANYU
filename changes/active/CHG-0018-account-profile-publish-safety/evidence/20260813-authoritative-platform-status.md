# CHG-0018 authoritative platform status closure evidence

Date: 2026-08-13
Patch base SHA: 64c245bc85ac56e34339fa056b0e291a16a3843b
Root baseline commit: 9104b95742e1ba23a61714ceb0c0feb005beb929
Upstream current SHA: c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72
Upstream capability: no native authoritative item delist reason or account publish restriction closure found in relevant upstream item/publish/account paths or matching GitHub issues.
Reuse decision: PATCH_UPSTREAM
Duplicate-development risk: low; reused existing ItemInfoManager -> ItemService -> Publisher preflight -> UI paths, no new scheduler, service, DB table, browser profile, or second publisher.
Rollback: revert vendor patch 64c245-chg0018-authoritative-platform-status.patch and redeploy previous images.

Execution contract:
User outcome: confirm item missing reasons and account publish restriction from official read-only evidence when possible.
Confirmed blocker: previous state stopped at NOT_IN_ACTIVE_LIST / RESTRICTION_SUSPECTED and did not store official publish restriction evidence.
Smallest success test: missing items receive bounded official detail probe without inference, account publish page preflight records PUBLISH_RESTRICTED only on official text, publisher fail-closes on effective authoritative restriction.

Implementation summary:
- Added bounded authoritative item detail probe inside existing ItemService; UNKNOWN/session/verification/network preserves previous state.
- Extended item statuses: ACTIVE, NOT_IN_ACTIVE_LIST, OFFLINE, SOLD, DELETED, UNDER_REVIEW, PLATFORM_DELISTED, UNKNOWN.
- Added publish restriction parser and read-only publish page preflight using existing Publisher path.
- Added Publisher pre-submit fail-closed guard for authoritative PUBLISH_RESTRICTED metadata.
- Added manual item page check-platform-status button for selected account only.
- No schema, new scheduler, second item monitor, second Publisher, second Browser Profile, appeal/relist/offline/publish/message actions.

Production sample result:
- Before item counts: UNSET=13, ACTIVE=10, NOT_IN_ACTIVE_LIST=7.
- Before account restriction: UNSET=10, RESTRICTION_SUSPECTED=1.
- Checked account_id=2221384086829, PROBE_MODE=READ_ONLY.
- Official active-list source mtop.idle.web.xyh.item.list returned total active count 0.
- 7 NOT_IN_ACTIVE_LIST items were probed through goofish_item_detail_page.
- Official item detail results: all 7 returned session_or_verification_required, final status preserved as NOT_IN_ACTIVE_LIST.
- Official publish page result: PUBLISH_RESTRICTED, reason text included official page phrase: ni yi bei xian zhi fa bu.
- Restriction until: null; no explicit until or duration found.
- After account restriction: PUBLISH_RESTRICTED=1, RESTRICTION_SUSPECTED=0.
- ACTIVE_RESTRICTION_SAMPLE_FOUND=true.

Sample item results:
- 1070448639794: LOCAL_PREVIOUS_STATE=NOT_IN_ACTIVE_LIST, OFFICIAL_RESULT=UNKNOWN, FINAL_PLATFORM_STATUS=NOT_IN_ACTIVE_LIST, REASON=session_or_verification_required, SOURCE=goofish_item_detail_page.
- 1070639622734: LOCAL_PREVIOUS_STATE=NOT_IN_ACTIVE_LIST, OFFICIAL_RESULT=UNKNOWN, FINAL_PLATFORM_STATUS=NOT_IN_ACTIVE_LIST, REASON=session_or_verification_required, SOURCE=goofish_item_detail_page.
- 1071350062753: LOCAL_PREVIOUS_STATE=NOT_IN_ACTIVE_LIST, OFFICIAL_RESULT=UNKNOWN, FINAL_PLATFORM_STATUS=NOT_IN_ACTIVE_LIST, REASON=session_or_verification_required, SOURCE=goofish_item_detail_page.
- 1072067658489: LOCAL_PREVIOUS_STATE=NOT_IN_ACTIVE_LIST, OFFICIAL_RESULT=UNKNOWN, FINAL_PLATFORM_STATUS=NOT_IN_ACTIVE_LIST, REASON=session_or_verification_required, SOURCE=goofish_item_detail_page.
- 1072119047871: LOCAL_PREVIOUS_STATE=NOT_IN_ACTIVE_LIST, OFFICIAL_RESULT=UNKNOWN, FINAL_PLATFORM_STATUS=NOT_IN_ACTIVE_LIST, REASON=session_or_verification_required, SOURCE=goofish_item_detail_page.
- 1072373573568: LOCAL_PREVIOUS_STATE=NOT_IN_ACTIVE_LIST, OFFICIAL_RESULT=UNKNOWN, FINAL_PLATFORM_STATUS=NOT_IN_ACTIVE_LIST, REASON=session_or_verification_required, SOURCE=goofish_item_detail_page.
- 1072777253309: LOCAL_PREVIOUS_STATE=NOT_IN_ACTIVE_LIST, OFFICIAL_RESULT=UNKNOWN, FINAL_PLATFORM_STATUS=NOT_IN_ACTIVE_LIST, REASON=session_or_verification_required, SOURCE=goofish_item_detail_page.

Sample account result:
- 2221384086829: PREVIOUS_STATE=RESTRICTION_SUSPECTED, OFFICIAL_RESTRICTION_RESULT=PUBLISH_RESTRICTED, FINAL_RESTRICTION_STATE=PUBLISH_RESTRICTED, REASON=official page text says publish is restricted, RESTRICTION_UNTIL=null, SOURCE=publish_preflight_page, EVIDENCE_TYPE=EXPLICIT_RESTRICTION_TEXT.

Safety and side effects:
- REAL_PRODUCTS_PUBLISHED=0
- PRODUCTS_RELISTED=0
- PRODUCTS_OFFLINED=0
- MESSAGES_SENT=0
- APPEALS_SUBMITTED=0
- FORCED_QR_OR_COOKIE_REFRESH=0
- Recent xy_publish_logs count=0
- Recent xy_auto_reply_message_logs count=0

Deploy and health:
- Deployed services: backend-web, scheduler, frontend.
- WebSocket not touched.
- Scheduler instances before=1, after=1, max_observed=1.
- Backend /docs HTTP 200.
- Frontend / HTTP 200.
- WebSocket /docs HTTP 200.

Validation:
- python -m pytest tests/test_chg0018_authoritative_platform_status.py tests/test_chg0018_password_item_platform_status.py tests/test_chg0018_consumer_readiness.py: 22 passed.
- python -m py_compile targeted backend/common modules: PASS.
- npm run build: PASS.
- git diff --check targeted files: PASS.
- python scripts/verify_repository.py: repository verification passed, 595 passed, 1 warning.
- PATCH_CLEAN_APPLY=PASS on detached base worktree 64c245bc85ac56e34339fa056b0e291a16a3843b.
- PATCH_BYTE_EQUIVALENCE=CRLF_DIFF_ONLY; no-index spot checks with --ignore-cr-at-eol showed no content differences, byte hashes differ because this Windows checkout has core.autocrlf=true.

Patch:
- vendor/patches/xianyu-auto-reply/64c245-chg0018-authoritative-platform-status.patch
- SHA256=F99F2E8AE83FF75B12EF0C2140D93AA4F8D17E35B7AA3E259D6BA939DD03C8E3
