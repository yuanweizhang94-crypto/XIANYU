# XIANYU — Desktop Recovery Handoff 2026-09-10

Status: `RECOVERY_IN_PROGRESS`  
Authority type: migration checkpoint + immutable-image Source Authority V2  
This document does not authorize production cutover.

## 1. Machine roles

```text
DESKTOP_HOSTNAME=PC-20250528MGDP
DESKTOP_ROLE=RECOVERY_TEST_TARGET
LAPTOP_CURRENT_WINDOWS_HOSTNAME=WIN-PQGV23OBQET
LAPTOP_HISTORICAL_HOST_ID=HUAWEI-LAPTOP
LAPTOP_ROLE=PRIMARY_LAST_KNOWN / SOURCE_AUTHORITY
ORIGINAL_LAPTOP_IDENTITY_PROVEN=true
PRODUCTION_DOUBLE_RUN=false
```

The laptop historical host id and current Windows hostname have already been proven to refer to the same source Huawei laptop. Do not rename the machine to satisfy the historical string.

## 2. Source baseline

Desktop XIANYU repo path: `D:\XIANYU`.

```text
XIANYU_GITHUB_MAIN=cba57282caf339d155778f3684c156666dea67e9
XIANYU_DESKTOP_LOCAL_HEAD=cba57282caf339d155778f3684c156666dea67e9
XIANYU_SOURCE_READY=true
```

The desktop checkout was safely fast-forwarded; do not reset/clean/stash unknown work and do not move the formal `D:\XIANYU` checkout backward to reconstruct historical Runtime.

## 3. Data/runtime migration already completed

Migration source package: `D:\PC_MIGRATION_20260909`.

The following were restored to desktop and verified at the migration layer:

```text
XIANYU_DOCKER_VOLUMES=PASS
XIANYU_BROWSER_DATA_RESTORED=true
XIANYU_ENV_PRESENT=true
XIANYU_ENV_HASH_MATCH=true
```

The restored set includes MySQL, Redis, backend logs, backup data, static data, WebSocket logs and browser_data. The large browser_data restore finished with the expected regular-file count `613171`.

The `.env` was handled as opaque protected data. Never expose or commit its content.

These restore facts are not equivalent to runtime validation. Until the rebuilt formal Runtime starts successfully, keep:

```text
XIANYU_MYSQL=RESTORED_NOT_RUNTIME_VALIDATED
XIANYU_REDIS=RESTORED_NOT_RUNTIME_VALIDATED
XIANYU_SESSION=NOT_RUNTIME_VALIDATED
XIANYU_PROFILE=NOT_RUNTIME_VALIDATED
```

## 4. Why four Runtime images require reconstruction

The migration package preserved Runtime identity, data and volumes but did not contain Docker image tar files for the four formal XIANYU application images.

Historical accepted images on the source laptop:

```text
Backend:
xianyu-chg0018-backend-web:chg0037-cv2-dc3c2d3-20260831-r1
image id=sha256:22fcd85af7c0061eb22e54c47f8b9bb1396d6b01039af21153c916ec7a81940f

WebSocket:
xianyu-chg0035-websocket:password-login-canonical-recovery-20260828-r1
image id=sha256:2807e779894fda036ca1d4726ca77308dbc273e430300078a7500384fd20687e

Frontend:
xianyu-chg0018-frontend:account-chat-final-5dd103e-20260829-r1
image id=sha256:d03a9292be8277b374cb4027fb264b0a6bd22f55520aa5ae5834abfb010f317a

Scheduler:
xianyu-chg0027-scheduler:session-cooldown-lineage-20260824-r1
image id=sha256:ab70f051e962a3138103de969e6976e13c923da86d9222eabf2b9223394331e8
```

Old Runtime history used accepted runtime preimages and is not always representable as `one Git commit + one patch`. Do not reconstruct by tag/date guessing or by forcing current main into an old image tag.

## 5. Recovery packages on desktop

The reconstruction stage uses three local packages:

```text
D:\XIANYU_RUNTIME_DELTA_20260910
D:\XIANYU_RECOVERY_AUTHORITY_V2_20260910
D:\XIANYU_RECOVERY_BYTE_SUPPLEMENT_20260910
```

Before use, each package must pass its own `SHA256SUMS.txt` verification with mismatch count 0.

Do not commit these packages to GitHub.

## 6. Authority V2 closure

The original legacy `RECOVERY_PATCH_SHA256` and old aggregate-SHA generation method could no longer be traced back to their original authority evidence. They are retained as historical/unproven values and no longer serve as the final V2 build gate.

A stronger source identity was created directly from immutable accepted Docker image bytes using a persisted canonical per-file manifest/aggregate method.

Final immutable-image Source Authority V2:

```text
BACKEND_V2_SOURCE_FILES=357
BACKEND_V2_TREE_SHA256=24640d4056e9e099a4c7e6d6b106083ae397fc59b4511086e5da602bcc437bed

WEBSOCKET_V2_SOURCE_FILES=251
WEBSOCKET_V2_TREE_SHA256=5b242d9adcbb7073bd9a371f605a124193f1d1448b501a3c2ec15fb02ece3494

SCHEDULER_V2_SOURCE_FILES=231
SCHEDULER_V2_TREE_SHA256=7560296587d8a4446da8fd24a6ba968944909abd64c5c94aeb5cbccc2814cc91

FRONTEND_CONTEXT_FILE_COUNT=452
FRONTEND_CONTEXT_TREE_SHA256=247dda4b8b4db9aa78d1eded11f6d9aed8088a9a5b12fa863f88f1b3d3bcc961
FRONTEND_OCI_REVISION=5dd103e096cb921e979ae1a3923febe5c357fff8
```

## 7. Byte-preserving supplement closure

The current recovery patches reproduced the logical Source but differed from immutable image bytes only by line-ending representation in a small subset.

Mismatch sets from the immutable image comparison:

```text
Backend=27 files
WebSocket=16 files
Scheduler=21 files
Total=64 files
```

Those exact files were extracted byte-for-byte from the immutable accepted images and packaged as `D:\XIANYU_RECOVERY_BYTE_SUPPLEMENT_20260910`.

After applying the current recovery patch and overlaying only those supplement files:

```text
BACKEND_FINAL_SOURCE_FILES=357
BACKEND_FINAL_TREE_SHA256=24640d4056e9e099a4c7e6d6b106083ae397fc59b4511086e5da602bcc437bed
BACKEND_FINAL_MISSING_COUNT=0
BACKEND_FINAL_EXTRA_COUNT=0
BACKEND_FINAL_SIZE_MISMATCH_COUNT=0
BACKEND_FINAL_CONTENT_MISMATCH_COUNT=0
BACKEND_SOURCE_IDENTITY_V2_MATCH=true

WEBSOCKET_FINAL_SOURCE_FILES=251
WEBSOCKET_FINAL_TREE_SHA256=5b242d9adcbb7073bd9a371f605a124193f1d1448b501a3c2ec15fb02ece3494
WEBSOCKET_FINAL_MISSING_COUNT=0
WEBSOCKET_FINAL_EXTRA_COUNT=0
WEBSOCKET_FINAL_SIZE_MISMATCH_COUNT=0
WEBSOCKET_FINAL_CONTENT_MISMATCH_COUNT=0
WEBSOCKET_SOURCE_IDENTITY_V2_MATCH=true

SCHEDULER_FINAL_SOURCE_FILES=231
SCHEDULER_FINAL_TREE_SHA256=7560296587d8a4446da8fd24a6ba968944909abd64c5c94aeb5cbccc2814cc91
SCHEDULER_FINAL_MISSING_COUNT=0
SCHEDULER_FINAL_EXTRA_COUNT=0
SCHEDULER_FINAL_SIZE_MISMATCH_COUNT=0
SCHEDULER_FINAL_CONTENT_MISMATCH_COUNT=0
SCHEDULER_SOURCE_IDENTITY_V2_MATCH=true
```

Therefore:

```text
BYTE_SUPPLEMENT_RECOVERY=PASS
RECOVERY_AUTHORITY_V2=PASS
BYTE_SUPPLEMENT_PROVEN=true
DESKTOP_RECONSTRUCTION_CAN_USE_V2=true
```

## 8. Desktop reconstruction/build target

The desktop must reconstruct in isolated workspaces only, then build new recovery tags rather than impersonating the old image tags:

```text
xianyu-chg0018-backend-web:desktop-recovery-20260910-r1
xianyu-chg0035-websocket:desktop-recovery-20260910-r1
xianyu-chg0018-frontend:desktop-recovery-20260910-r1
xianyu-chg0027-scheduler:desktop-recovery-20260910-r1
```

Build order should be serial. A 502/timeout does not prove build failure; first inspect BuildKit/process/image state before retrying.

## 9. TEST Runtime requirements

Only after all four reconstruction/build gates pass may the desktop start the formal TEST Runtime.

Before WebSocket/Scheduler connection:

```text
REAL_PUBLISH_DISABLED=true
REAL_AUTO_REPLY_SEND_DISABLED=true
REAL_AUTO_DELIVERY_DISABLED=true
PRODUCTION_SCHEDULER_JOBS_DISABLED=true
```

The TEST Runtime must validate, without real platform writes:

- MySQL connection/table count (migration baseline: 63 tables, subject to current authoritative explanation if changed)
- Redis PING/DBSIZE
- Backend/Frontend health
- Session/Profile adoption
- default account/login state
- read-only Chat connectivity/conversations
- Auto Reply engine/config readiness without sending a message
- Publish capability/dry-run without submitting an item
- WebSocket technical health
- Scheduler technical health with production jobs disabled

If platform login/QR/OTP/face is truly required after migration, stop only at that human boundary. Do not forge Cookie/ONLINE state.

## 10. Cutover gate

Until every TEST requirement has passed:

```text
DESKTOP_TEST_MODE!=PASS
DESKTOP_READY_FOR_CUTOVER=false
DESKTOP_PRODUCTION=false
LAPTOP_ROLE=PRIMARY_LAST_KNOWN
PRODUCTION_DOUBLE_RUN=false
```

When `DESKTOP_READY_FOR_CUTOVER=true` is eventually proven, that still does not authorize production activation. The final cutover is a separate controlled step:

```text
freeze laptop production Scheduler/WebSocket/Auto Reply/workers
→ final state/readback if required
→ start desktop production
→ prove desktop PRIMARY
→ prove laptop STANDBY
→ prove PRODUCTION_DOUBLE_RUN=false
```

## 11. Current next action at this checkpoint

```text
NEXT_UNIQUE_ACTION=
DESKTOP VERIFY THREE PACKAGES
→ RECONSTRUCT WITH V2 + BYTE SUPPLEMENT
→ BUILD FOUR DESKTOP RECOVERY IMAGES
→ START SIDE-EFFECT-DISABLED TEST RUNTIME
→ COMPLETE MYSQL/REDIS/SESSION/ACCOUNT/CHAT/AUTOREPLY/PUBLISH/WEBSOCKET/SCHEDULER READBACK
→ SET DESKTOP_READY_FOR_CUTOVER=true ONLY IF ALL PASS
```

If a newer execution report is supplied after this file was written, treat that report as a newer checkpoint and verify it against current GitHub/Runtime rather than reverting to this document.
