# CHG-0023 runtime acceptance and formal persistence — 2026-08-23

Status: VERIFYING

Change ID: `CHG-0023-websocket-auto-reply-readiness-contract-restoration`

## Authority separation

This evidence closes the formal source-persistence record after production acceptance. It does not redeploy production and it does not require one synthetic full-project linear upstream baseline.

```text
RUNTIME_ACCEPTANCE=PASS
CHG0022_PRODUCTION_DELTA_PROVENANCE=PASS
BACKEND_PREIMAGE_CORRECTION=PASS
LINEAR_PATCH_STACK_REQUIRED=false
PER_FILE_PREIMAGE_PROVENANCE=true
CHG0023_VENDOR_PATCH_ROLE=PER_FILE_PROVEN_PRODUCTION_OWNER_DELTA_AUTHORITY
UPSTREAM_AUDIT_AUTHORITY=9cbb3725b7e91daec33cb824a3ff4bd84acdcb12
FULL_FILE_UPSTREAM_EQUIVALENCE_NOT_REQUIRED=true
PRODUCTION_OWNER_DELTA_EXACTNESS_REQUIRED=true
CUMULATIVE_SCOPE_EXPANSION=false
UNEXPLAINED_NON_CHG0023_DELTA=false
```

The upstream audit pin remains the upstream capability authority. The two CHG-0023 owner preimages are separate exact immutable runtime-file authorities.

## Corrected Backend owner provenance

The previously selected Backend file from `xianyu-chg0018-backend-web:chat-upstream-golden-path-cleanup-20260815-r2` was only the image running immediately before CHG-0023 deployment. It was not the candidate-build owner preimage.

```text
PREVIOUS_BACKEND_PREIMAGE_SHA256=93a8172eecd4e2311acfe0bd30732a541be9eb899fa35042ddd499ef7b687e97
PREVIOUS_BACKEND_PREIMAGE_CLASSIFICATION=WRONG_PREDEPLOY_RUNTIME_BASELINE
PREVIOUS_SCOPE_CONTAMINATION=BASELINE_SELECTION_ERROR
```

The accepted Backend candidate was built on the already-validated auth-cookie closure image. Immutable RootFS ancestry proves that the candidate's first 83 layers are exactly the 83 layers of `xianyu-chg0018-backend-web:auth-cookie-closure-20260819-r2`; the candidate adds only the two CHG-0023 overlay layers that copy and execute `apply_chg0023.py backend`.

```text
CHG0023_BACKEND_OWNER_PREIMAGE_AUTHORITY=xianyu-chg0018-backend-web:auth-cookie-closure-20260819-r2
CHG0023_BACKEND_OWNER_PREIMAGE_IMAGE_ID=sha256:60f6ce94a1db296c3909ceff71629d1fab86150c790e7966a7dadb9288df2fe9
BACKEND_PREIMAGE_SHA256=3c3dab0b0a4a3a7cdcfe696413b47def32aa92722c89632294d9e3d361ef2ab1
BACKEND_PREIMAGE_GIT_BLOB=a4ed1c0ec5d2a5bad29ba69aefbad71d46d089c0
BACKEND_POSTIMAGE_SHA256=ac341a5801f3ed521335fcaac3ed05e3f5179d33ce739ee8fc0788f3f2bd9dee
```

The corrected Backend preimage to accepted postimage diff is one hunk entirely inside `_build_business_capabilities()`. It only moves authoritative platform-verification, HUMAN_QR/no-credentials, and expired-Session blockers before `connected + token_ready -> ONLINE`.

```text
BACKEND_SCOPE_VALID=true
CHAT_CHANGES_PRESENT=false
SESSION_COOKIE_WRITER_CHANGES_PRESENT=false
NON_CHG0023_BACKEND_HUNKS=0
```

## WebSocket owner provenance

```text
CHG0023_WEBSOCKET_OWNER_PREIMAGE_AUTHORITY=xianyu-chg0022-websocket:token-network-classification-20260821-r1
WEBSOCKET_PREIMAGE_SHA256=4175661b8e464c30e3c1d24af561a823329bec557b42a74601a0073529b3484a
WEBSOCKET_PREIMAGE_GIT_BLOB=13223958a1439bbafa6d7e1bc834f69e4580f304
WEBSOCKET_POSTIMAGE_SHA256=b8681987c0aa04f596b5aaaf6a832941e11a576f547987bb3e8c8423eb5c8e5a
WEBSOCKET_SCOPE_VALID=true
```

The WebSocket delta stays in existing `CookieManager.get_task_status()` only: `token_ready=false` by default and `token_ready=bool(getattr(instance, "current_token", None))` for a live instance. The existing internal status route remains pass-through.

CHG-0022 `xianyu_async.py` is not a CHG-0023 owner and remains exact:

```text
CHG0022_XIANYU_ASYNC_AUTHORITY=PROVEN_PRODUCTION_POSTIMAGE
CHG0022_XIANYU_ASYNC_SHA256=9e085fac9e4d5030a9b0ddc329e50434e23ea243dffdf3cc1161696ffd6a4fd5
CHG0022_XIANYU_ASYNC_PRESERVED=true
```

## Final vendor patch

Artifact:

`vendor/patches/xianyu-auto-reply/chg0023-readiness-owner-deltas.patch`

Generated in a disposable Git baseline with `core.autocrlf=false` from only the two exact preimages, then replacing only those two files with accepted postimages. The disposable builder marks only those two target paths `-diff` in local `.git/info/attributes` and runs `git diff --binary --full-index HEAD`, producing two Git binary patch records that preserve the exact Git blobs independent of checkout line endings. No repository attributes are changed; no hunk was hand-edited or manually spliced.

```text
CHG0023_VENDOR_PATCH_SHA256=e6808621fd86ade619dff2be622f9c419feca7436542ca004854210f266adc24
GIT_BINARY_PATCH_COUNT=2
PATCH_RUNTIME_FILE_COUNT=2
PATCH_RUNTIME_FILES=backend-web/app/api/routes/cookies.py;websocket/app/services/xianyu/cookie_manager.py
XIANYU_ASYNC_IN_PATCH=false
INTERNAL_STATUS_ROUTE_IN_PATCH=false
SESSION_COOKIE_CLOSURE_FILES_IN_PATCH=false
CHAT_FILES_IN_PATCH=false
```

Exact replay against a second clean two-owner preimage baseline:

```text
PATCH_APPLY_CHECK=PASS
PATCH_CLEAN_APPLY=PASS
PATCH_OWNER_POSTIMAGES_MATCH_ACCEPTED_PRODUCTION=true
REPLAY_BACKEND_SHA256=ac341a5801f3ed521335fcaac3ed05e3f5179d33ce739ee8fc0788f3f2bd9dee
REPLAY_WEBSOCKET_SHA256=b8681987c0aa04f596b5aaaf6a832941e11a576f547987bb3e8c8423eb5c8e5a
```

Two disposable text-patch generation attempts were discarded before persistence: the first inherited Windows `core.autocrlf`, and the second proved that an outer text patch could still be normalized by the formal repository and lose byte-exact replay semantics for the mixed-line-ending owner files. Neither discarded artifact was committed. The final artifact above uses Git binary patch records and is the only accepted artifact.

## Deterministic functional provenance model

The executable test composition is not a historical commit:

```text
COMPOSITE_TEST_TREE_IS_HISTORICAL_COMMIT=false
COMPOSITE_TEST_TREE_IS_DETERMINISTIC_PROVENANCE_MODEL=true
```

Backend model: accepted auth-cookie closure filesystem plus accepted CHG-0023 `cookies.py`.

WebSocket model: accepted Session/Cookie closure filesystem plus exact CHG-0022 production `xianyu_async.py` plus accepted CHG-0023 `cookie_manager.py`.

The original CHG-0023 deterministic candidate regression harness was rerun on read-only filesystem copies extracted from the accepted immutable Backend and WebSocket candidate images. Containers were created only for `docker cp` and removed without `docker start`.

Backend result:

```text
UNKNOWN_COOKIE_WRITERS=0
MISSING_EXPECTED_BASELINE_CALLERS=0
SESSION_COOKIE_CANDIDATE_AUTH_GATE=PASS
STALE_RESPONSE_CAS=PASS
PER_ACCOUNT_SINGLE_FLIGHT=PASS
HUMAN_QR_STICKY_SAME_FINGERPRINT=PASS
SAFE_MTOP_AUTH_PROBE=PASS
CHG0023_BACKEND_TARGETED=6/6_PASS
QR_FALSE_GREEN_STATIC_COUNT=0
BACKEND_REGRESSION_PASS
```

WebSocket result:

```text
UNKNOWN_COOKIE_WRITERS=0
MISSING_EXPECTED_BASELINE_CALLERS=0
SESSION_COOKIE_CANDIDATE_AUTH_GATE=PASS
STALE_RESPONSE_CAS=PASS
PER_ACCOUNT_SINGLE_FLIGHT=PASS
HUMAN_QR_STICKY_SAME_FINGERPRINT=PASS
SAFE_MTOP_AUTH_PROBE=PASS
CHG0022_NETWORK_REGRESSION=10/10_PASS
REMOTE_TOKEN_CALL_COUNT=0_BY_NETWORK_BRANCH
TOKEN_INVALIDATION_COUNT=0_BY_NETWORK_BRANCH
NETWORK_BACKOFF=true
TOKEN_CACHE_REUSE=true
REMOTE_TOKEN_STORM=false
NEW_REMOTE_TOKEN_BURST_COUNT=0
RECONNECT_LOOP=false
TOKEN_READY_PRODUCER=3/3_PASS
INTERNAL_ENDPOINT_PASSTHROUGH=PASS
WEBSOCKET_REGRESSION_PASS
```

Formal acceptance classification:

```text
CHG0023_TARGETED_TESTS=PASS
QR_FALSE_GREEN_COUNT_MODEL=0
CHG0022_REGRESSION=PASS
REMOTE_TOKEN_CALL_COUNT_DURING_NETWORK_FAULT=0
TOKEN_INVALIDATION_COUNT_DURING_NETWORK_FAULT=0
NETWORK_BACKOFF=true
TOKEN_CACHE_REUSE=true
REMOTE_TOKEN_STORM=false
NEW_REMOTE_TOKEN_BURST_COUNT=0
RECONNECT_LOOP=false
SESSION_COOKIE_SAFETY=PASS
UNKNOWN_COOKIE_WRITERS=0_NEW_UNKNOWN_WRITERS_VS_BASELINE
UNVALIDATED_CANDIDATE_COMMITTED=false
STALE_RESPONSE_RESULT=STALE_DISCARDED
STALE_RESPONSE_COMMIT_COUNT=0
PER_ACCOUNT_SINGLE_FLIGHT=PASS
HUMAN_QR_STICKY_SAME_FINGERPRINT=PASS
SAFE_MTOP_AUTH_PROBE=PASS
VALIDATED_CAS=PASS
```

## Production acceptance — both attempts

Attempt 1 remains preserved as historical evidence:

```text
ATTEMPT_1_EVIDENCE_PRESERVED=true
ATTEMPT_1_BACKEND_REPLACE_RESULT=FAILED_POST_RUNTIME_CONFIG_MISMATCH_LABELS
ATTEMPT_1_ROOT_CAUSE=desktop.docker.io/ports.scheme
ATTEMPT_1_ROLLBACK=PASS
ATTEMPT_1_WEBSOCKET=NOT_ATTEMPTED
COMPANY_REPAIR_PR=7
COMPANY_RUNTIME_AUTHORITY_MERGE=777897b859c7e05cb1fed58a713ad73d04041b9b
```

Attempt 2 is the accepted production activation:

```text
ATTEMPT_2_EVIDENCE_RECORDED=true
BACKEND_REPLACE_RESULT=SUCCESS
WEBSOCKET_REPLACE_RESULT=SUCCESS
SOURCE_RUNTIME_MATCH=true
BACKEND_SOURCE_RUNTIME_MATCH=true
WEBSOCKET_SOURCE_RUNTIME_MATCH=true
ORIGINAL_4_POSITIVE_CONTROLS=PASS
WANGXIA_CONTROL=POSITIVE
NEGATIVE_CONTROLS=PASS
QR_FALSE_GREEN_COUNT=0
CHG0022_REGRESSION=PASS
SESSION_COOKIE_SAFETY=PASS
REMOTE_TOKEN_STORM=false
NEW_REMOTE_TOKEN_BURST_COUNT=0
RECONNECT_LOOP=false
TOKEN_CACHE_REUSE=true
REAL_MESSAGES_SENT=0
RUNTIME_ACCEPTANCE=PASS
```

`WANGXIA_CONTROL=POSITIVE` does not assert `SESSION_AUTH_VALID=true`; that stronger Session claim is intentionally not made.

## Current continuation safety

This formal-persistence continuation performs no production deployment or account/business action:

```text
PRODUCTION_CONTAINER_MUTATION_COUNT=0
PRODUCTION_CONTAINER_START_COUNT=0
REAL_MESSAGES_SENT=0
QR_ACTIONS=0
ITEM_SYNC_PERFORMED=false
```

Disposable extraction containers used for source readback/test filesystem copying were never started and were removed after extraction.

## Formal verification

The current formal branch validation was executed after writing the exact patch/evidence/test set:

```text
CHG0023_FORMAL_ARTIFACT_TEST=5/5_PASS
DETECT_DUPLICATE_CAPABILITIES=PASS
SECURITY_SCAN=PASS
GIT_DIFF_CHECK=PASS
GIT_DIFF_CACHED_CHECK=IMMUTABLE_PATCH_ARTIFACT_ONLY_EXCEPTION__GIT_GENERATED_BINARY_PATCH_FINAL_BLANK_LINE
VALIDATE_CHANGE_RESULT=FAIL_PRE_EXISTING_UNRELATED
VERIFY_REPOSITORY_RESULT=FAIL_PRE_EXISTING_UNRELATED
PRE_EXISTING_UNRELATED_FAILURES=CHG0020_ARCHIVE_MISSING_DESIGN_TASKS
NEW_CHG0023_VERIFY_FAILURES=0
```

`validate_change.py` and `verify_repository.py` both stop only on the already-known archived `CHG-0020-zidongzhua-market-search` governance debt: missing `design.md` and `tasks.md`. That unrelated archive debt is intentionally not repaired in CHG-0023.

`git diff --cached --check` reports only `new blank line at EOF` inside the immutable Git-generated binary patch artifact. The staged patch ends with the normal blank separator emitted by `git diff --binary`; its staged SHA256, two clean-apply checks, and exact two-owner postimage equivalence are locked. Per repository policy, the generated patch bytes are not hand-edited merely to satisfy the outer diff checker.

The repository also contains an already-existing CHG-0022 unit-test path assumption that still reads `changes/active/CHG-0022-websocket-token-network-classification` after CHG-0022 was archived. Re-running that test on the untouched formal start SHA `522a38a55342fbe3d8e7cf55b01d5d8112efeaf3` reproduces the same four `FileNotFoundError` failures, proving they are not introduced by CHG-0023. The actual production-authoritative CHG-0022 executable network regression for this Change is the 10/10 PASS recorded above.

## Integration boundary

Runtime acceptance is complete and T5 is closed. The exact reviewed task files were committed as `7f4d864928baf2d5695ed984e764bd1292158022`, pushed to `chore/CHG-0023-websocket-auto-reply-readiness-contract-restoration`, then fresh-fetched with exact local/remote SHA equality. That readback satisfied the T6 persistence condition; the final task-state/generated-state closeout is a governance-only follow-up commit.

```text
FORMAL_SOURCE_PERSISTED=true
FORMAL_EVIDENCE_PERSISTED=true
FORMAL_BRANCH_PUSHED=true
FIRST_PERSISTENCE_COMMIT=7f4d864928baf2d5695ed984e764bd1292158022
FIRST_PERSISTENCE_LOCAL_REMOTE_MATCH=true
T5_COMPLETE=true
T6_COMPLETE=true
AUTO_REPLY_FULL_PRODUCTION_READY=PENDING_GIT_MAIN_INTEGRATION
NEXT_SINGLE_ACTION=STOP_AND_RETURN_TO_COMMANDER_FOR_CHG0023_GIT_INTEGRATION
```
