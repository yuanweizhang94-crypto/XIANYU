# CHG-0006 Acceptance

Status: APPROVED
Change ID: CHG-0006-xianyu-publish-boundary

## Draft-stage acceptance criteria

1. CHG-0005 exists only under `changes/archive/`.
2. CHG-0005 status is ARCHIVED in proposal, design, tasks, and acceptance.
3. CHG-0005 historical acceptance test remains preserved.
4. CHG-0005 records PR #5, feature HEAD `c4f7a3a3d14e34e5ebdaf6abd79587d45137f587`, and merge commit `f00156045d75e632d71ade640a85a4c522568158`.
5. `CAP-XY-REPLY` remains verified.
6. CAP-XY-REPLY Evidence Candidate remains `5724d164619c64e93295595b3acdd1429d24e3e0`.
7. CAP-XY-REPLY keeps exactly eight implementation paths.
8. CAP-XY-REPLY keeps exactly twelve test paths.
9. CAP-XY-REPLY acceptance evidence points to archived CHG-0005.
10. Exactly one Active Change exists.
11. The only Active Change is CHG-0006-xianyu-publish-boundary.
12. CHG-0006 proposal, design, tasks, and acceptance are DRAFT.
13. CHG-0006 has exactly nine tasks.
14. All CHG-0006 tasks are incomplete.
15. DRAFT state has no executable next task.
16. `CAP-XY-PUBLISH` remains planned.
17. `CAP-XY-PUBLISH.active_change` remains null.
18. `CAP-XY-PUBLISH.implementation_paths` remains empty.
19. `CAP-XY-PUBLISH.test_paths` remains empty.
20. `CAP-XY-PUBLISH.last_verified_commit` remains null.
21. Capability totals remain planned 4 and verified 6.
22. No Runtime, Migration, dependency, workflow, or external behavior changes are introduced.
23. No Playwright, browser, or platform access is introduced.
24. No listing publication is introduced.
25. No real data or credential material is introduced.
26. The new PR remains Draft, open, and unmerged.
27. Requested reviewers remain empty.
28. Auto-merge remains disabled.
29. CHG-0006 T1 has not started.
30. Moving beyond DRAFT requires separate authorization.

## Current authorization

CHG-0006 is APPROVED for T1 through T5 governance and design work only.

T1 through T6 are complete.

T7 is the next task but is not authorized in this execution and has not started.

No implementation, capability binding, reviewer request, Ready transition, auto-merge, or merge is authorized.

## T1 acceptance criteria

1. Proposal, design, tasks, and acceptance are all APPROVED.
2. Only T1 is complete.
3. T2 through T9 remain incomplete.
4. PROJECT_STATE reports 1 / 9 tasks complete.
5. PROJECT_STATE next_task is `T2 Finalize listing, publish request, attempt, and outcome terminology`.
6. CAP-XY-PUBLISH remains planned, unbound, with empty implementation_paths, empty test_paths, null active_change, and null last_verified_commit.
7. PR #6 remains Draft, open, and unmerged.
8. No Runtime, Migration, dependency, workflow, Registry, app, or capability evidence change is introduced.

## T2 acceptance criteria

1. T1 and T2 are complete.
2. T3 through T9 remain incomplete.
3. PROJECT_STATE reports 2 / 9 tasks complete.
4. PROJECT_STATE next_task is `T3 Approve permission, credential, risk-control, and platform boundaries`.
5. Approved terminology includes ListingDraft, PublishRequest, PublishValidationResult, PublishDecision, PublishDecisionType, PublishAttempt, PublishAttemptState, PublishOutcomeType, PublishReasonCode, and PublishEvaluationContext.
6. READY is documented as local readiness only and not publication.
7. CAP-XY-PUBLISH remains planned and unbound.

## T3 acceptance criteria

1. T1 through T3 are complete.
2. T4 through T9 remain incomplete.
3. PROJECT_STATE reports 3 / 9 tasks complete.
4. PROJECT_STATE next_task is `T4 Approve validation, idempotency, duplicate, and uncertainty boundaries`.
5. Authorization states are AUTHORIZED, DENIED, and UNKNOWN.
6. Risk states are CLEAR, BLOCKED, and UNKNOWN.
7. UNKNOWN authorization and UNKNOWN risk fail closed.
8. Credential and platform objects remain outside Domain, Service, Repository, audit, and tests.
9. No Playwright, browser, Xianyu, publication, network, Credential, WeCom, or AI behavior is authorized.

## T4 acceptance criteria

1. T1 through T4 are complete.
2. T5 through T9 remain incomplete.
3. PROJECT_STATE reports 4 / 9 tasks complete.
4. PROJECT_STATE next_task is `T5 Approve ownership, persistence, lifecycle, audit, and failure boundaries`.
5. Validation order is deterministic and fail-closed.
6. Required fields and normalization boundaries are documented.
7. Idempotency replay, idempotency conflict, duplicate draft handling, and UNKNOWN outcome manual review are documented.
8. READY is documented as local validation only and not publication.

## T5 acceptance criteria

1. T1 through T5 are complete.
2. T6 through T9 remain incomplete.
3. PROJECT_STATE reports 5 / 9 tasks complete.
4. PROJECT_STATE next_task is `T6 Implement only the separately approved local publishing boundary`.
5. Owner module remains `worker.publish`.
6. Future package path `app/xianyu_system/worker/publish` is documented only and is not created.
7. ListingDraftLifecycle excludes `PUBLISHED` because the local boundary does not publish.
8. Persistence and audit boundaries are conceptual only; no schema, Migration, table, column, or index is introduced.
9. Audit excludes Credential, Cookie, Token, Secret, browser state, raw platform response, real personal data, and complete content.
10. Failure classification and no-retry boundaries are documented.
11. CAP-XY-PUBLISH remains planned, unbound, with empty implementation_paths, empty test_paths, null active_change, and null last_verified_commit.
12. PR #6 remains Draft, open, and unmerged.

## T6 acceptance criteria

1. T1 through T6 are complete.
2. T7 through T9 remain incomplete.
3. PROJECT_STATE reports 6 / 9 tasks complete.
4. PROJECT_STATE next_task is `T7 Add unit, contract, security, and active-change acceptance tests`.
5. The local publish package exists under `app/xianyu_system/worker/publish/`.
6. Domain types match the approved terminology and lifecycle names.
7. Validation order is fixed and fail closed.
8. `synthetic_fixture=false` cannot enter READY.
9. UNKNOWN authorization cannot enter READY.
10. UNKNOWN risk cannot enter READY.
11. Same idempotency key with the same fingerprint is replay.
12. Same idempotency key with a different fingerprint is conflict.
13. A different idempotency key with the same draft revision and fingerprint is duplicate.
14. UNKNOWN historical outcome is manual review.
15. READY is only a local decision for a separately authorized future boundary.
16. Service contains no platform publication behavior.
17. No Playwright, browser, network, Credential, real-data, or platform Adapter behavior exists.
18. Migration `0005_xianyu_publish_boundary` exists and is chained after the reply boundary.
19. CAP-XY-PUBLISH Registry remains planned, unbound, with empty implementation_paths, empty test_paths, null active_change, and null last_verified_commit.
20. T7 has not started.
21. PR #6 remains Draft, open, and unmerged.

## T7 completion record

T7 is complete. Permanent local Publish boundary tests now cover domain normalization, fingerprint stability, validation fail-closed ordering, service idempotency/duplicate/UNKNOWN/persistence-failure behavior, local SQLite persistence contracts, migration constraints, security boundaries, import safety, and active-change acceptance.

CAP-XY-PUBLISH remains planned and unbound until T8. T7 coverage includes test_publish_domain.py, test_publish_fingerprint.py, test_publish_validation.py, test_publish_service.py, test_publish_persistence.py, and test_publish_security.py. T8 is the next task and has not started in the T7 commit.

## T8 Phase A evidence candidate record

T8 Phase A registers CAP-XY-PUBLISH as `implementing` with exact local deterministic Publish implementation and test evidence paths. `active_change` is `CHG-0006-xianyu-publish-boundary`; `last_verified_commit` remains null until the Phase A Candidate commit has completed local verification and GitHub Actions. T8 remains incomplete until Phase B records the verified Candidate SHA.


## CHG-0006 T8 Phase B verification record

CAP-XY-PUBLISH evidence paths are registered and verified for the local deterministic Publish boundary.

Evidence Candidate SHA: `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`

Candidate GitHub Actions result: quality push, quality pull_request, tests push, tests pull_request, security push, and security pull_request all completed successfully.

Registry status: verified

Active change: null

Last verified commit: `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`

Tasks: 8 / 9

Next task: T9 Complete final PR administration

T9 is not authorized and has not started. PR #6 remains Draft, open, and unmerged. Verified does not authorize Ready, reviewer request, review submission, auto-merge, merge, archive, branch deletion, CHG-0007, real Xianyu access, listing publication, media upload, Credential handling, browser automation, external platform access, platform adapter, scheduler, worker loop, retry behavior, dependency change, or workflow change.
