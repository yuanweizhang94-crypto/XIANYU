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

T1 through T5 are complete.

T6 is the next task but is not authorized in this execution and has not started.

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
