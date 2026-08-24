# CHG-0029 Acceptance

Change ID: CHG-0029-core-capability-closure
Status: ARCHIVED

## Required Acceptance

- CHG-0028 is archived with PR #41 merge commit `4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89` recorded.
- CHG-0029 is the only active Change and contains the three-line execution contract.
- Automatic reply source/runtime/health/account cohort are classified, with token storm false, reconnect loop false, transient classification preserved, QR fail-closed, and no real message sends.
- Online chat source/runtime/websocket health/self-rehydration/classification/conversation-read capability are classified, with no sends and no manual reconnect.
- Product publish CHG-0028 runtime is active or explicitly blocked, with route/source hash evidence, global `ON_DEMAND`/`NOT_CHECKED`, no persisted Publisher readiness writer, no account polling producer, and Direct/Personal Publisher Browser independence preserved.
- CHG-0028 patch deployment uses the current Git blob/LF bytes with SHA256 `CED451293701C53475E23F9B87DF205AB97AFDD0B3696D35A4D9C8675BC4E490`; Windows checkout CRLF bytes are treated only as a local checkout representation and are not the deployment artifact.
- Deterministic tests and relevant regressions pass or are truthfully classified as pre-existing global debt outside CHG-0029.
- Scoped runtime deploy touches only affected XIANYU services and records rollback preimages.
- GitHub persistence verifies local commit SHA equals remote branch SHA, and merge verifies remote main SHA when merge is performed.

## GitHub Closure

`PR_NUMBER=42`

`PR_MERGED=true`

`LOCAL_COMMIT_SHA=a90c508f010d7e46a91b7986154117f50f1fbaed`

`REMOTE_BRANCH_SHA=a90c508f010d7e46a91b7986154117f50f1fbaed`

`MERGE_COMMIT_SHA=fe1b184c9d32c9d94721320702b5d6b0c55fe169`

`REMOTE_MAIN_SHA=fe1b184c9d32c9d94721320702b5d6b0c55fe169`

`SCOPED_CI=SECURITY_PASS__QUALITY_TESTS_FAIL_SAME_AS_MAIN_GLOBAL_DEBT`

`GLOBAL_CI_DEBT_ABSORBED=NO`

## Safety Counters

`REAL_MESSAGES_SENT=0`

`REAL_PRODUCTS_PUBLISHED=0`

`REAL_PRODUCTS_MODIFIED=0`

`ITEM_SYNC_INVOCATION_COUNT=0`

`QR_LOGIN_INVOCATION_COUNT=0`

`MANUAL_RECONNECT_INVOCATION_COUNT=0`

`BROWSER_INVOCATION_COUNT=0`

`PLAYWRIGHT_CDP_INVOCATION_COUNT=0`

`GLOBAL_PERSISTED_PUBLISH_READINESS_WRITER_CREATED=0`

`DIRTY_CHG0018_TOUCHED=0`

## Upstream Capability Audit

Same as proposal: current work uses existing upstream/XIANYU owners for automatic reply, online chat, and publish capability.

## Pinned Upstream Evidence

Same as proposal: pinned matrix upstream `bda1a859df63fa5f24e51398fa80a23490bb6dfc`, production publish lineage `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`, and CHG-0028 route evidence `5984b483b5bfd6c852ef00c22291b1bf163022ee`.

## Existing Local Implementation Search

Current main and archived Changes CHG-0022 through CHG-0028 are the local implementation record. Runtime inspection determines whether merged artifacts are active.

## Reuse Decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate Implementation Risk

No second owner may be created. Any code defect must be repaired in the existing owner only.

## Why Upstream Cannot Satisfy The Requirement

Upstream cannot prove or activate this laptop's current runtime images and production account-cohort state; CHG-0029 supplies that operations wrapper.

## Approved Exception ADR

Not applicable.

## Component Owner

Backend/WebSocket/Scheduler/Frontend remain the runtime component owners; CHG-0029 owns only verification and scoped activation evidence.

## Retirement Plan For Overlapping Local Code

No overlapping local code is introduced.
