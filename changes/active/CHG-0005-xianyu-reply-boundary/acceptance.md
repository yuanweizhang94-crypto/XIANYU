# CHG-0005 Acceptance

Status: APPROVED
Change ID: CHG-0005-xianyu-reply-boundary

## T1 approval acceptance criteria

1. CHG-0004 exists only under `changes/archive/`.
2. CHG-0004 status is ARCHIVED in proposal, design, tasks, and acceptance.
3. CHG-0004 historical tests remain preserved under the archive directory.
4. CHG-0004 records PR #4 merge commit `bab7a1a86239cb4dba9b2f7dc8db0ff33bc80dc6`.
5. Exactly one Active Change exists.
6. The Active Change is CHG-0005-xianyu-reply-boundary.
7. CHG-0005 status is APPROVED in all four governance documents.
8. CHG-0005 contains exactly nine tasks.
9. Only T1 is complete.
10. T2 through T9 remain incomplete.
11. generated/PROJECT_STATE.json identifies CHG-0005 as the only Active APPROVED Change.
12. PROJECT_STATE completed task count is 1.
13. PROJECT_STATE next_task is `T2 Finalize reply rule, template, and decision terminology`.
14. CAP-XY-MESSAGE remains verified.
15. CAP-XY-MESSAGE remains unbound.
16. CAP-XY-MESSAGE keeps Candidate SHA `49498e6f30944883c1a0a5a504932bbd02fc86de`.
17. CAP-XY-MESSAGE keeps exactly seven implementation paths.
18. CAP-XY-MESSAGE keeps exactly ten test paths.
19. CAP-XY-MESSAGE acceptance evidence points to the archived CHG-0004 test.
20. CAP-XY-REPLY remains planned.
21. CAP-XY-REPLY remains unbound.
22. CAP-XY-REPLY has no implementation paths.
23. CAP-XY-REPLY has no test paths.
24. CAP-XY-REPLY has no last verified commit.
25. No Reply Runtime, Rule Engine, Template Engine, Service, Repository, Worker, API, Web UI, database table, Migration, Scheduler Job, WeCom adapter, AI adapter, or sending behavior is added.
26. No real Xianyu account, message sending, Cookie, Token, Secret, Session Material, browser Profile, customer data, or external network behavior is added.
27. No dependency, CI, Runtime, Core, Account, Message, Migration, Capability Registry binding, or implementation evidence file is modified.
28. Capability counts remain planned 5 and verified 5.
29. Unit tests remain 225.
30. Contract tests remain 78.
31. Permanent acceptance tests remain 15.
32. Active acceptance tests remain 4.
33. Full collection remains 322.
34. Repository verification, security scan, duplicate capability validation, Ruff, Mypy, Pip Check, and all required GitHub Actions pass.
35. PR #5 remains Draft, open, and unmerged.
36. Requested Reviewers remain empty.
37. Auto-merge remains disabled.
38. T2 has not started.
39. Ready for review, Merge, and branch deletion remain unauthorized.

## Current authorization

Project-owner approval for CHG-0005 is recorded.

T1 through T5 are complete.

T6 is the next executable task and has not started.

Implementation, Capability binding, Ready for review, Reviewer request, Auto-merge, and Merge are not authorized.

## T2 acceptance criteria

1. CHG-0005 remains APPROVED.
2. T1 and T2 are complete.
3. T3 through T9 remain incomplete.
4. PROJECT_STATE reports completed tasks as 2 / 9.
5. PROJECT_STATE next_task is `T3 Approve authorization, risk-control, and content-safety boundaries`.
6. Final terminology covers ReplyRule, ReplyCondition, ReplyTemplate, ReplyDecision, ReplyDecisionType, ReplyReasonCode, ReplyEvaluationContext, repository protocols, and service interfaces.
7. ReplyEvaluationContext is explicitly a reply-side adapter contract and does not modify CAP-XY-MESSAGE semantics.
8. CAP-XY-REPLY remains planned, unbound, and without implementation paths, test paths, active_change, or last_verified_commit.
9. CAPABILITY_REGISTRY is not modified.
10. No Runtime, Migration, dependency, workflow, Ready transition, reviewer request, auto-merge, or merge is authorized.


## T3 acceptance criteria

1. CHG-0005 remains APPROVED.
2. T1 through T3 are complete.
3. T4 through T9 remain incomplete.
4. PROJECT_STATE reports completed tasks as 3 / 9.
5. PROJECT_STATE next_task is `T4 Approve matching, precedence, fallback, and escalation boundaries`.
6. Authorization states fail closed unless explicitly authorized.
7. Risk-control states fail closed unless explicitly allowed or low risk.
8. Sensitive-topic and policy-blocked content suppress replies before template rendering.
9. Unsupported language and human-transfer cases return escalation decisions only.
10. Audit and logging boundaries prohibit full message text, credential material, browser state, raw network payloads, and secret material.
11. CAP-XY-REPLY remains planned, unbound, and without implementation paths, test paths, active_change, or last_verified_commit.
12. CAPABILITY_REGISTRY is not modified.
13. No Runtime, Migration, dependency, workflow, Ready transition, reviewer request, auto-merge, or merge is authorized.


## T4 acceptance criteria

1. CHG-0005 remains APPROVED.
2. T1 through T4 are complete.
3. T5 through T9 remain incomplete.
4. PROJECT_STATE reports completed tasks as 4 / 9.
5. PROJECT_STATE next_task is `T5 Approve ownership, persistence, lifecycle, and failure boundaries`.
6. Matching operators are limited to `equals`, `contains`, `starts_with`, and `ends_with`.
7. Normalization and case handling are explicit and deterministic.
8. Conditions in one rule combine with AND only.
9. Smaller integer priority values have higher priority.
10. Multiple highest-priority matches produce `CONFLICT` and no rendered text.
11. No eligible matching rule produces `NO_MATCH` and no rendered text.
12. Invalid fields, operators, templates, variables, lifecycle states, or priorities produce `INVALID_INPUT`.
13. T3 suppression and escalation decisions take precedence over matching and rendering.
14. CAP-XY-REPLY remains planned, unbound, and without implementation paths, test paths, active_change, or last_verified_commit.
15. CAPABILITY_REGISTRY is not modified.
16. No Runtime, Migration, dependency, workflow, Ready transition, reviewer request, auto-merge, or merge is authorized.


## T5 acceptance criteria

1. CHG-0005 remains APPROVED.
2. T1 through T5 are complete.
3. T6 through T9 remain incomplete.
4. PROJECT_STATE reports completed tasks as 5 / 9.
5. PROJECT_STATE next_task is `T6 Implement only the approved local fixed-script reply boundary`.
6. Ownership, domain model, public interfaces, database design, lifecycle, migration plan, failure behavior, and test matrix are approved in design documentation.
7. Migration created in Phase 1: no.
8. Runtime files created in Phase 1: no.
9. CAP-XY-REPLY remains planned, unbound, and without implementation paths, test paths, active_change, or last_verified_commit.
10. CAPABILITY_REGISTRY is not modified.
11. CAP-XY-MESSAGE remains verified and unchanged.
12. No dependency, workflow, Ready transition, reviewer request, auto-merge, merge, branch deletion, or CHG-0006 is authorized.
13. The diagnostic `tests` Mypy baseline remains accepted only up to 145 errors in 16 files.
14. Technical-debt cleanup of unrelated `tests/` Mypy issues is not performed.


## Owner Design Review corrective acceptance criteria

1. CHG-0005 remains APPROVED.
2. T1 through T5 remain complete.
3. T6 through T9 remain incomplete.
4. PROJECT_STATE reports completed tasks as 5 / 9.
5. PROJECT_STATE next_task is `T6 Implement only the approved local fixed-script reply boundary`.
6. ReplyRule identity is `(rule_id, version)`.
7. ReplyCondition references exact `(rule_id, rule_version)`.
8. ReplyAuditEvent records optional but exact `rule_version`; when `rule_id` exists, `rule_version` also exists.
9. ReplyRule and ReplyTemplate do not define an independent persisted `enabled` field.
10. `lifecycle_state == ENABLED` is the only rule and template evaluation-eligibility source.
11. `ARCHIVED` is immutable and cannot transition to another lifecycle state.
12. Rule, Template, and Audit repositories have separated responsibilities.
13. ReplyEvaluator returns `ReplyEvaluationResult` and does not render templates.
14. ReplyDecisionService owns template loading, rendering, final decision construction, sanitized audit recording, commit, and rollback.
15. Phase 1 still has no Runtime or Migration.
16. CAP-XY-REPLY remains planned and unbound.
17. Capability counts remain planned 5 / verified 5.
18. T6 requires a separate explicit owner authorization.

## T6 implementation record

T6 is implemented under the approved local fixed-script reply boundary. The runtime package `app/xianyu_system/reply/` and migration `migrations/versions/0004_xianyu_reply_boundary.py` now exist. The implementation remains local and deterministic: no CLI, API, Web UI, worker loop, scheduler, sender, Xianyu client, browser adapter, WeCom adapter, AI adapter, credential resolver, external network behavior, or message sending behavior is introduced.

CAP-XY-REPLY intentionally remains `planned` and unbound during T6: implementation paths, test paths, `active_change`, and `last_verified_commit` are not registered until T8.
