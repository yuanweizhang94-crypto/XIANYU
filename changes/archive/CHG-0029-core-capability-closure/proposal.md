# CHG-0029 Core Capability Closure

Change ID: CHG-0029-core-capability-closure
Status: ARCHIVED
Created: 2026-08-25
Predecessor: CHG-0028-publish-readiness-owner-convergence

## User Outcome

Close the three current XIANYU core production capability gaps for automatic reply, online chat, and product publish by proving current GitHub, local source, runtime, account cohort state, existing owner behavior, and runtime activation truth without real message sends, real product publishing, QR login, browser actions, or manual reconnect.

## Execution Contract

User outcome: automatic reply, online chat, and product publish are source-current, runtime-active, health-checked, and truthfully classified by account cohort.

Confirmed blocker: production containers are running older component images; Backend lacks the CHG-0028 selected-account on-demand route in runtime, while WebSocket/Chat/Auto Reply still need current read-only owner and account-cohort verification.

Smallest success test: source/patch deterministic tests pass, only affected official containers are activated when stale, health and runtime source hashes prove the intended files are loaded, and sanitized read-only probes classify all three capabilities without sending messages, publishing products, invoking Item Sync, scanning QR, using Browser/CDP/Playwright, or manually reconnecting.

## Scope

Allowed scope:

- read current GitHub, local source, runtime containers, images, ports, mounts, health, and sanitized logs/status;
- create and maintain this single active Change and evidence;
- apply already-merged source/patch artifacts into affected runtime components when runtime is stale;
- build or commit scoped official runtime images from current production preimages plus approved patch layers;
- replace/restart only affected XIANYU services with rollback preimage recorded;
- run deterministic tests and read-only health/status/conversation/account-cohort probes;
- commit, push, open PR, classify CI, merge normally, and verify remote SHA for this Change.

Forbidden scope:

- real product publish, product modification, item offline/sync, real message send, QR login, face/slider/CAPTCHA bypass, manual reconnect, Browser UI, Playwright, CDP, Profile or port-policy work;
- new Publisher, Chat, WebSocket, Session, Token, Cookie, Account, Scheduler, readiness writer, database table, background producer, sender, or execution owner;
- `GLOBAL_PERSISTED_PUBLISH_READINESS` revival or any `session_maintenance.consumers.publish` writer;
- changes to `D:/xianyu` CHG0018 dirty worktree.

## Upstream Capability Audit

Fresh upstream and existing CHG-0028 evidence identify the native Publisher capability as selected-account on-demand `PublishAccountCapabilityService.detect -> mtop.idle.pc.idleitem.preget`, surfaced through a selected-account route and not persisted globally. Existing upstream ownership for automatic reply and online chat remains WebSocket/Backend native services described by the capability matrix: WebSocket connection, message receiving, online chat, keyword/default reply, account status, token/session renewal, and risk verification signals.

## Pinned Upstream Evidence

Pinned upstream baseline remains `D:/xianyu-upstream-pilot` at `bda1a859df63fa5f24e51398fa80a23490bb6dfc` for capability matrix evidence. Current production publish source lineage includes upstream `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`; CHG-0028 records fresh upstream `29dc831d4498f3174f0502c989a352ef59815553` and selected-account route commit `5984b483b5bfd6c852ef00c22291b1bf163022ee`.

## Existing Local Implementation Search

Current XIANYU `main` at `4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89` contains the approved CHG-0028 patch artifact and deterministic tests, plus archived CHG-0022, CHG-0023, CHG-0026, and CHG-0027 evidence for token/network classification, auto-reply readiness, QR/chat recovery, and transient classification. Runtime inspection must decide whether those merged facts are active in containers.

## Reuse Decision

Decision: WRAP_FOR_OPERATIONS

This Change does not design a new business capability. It activates and verifies the existing upstream/XIANYU owners, applying already-approved source patches only when runtime is stale. If a real code defect is proven after source/current-runtime comparison, that defect must be split into a separate minimal Change or explicitly recorded as a CHG-0029 scoped patch inside the existing owner.

## Duplicate Implementation Risk

Risk is low while CHG-0029 stays an operations/runtime activation and evidence wrapper. Risk becomes high if it creates any second sender, Publisher readiness writer, Chat state machine, Token owner, Session owner, Browser gate, Scheduler producer, or COMPANY-side truth source.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the business owners, but it cannot by itself prove that this laptop's current Docker containers are running the merged XIANYU patch layers, current image source, and accepted production health/account-cohort state. That runtime activation and evidence wrapper is the missing operational requirement.

## Approved Exception ADR

Not applicable. `BUILD_LOCAL_EXCEPTION` is not authorized.

## Component Owner

Automatic reply and online chat owners remain upstream/XIANYU WebSocket and Backend Chat services. Product publish capability owner remains XIANYU Backend selected-account `PublishAccountCapabilityService.detect` and normal Direct/Personal Publisher routing. CHG-0029 owns only operations evidence and scoped runtime activation.

## Retirement Plan For Overlapping Local Code

No overlapping implementation is added. Any temporary deployment helper or extracted runtime workdir is evidence-only and must not become a production owner.
